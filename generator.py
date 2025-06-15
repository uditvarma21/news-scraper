import os
import json

DATA_DIR = "data"
OUTPUT_DIR = "docs"
TAGS_DIR = os.path.join(OUTPUT_DIR, "tags")
TEMPLATE_DIR = "templates"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_html(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def flatten_articles(articles_json):
    if isinstance(articles_json, list) and len(articles_json) == 1 and isinstance(articles_json[0], dict):
        return list(articles_json[0].values())
    return articles_json

def build_tag_page(tag, article_ids, articles_dict):
    articles = [a for a in articles_dict if a["id"] in article_ids]
    articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    articles_html = ""
    for article in articles:
        articles_html += (
            f"<div class='article'>"
            f"<h3>{article['title']}</h3>"
            f"<div>{article['content']}</div>"
            f"</div>\n"
        )
    with open(os.path.join(TEMPLATE_DIR, "tag.html")) as f:
        template = f.read()
    return template.replace("{{ tag_name }}", tag).replace("{{ articles_by_date }}", articles_html)

def build_index_page(tags):
    tag_links = "\n".join(
        f"<li><a href='tags/{tag.replace(' ', '_')}.html'>{tag}</a></li>" for tag in tags
    )
    with open(os.path.join(TEMPLATE_DIR, "index.html")) as f:
        template = f.read()
    return template.replace("{{ tag_links }}", tag_links)

def main():
    print("📦 Loading data...")
    articles_dict = load_json(os.path.join(DATA_DIR, "articles.json"))  # Now a dict
    articles_list = list(articles_dict.values())  # Convert to list for processing
    tags_dict = load_json(os.path.join(DATA_DIR, "tags.json"))

    print("🛠️ Generating tag HTML pages...")
    for tag, ids in tags_dict.items():
        html = build_tag_page(tag, ids, articles_list)
        tag_filename = os.path.join(TAGS_DIR, f"{tag.replace(' ', '_')}.html")
        save_html(html, tag_filename)

    print("🛠️ Generating index.html...")
    index_html = build_index_page(tags_dict.keys())
    save_html(index_html, os.path.join(OUTPUT_DIR, "index.html"))

    print("✅ Completed generation!")

if __name__ == "__main__":
    main()
