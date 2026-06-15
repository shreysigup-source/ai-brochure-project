import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_page_html(url):
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        if href:
            absolute = urljoin(base_url, href)
            links.append(absolute)
    return links

def filter_links(links, base_url):
    good_keywords = ["about", "service", "product", "solution", "contact", "industry"]
    bad_keywords = ["career", "privacy", "login", "terms", "signup", "blog"]
    
    filtered = []
    for link in links:
        if not link.startswith(base_url):
            continue
        if any(bad in link.lower() for bad in bad_keywords):
            continue
        if any(good in link.lower() for good in good_keywords):
            filtered.append(link)
    return filtered

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    
    for tag in soup(["nav", "footer", "header", "script", "style"]):
        tag.decompose()
    
    text = soup.get_text(separator=" ", strip=True)
    return text

if __name__ == "__main__":
    html = get_page_html("https://books.toscrape.com")
    text = extract_text(html)
    print(text[:1000])