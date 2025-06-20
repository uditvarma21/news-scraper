import requests
from bs4 import BeautifulSoup
from storage import Storage
from datetime import datetime

BASE = "https://www.drishtiias.com/current-affairs-news-analysis-editorials/news-analysis"

def scrape_by_date(date_str):
    url = BASE + "/" + date_str
    print("🔍 Fetching:", url)
    r = requests.get(url)
    r.raise_for_status()

    # Check for fallback to homepage
    if "Latest Updates" in r.text and "Search" in r.text:
        print("⚠️ Redirected to homepage — likely no article for this date.")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.select("div.article-detail")

    if not articles:
        print("❌ No articles found.")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        return []

    news = []

    for article in articles:
        title_tag = article.find("h1", id="dynamic-title")
        if not title_tag:
            continue
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
            classes = child.get("class", [])
            if child.name == "h1" and child.get("id") == "dynamic-title":
                continue
            if child.name == "div" and ("tags-new" in classes or "starRating" in classes or "next-post" in classes):
                continue
            content_html += str(child)

        news.append({
            "id": title,
            "date": date_str,
            "title": title,
            "tags": tags,
            "content": content_html.strip()
        })

    return news

def main():
    # 🔁 Use today's date
    date_str = datetime.now().strftime("%d-%m-%Y")
    print(f"📅 Running scraper for {date_str}")
    items = scrape_by_date(date_str)

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
