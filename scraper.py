import requests
from bs4 import BeautifulSoup
from storage import Storage
from datetime import datetime, timedelta

BASE = "https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis"

def get_article_links(date_str):
    url = f"{BASE}/{date_str}"
    print("🔍 Fetching listing:", url)
    r = requests.get(url)
    r.raise_for_status()

    if "Latest Updates" in r.text and "Search" in r.text:
        print("⚠️ Redirected to homepage — likely no article for this date.")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    article_links = []

    for a in soup.select("h2.title a"):
        href = a.get("href")
        if href and href.startswith("/"):
            full_url = "https://www.drishtiias.com" + href
            article_links.append(full_url)

    print(f"🔗 Found {len(article_links)} article links.")
    return article_links

def scrape_article(url, date_str):
    print("📰 Fetching article:", url)
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    article = soup.select_one("div.article-detail")

    if not article:
        print("❌ No article-detail found for", url)
        return None

    title_tag = article.find("h1", id="dynamic-title")
    if not title_tag:
        return None
    title = title_tag.get_text(strip=True)

    # Tags
    tags = []
    tag_block = article.find("div", class_="tags-new")
    if tag_block:
        tags = [a.get_text(strip=True) for a in tag_block.find_all("a")]

    # Remove unwanted sections
    for unwanted_class in ["starRating", "next-post"]:
        unwanted = article.find("div", class_=unwanted_class)
        if unwanted:
            unwanted.decompose()

    # Keep full HTML content
    content_html = ""
    for child in article.find_all(recursive=False):
        if child.name == "h1" and child.get("id") == "dynamic-title":
            continue
        if child.name == "div" and any(cls in child.get("class", []) for cls in ["tags-new", "starRating", "next-post"]):
            continue
        content_html += str(child)

    return {
        "id": title,
        "date": date_str,
        "title": title,
        "tags": tags,
        "content": content_html.strip()
    }

def scrape_all_articles_for_date(date_str):
    links = get_article_links(date_str)
    news = []

    for url in links:
        article = scrape_article(url, date_str)
        if article:
            news.append(article)

    return news

def main():
    # Use yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%d-%m-%Y")
    print(f"📅 Running scraper for {date_str}")
    items = scrape_all_articles_for_date(date_str)

    if not items:
        print("⚠️ No articles processed.")
    else:
        storage = Storage()
        for item in items:
            storage.add_article(item)
        storage.save()
        print(f"✅ Saved {len(items)} articles.")

if __name__ == "__main__":
    main()
