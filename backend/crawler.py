import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Links containing these words are likely the pages we actually want to read.
CATEGORY_KEYWORDS = {
    "about": ["about"],
    "services": ["service"],
    "products": ["product"],
    "industries": ["industry", "industries"],
    "contact": ["contact"],
}

# Links containing these words are pages we never want (careers, blog posts, etc.)
BAD_KEYWORDS = ["career", "privacy", "login", "terms", "signup", "blog"]

# Safety limit: how many pages (including the homepage) we will visit per website,
# so a huge site can't make the crawler run forever.
MAX_PAGES = 6


def get_page_html(url):
    """Downloads the raw HTML of one page. Returns None if anything goes wrong."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_links(html, base_url):
    """Pulls every <a href="..."> out of a page and turns it into a full absolute URL."""
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")

        if not href:
            continue
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        absolute = urljoin(base_url, href)
        links.append(absolute)

    return links


def categorize_links(links, base_url):
    """
    Sorts links into buckets like "about", "services", "contact", etc. based on
    keywords found in the URL itself. Links to other websites, or links matching
    BAD_KEYWORDS (career, privacy, login...), are skipped entirely.

    Returns something like:
      {
        "about": ["https://company.com/about-us"],
        "services": ["https://company.com/services"],
        "products": [],
        "industries": [],
        "contact": ["https://company.com/contact"]
      }
    """
    categorized = {category: [] for category in CATEGORY_KEYWORDS}

    for link in links:
        link_lower = link.lower()

        if not link.startswith(base_url):
            continue
        if any(bad in link_lower for bad in BAD_KEYWORDS):
            continue

        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in link_lower for keyword in keywords):
                if link not in categorized[category]:
                    categorized[category].append(link)

    return categorized


def extract_text(html):
    """Turns a page's HTML into plain readable text, removing nav/footer/menus/scripts."""
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["nav", "footer", "header", "script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text


def crawl_website(base_url):
    """
    The main function main.py calls. Given a company's homepage URL, this:
      1. Downloads the homepage and reads its text.
      2. Finds links to "about", "services", "products", "industries", "contact" pages.
      3. Visits a few of those pages (up to MAX_PAGES total) and reads their text too.

    Returns a dictionary like:
      {
        "home": "...",
        "about": "...",
        "services": "...",
        "products": "...",
        "industries": "...",
        "contact": "..."
      }
    Categories with no matching page are simply left as an empty string -- extractor.py
    already knows to skip empty categories when it builds its prompt.
    """
    MAX_CHARS_PER_PAGE = 5000  # roughly one page worth of reading, keeps the AI's request small

    base_url = base_url.rstrip("/")

    home_html = get_page_html(base_url)
    if home_html is None:
        # If we can't even load the homepage, there's nothing more we can do.
        return {"home": ""}

    crawled_data = {"home": extract_text(home_html)[:MAX_CHARS_PER_PAGE]}

    links = extract_links(home_html, base_url)
    categorized = categorize_links(links, base_url)

    pages_visited = 1  # the homepage already counts as one page

    for category, category_links in categorized.items():
        page_text = ""

        for link in category_links:
            if pages_visited >= MAX_PAGES:
                break

            page_html = get_page_html(link)
            pages_visited += 1

            if page_html:
                page_text += " " + extract_text(page_html)

        crawled_data[category] = page_text.strip()[:MAX_CHARS_PER_PAGE]

    return crawled_data


if __name__ == "__main__":
    data = crawl_website("https://books.toscrape.com")
    for category, text in data.items():
        print(f"\n--- {category.upper()} ---")
        print(text[:300])