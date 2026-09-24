import subprocess
import urllib.parse

from browser.history import History
from config import SEARCH_ENGINE


class ViaBrowser:

    def __init__(self):
        self.history = History()

    def normalize(self, url):
        url = url.strip()

        if not url:
            return None

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    def open(self, url):
        url = self.normalize(url)

        if not url:
            return False

        self.history.add(url)

        try:
            result = subprocess.run(
                [
                    "am",
                    "start",
                    "-a",
                    "android.intent.action.VIEW",
                    "-d",
                    url
                ],
                capture_output=True,
                text=True
            )

            return result.returncode == 0

        except OSError as error:
            print(f"[Thor] Browser error: {error}")
            return False

    def search(self, query):
        query = query.strip()

        if not query:
            return False

        encoded = urllib.parse.quote_plus(query)

        return self.open(
            SEARCH_ENGINE + encoded
        )
