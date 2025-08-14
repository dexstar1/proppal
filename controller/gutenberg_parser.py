import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# --- Config ---
CACHE_DIR = Path(".wp_block_styles_cache")
CACHE_DIR.mkdir(exist_ok=True)

# --- Gutenberg block renderers ---

def render_paragraph(attrs, inner_html):
    return f"<p>{inner_html}</p>"

def render_heading(attrs, inner_html):
    level = attrs.get("level", 2)
    return f"<h{level}>{inner_html}</h{level}>"

def render_image(attrs, inner_html):
    src = attrs.get("url", "")
    alt = attrs.get("alt", "")
    return f'<figure><img src="{src}" alt="{alt}"/>{inner_html}</figure>'

def render_list(attrs, inner_html):
    tag = "ol" if attrs.get("ordered") else "ul"
    return f"<{tag}>{inner_html}</{tag}>"

def render_quote(attrs, inner_html):
    return f"<blockquote>{inner_html}</blockquote>"

def render_code(attrs, inner_html):
    return f"<pre><code>{inner_html}</code></pre>"

def render_table(attrs, inner_html):
    return f"<table>{inner_html}</table>"

# Add more renderers here if needed

BLOCK_RENDERERS = {
    "core/paragraph": render_paragraph,
    "core/heading": render_heading,
    "core/image": render_image,
    "core/list": render_list,
    "core/quote": render_quote,
    "core/code": render_code,
    "core/table": render_table,
}

# --- Fetch WP post content from REST API ---

def fetch_wp_content(api_url, post_id, use_rendered=True):
    url = f"{api_url.rstrip('/')}/wp-json/wp/v2/pages/{post_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["content"]["rendered" if use_rendered else "raw"]

# --- Gutenberg block parser ---

def parse_gutenberg_html(html):
    pattern = re.compile(
        r"<!--\s+wp:([a-zA-Z0-9\/_-]+)(.*?)\s+-->(.*?)<!--\s+\/wp:\1\s+-->",
        re.S,
    )

    output_html = ""
    pos = 0
    for match in pattern.finditer(html):
        block_name = match.group(1)
        attrs_str = match.group(2).strip()
        inner_html = match.group(3).strip()

        try:
            attrs = json.loads(attrs_str) if attrs_str else {}
        except json.JSONDecodeError:
            attrs = {}

        renderer = BLOCK_RENDERERS.get(block_name, lambda a, h: h)
        rendered = renderer(attrs, inner_html)

        output_html += html[pos : match.start()] + rendered
        pos = match.end()

    output_html += html[pos:]
    return output_html

# --- Crawl the site and download all CSS files ---

def crawl_and_download_all_css(site_url, css_path):
    """
    Crawl the homepage and download all linked CSS files (including theme, plugins, block-library, etc).
    Save the combined CSS to css_path.
    """
    resp = requests.get(site_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    css_blocks = []

    # Download all <link rel="stylesheet"> CSS files
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href and href.endswith(".css"):
            # Make absolute if needed
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = site_url.rstrip("/") + href
            elif not href.startswith("http"):
                href = site_url.rstrip("/") + "/" + href
            try:
                css_resp = requests.get(href)
                if css_resp.status_code == 200:
                    css_blocks.append(f"/* {href} */\n" + css_resp.text)
            except Exception as e:
                print(f"Failed to fetch CSS from {href}: {e}")

    # Also grab any <style> tags from the homepage
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            css_blocks.append(style_tag.string)

    # Combine and write to css_path
    all_css = "\n\n".join(css_blocks)
    css_file = Path(css_path)
    css_file.parent.mkdir(parents=True, exist_ok=True)
    css_file.write_text(all_css, encoding="utf-8")
    return all_css

# --- Read local gutenberg_styles.css ---

def get_local_gutenberg_styles(css_path):
    css_file = Path(css_path)
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    else:
        print(f"Warning: {css_file} not found.")
        return ""

# --- Final render function ---

def render_wp_post(api_url, post_id, css_path, site_url, use_rendered=True):
    # Crawl and download all CSS for the site
    all_styles = crawl_and_download_all_css(site_url, css_path)
    html_content = fetch_wp_content(api_url, post_id, use_rendered)
    parsed_html = parse_gutenberg_html(html_content)

    final_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{all_styles}
</style>
</head>
<body>
{parsed_html}
</body>
</html>"""

    # Convert to FastHTML
    fasthtml_module = html_to_fasthtml(final_html)
    
    # Save FastHTML module
    module_path = Path("wp_content.py")
    module_path.write_text(fasthtml_module, encoding="utf-8")
    print(f"FastHTML module saved to {module_path}")

    return final_html

def html_to_fasthtml(html_content):
    """Convert HTML string to FastHTML components"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    def convert_element(element):
        if isinstance(element, str):
            return element.strip() if element.strip() else ""
            
        if element.name == 'div':
            children = [convert_element(child) for child in element.children]
            children = [c for c in children if c]  # Remove empty strings
            cls = element.get('class', [])
            cls_str = ' '.join(cls) if cls else None
            return f"Div({', '.join(children)}" + (f", cls='{cls_str}')" if cls_str else ")")
            
        elif element.name == 'p':
            children = [convert_element(child) for child in element.children]
            children = [c for c in children if c]  # Remove empty strings
            cls = element.get('class', [])
            cls_str = ' '.join(cls) if cls else None
            return f"P({', '.join(children)}" + (f", cls='{cls_str}')" if cls_str else ")")
            
        elif element.name == 'h1':
            return f"H1('{element.get_text()}')"
        elif element.name == 'h2':
            return f"H2('{element.get_text()}')"
        elif element.name == 'h3':
            return f"H3('{element.get_text()}')"
        elif element.name == 'h4':
            return f"H4('{element.get_text()}')"
            
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '')
            cls = element.get('class', [])
            cls_str = ' '.join(cls) if cls else None
            return f"Img(src='{src}', alt='{alt}'" + (f", cls='{cls_str}')" if cls_str else ")")
            
        elif element.name == 'a':
            href = element.get('href', '#')
            cls = element.get('class', [])
            cls_str = ' '.join(cls) if cls else None
            return f"A('{element.get_text()}', href='{href}'" + (f", cls='{cls_str}')" if cls_str else ")")
            
        return ""

    # Convert the body content
    body = soup.find('body')
    if not body:
        return ""
        
    fasthtml_components = []
    for element in body.children:
        if isinstance(element, str) and not element.strip():
            continue
        converted = convert_element(element)
        if converted:
            fasthtml_components.append(converted)

    # Generate the FastHTML module
    module_content = f"""from fasthtml.common import *

def WPContent():
    return Section(
        {',\\n        '.join(fasthtml_components)},
        cls='wp-content'
    )
"""
    
    return module_content

# --- Example usage ---

if __name__ == "__main__":
    API_URL = "https://gutenbergui.com"  # Your WordPress site REST API base
    SITE_URL = "https://gutenbergui.com" # The homepage to crawl for CSS
    POST_ID = 174                        # Post ID to fetch
    CSS_PATH = "../.wp_block_styles_cache/gutenberg_styles.css"  # Path to your local CSS file

    output_html = render_wp_post(API_URL, POST_ID, CSS_PATH, SITE_URL, use_rendered=True)

    with open("rendered_post.html", "w", encoding="utf-8") as f:
        f.write(output_html)

    print("Rendered post saved to rendered_post.html")