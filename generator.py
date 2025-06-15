import os
from storage import Storage

<<<<<<< HEAD
DATA_DIR = "data"
OUTPUT_DIR = "docs"
TAGS_DIR = os.path.join(OUTPUT_DIR, "tags")
TEMPLATE_DIR = "templates"
=======
DOCS_DIR = "docs"
TAGS_DIR = os.path.join(DOCS_DIR, "tags")
STATIC_PATH_INDEX = "static/base.css"
STATIC_PATH_TAG = "../static/base.css"
>>>>>>> 🔥 Removed templates, moved all content to docs with updated styling

def build_index(tags):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Drishti Current Affairs</title>
  <link rel="stylesheet" href="{STATIC_PATH_INDEX}">
</head>
<body>
  <h1>Current Affairs Tags</h1>
  <ul>
"""
    for tag in sorted(tags):
        safe_tag = tag.replace(" ", "_")
        html += f"<li><a href='tags/{safe_tag}.html'>{tag}</a></li>\n"

    html += """
  </ul>
</body>
</html>
"""
    return html

def build_tag_page(tag, article_ids, articles_dict):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{tag} Articles</title>
  <link rel="stylesheet" href="{STATIC_PATH_TAG}">
</head>
<body>
  <h1>{tag}</h1>
"""

    for aid in article_ids:
        article = articles_dict.get(aid)
        if not article:
            continue
        html += f"""
  <div class="article">
    <h3>{article['title']}</h3>
    <p><em>{article['date']}</em></p>
    {article['content']}
  </div>
"""

    html += """
</body>
</html>
"""
    return html

def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(TAGS_DIR, exist_ok=True)

    storage = Storage()
    index_html = build_index(storage.tags)
    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    for tag, ids in storage.tags.items():
        tag_filename = tag.replace(" ", "_") + ".html"
        tag_html = build_tag_page(tag, ids, storage.articles)
        with open(os.path.join(TAGS_DIR, tag_filename), "w", encoding="utf-8") as f:
            f.write(tag_html)

    print(f"✅ HTML pages generated in {DOCS_DIR}/")

if __name__ == "__main__":
    main()
