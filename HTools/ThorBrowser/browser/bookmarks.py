import json
import os

from config import BOOKMARKS_FILE


class Bookmarks:

    def __init__(self):
        self.file = BOOKMARKS_FILE
        self._ensure()

    def _ensure(self):
        directory = os.path.dirname(self.file)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file):
            self._save([])

    def _load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list):
                    return data

        except (OSError, json.JSONDecodeError):
            pass

        return []

    def _save(self, data):
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

    def add(self, url):
        data = self._load()

        if url not in data:
            data.append(url)
            self._save(data)
            return True

        return False

    def remove(self, url):
        data = self._load()

        if url in data:
            data.remove(url)
            self._save(data)
            return True

        return False

    def get_all(self):
        return self._load()
