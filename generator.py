import os
import re
from storage import Storage

OUTPUT_DIR = "docs"
TAGS_DIR = os.path.join(OUTPUT_DIR, "tags")

STATIC_PATH_INDEX = "static/base.css"
STATIC_PATH_TAG = "../static/base.css"

def safe_filename(tag):
    """Convert tag to a safe filename for filesystem use."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', tag.replace(" ", "_")) + ".html"

def build_index(tags, articles):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Drishti Current Affairs</title>
  <link rel="stylesheet" href="{STATIC_PATH_INDEX}">
  <style>
    .badge {{
      background-color: red;
      color: white;
      border-radius: 50%;
      padding: 3px 7px;
      font-size: 12px;
      margin-left: 8px;
      vertical-align: middle;
      display: none;
    }}
    li {{
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>
  <h1>Current Affairs Tags</h1>
  <ul>
"""
    for tag in sorted(tags):
        safe_tag = re.sub(r'[^a-zA-Z0-9_]', '_', tag.replace(" ", "_"))
        article_ids = list(dict.fromkeys(tags[tag]))  # Deduplicate here
        valid_article_ids = [aid for aid in article_ids if aid in articles]
        if not valid_article_ids:
            continue
        latest_date = max([articles[aid]['date'] for aid in valid_article_ids])
        html += f"""    <li>
      <a href='tags/{safe_tag}.html' 
         data-tag="{safe_tag}" 
         data-latest="{latest_date}" 
         data-count="{len(valid_article_ids)}">
         {tag}
         <span class="badge" id="badge-{safe_tag}"></span>
      </a>
    </li>
"""

    html += """
  </ul>
  <script>
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll("a[data-tag]").forEach(link => {
        const tag = link.dataset.tag;
        const latest = new Date(link.dataset.latest);
        const count = parseInt(link.dataset.count);
        const lastVisit = localStorage.getItem("visit_" + tag);
        const badge = document.getElementById("badge-" + tag);

        if (!lastVisit || new Date(lastVisit) < latest) {
          badge.textContent = count;
          badge.style.display = "inline-block";
        }
      });

      document.querySelectorAll("a[data-tag]").forEach(link => {
        link.addEventListener("click", function () {
          localStorage.setItem("visit_" + this.dataset.tag, new Date().toISOString());
        });
      });
    });
  </script>
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    @media (max-width: 600px) {{
      body {{
        padding: 10px;
        font-size: 16px;
      }}
      h1 {{
        font-size: 24px;
      }}
    }}
  </style>
</head>
<body>
  <h1>{tag}</h1>
"""
    for aid in list(dict.fromkeys(article_ids)):  # Deduplicate again
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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TAGS_DIR, exist_ok=True)

    storage = Storage()

    index_html = build_index(storage.tags, storage.articles)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    for tag, ids in storage.tags.items():
        unique_ids = list(dict.fromkeys(ids))
        valid_ids = [aid for aid in unique_ids if aid in storage.articles]
        if not valid_ids:
            continue
        tag_filename = safe_filename(tag)
        tag_html = build_tag_page(tag, valid_ids, storage.articles)
        with open(os.path.join(TAGS_DIR, tag_filename), "w", encoding="utf-8") as f:
            f.write(tag_html)

    print(f"✅ HTML pages generated in {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
