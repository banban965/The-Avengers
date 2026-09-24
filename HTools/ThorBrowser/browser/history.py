import json
import os

from config import HISTORY_FILE


class History:

    def __init__(self):
        self.file = HISTORY_FILE
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

        if url in data:
            data.remove(url)

        data.insert(0, url)

        self._save(data[:100])

    def get_all(self):
        return self._load()

    def clear(self):
        self._save([])
