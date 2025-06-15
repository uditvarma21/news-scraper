import json
import os

class Storage:
    def __init__(self, tag_path="data/tags.json", article_path="data/articles.json"):
        self.tag_path = tag_path
        self.article_path = article_path
        self.tags = self._load_json(tag_path)
        self.articles = self._load_json(article_path)

        # Ensure both are dictionaries
        if not isinstance(self.tags, dict):
            self.tags = {}
        if not isinstance(self.articles, dict):
            self.articles = {}

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        return {}
                    return data
                except json.JSONDecodeError:
                    return {}
        return {}

    def add_article(self, article):
        article_id = article["id"]
        self.articles[article_id] = article

        for tag in article["tags"]:
            if tag not in self.tags:
                self.tags[tag] = []
            if article_id not in self.tags[tag]:
                self.tags[tag].append(article_id)

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(self.tag_path, "w", encoding="utf-8") as f:
            json.dump(self.tags, f, ensure_ascii=False, indent=2)

        with open(self.article_path, "w", encoding="utf-8") as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
