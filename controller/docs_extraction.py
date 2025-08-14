import requests
from bs4 import BeautifulSoup

def extract_section(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    section = soup.find("section", class_="px-md-10 py-10")
    if section:
        return section.prettify()
    else:
        print("Section with class 'px-md-10 py-10' not found.")
        return ""

if __name__ == "__main__":
    while True:
        url = input("Enter the docs URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
        html = extract_section(url)
        if html:
            print("\nExtracted Section:\n")
            print(html)
            # Optional: Save to file
            save = input("Save to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename (e.g. reviews_section.html): ").strip()
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Saved to {filename}\n")