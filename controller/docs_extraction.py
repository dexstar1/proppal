import requests
from bs4 import BeautifulSoup
import os

def extract_section(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    section = soup.find("section", class_="px-md-10 py-10")
    if section:
        return section
    else:
        print("Section with class 'px-md-10 py-10' not found.")
        return None

def html_to_fasthtml(section):
    # Basic conversion: handles headings, paragraphs, divs, spans, i, a, hr, etc.
    def convert(el):
        if isinstance(el, str):
            return repr(el.strip()) if el.strip() else ""
        tag = el.name
        cls = el.get("class", [])
        cls_str = " ".join(cls) if cls else None
        children = [convert(child) for child in el.children if convert(child)]
        children_str = ", ".join(children)
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            return f"{tag.upper()}({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "p":
            return f"P({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "div":
            return f"Div({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "span":
            return f"Span({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "i":
            return f"I({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "a":
            href = el.get("href", "#")
            return f"A({children_str}, href={repr(href)}{', cls=' + repr(cls_str) if cls_str else ''})"
        elif tag == "hr":
            return "Hr()"
        elif tag == "time":
            dt = el.get("datetime", "")
            return f"Time({children_str}, datetime={repr(dt)})"
        elif tag == "code":
            return f"Code({children_str}{', cls=' + repr(cls_str) if cls_str else ''})"
        else:
            # fallback for unknown tags
            return children_str
    body = convert(section)
    return f"""from fasthtml.common import *

def Module():
    return Section(
        {body},
        cls="px-md-10 py-10"
    )
"""

if __name__ == "__main__":
    docs_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    os.makedirs(docs_folder, exist_ok=True)
    while True:
        url = input("Enter the docs URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
        section = extract_section(url)
        if section:
            module_code = html_to_fasthtml(section)
            print("\nPreview of FastHTML module:\n")
            print(module_code)
            save = input("Save to docs folder? (y/n): ").strip().lower()
            if save == 'y':
                mod_name = input("Enter module name (e.g. reviews): ").strip()
                filename = os.path.join(docs_folder, f"{mod_name}.py")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(module_code)
                print(f"Saved to {filename}\n")