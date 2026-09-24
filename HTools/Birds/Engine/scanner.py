from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from http.client import InvalidURL
from threading import Lock


class BirdsScanner:

    def __init__(
        self,
        base_url,
        wordlist,
        threads=10,
        timeout=5
    ):
        self.base_url = (
            base_url.rstrip("/") + "/"
        )

        self.wordlist = wordlist

        self.threads = max(
            1,
            min(int(threads), 200)
        )

        self.timeout = timeout

        self.checked = 0
        self.found = 0
        self.errors = 0

        self.lock = Lock()

    def _make_url(self, path):

        path = path.strip().lstrip("/")

        encoded = quote(
            path,
            safe="/%:@-._~!$&'()*+,;="
        )

        return urljoin(
            self.base_url,
            encoded
        )

    def _request(self, path):

        url = self._make_url(path)

        try:

            request = Request(
                url,
                headers={
                    "User-Agent":
                        "Birds/2.1",
                    "Accept":
                        "*/*",
                }
            )

            with urlopen(
                request,
                timeout=self.timeout
            ) as response:

                return {
                    "url": url,
                    "path": path,
                    "status": response.status,
                }

        except HTTPError as error:

            return {
                "url": url,
                "path": path,
                "status": error.code,
            }

        except (
            URLError,
            TimeoutError,
            OSError,
            InvalidURL,
            ValueError,
        ):

            with self.lock:
                self.errors += 1

            return None

    def load_wordlist(self):

        paths = []

        with open(
            self.wordlist,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                paths.append(line)

        return list(
            dict.fromkeys(paths)
        )

    def baseline(self):

        result = self._request(
            "__birds_nonexistent_"
            "9f72c1__"
        )

        if result:
            return result["status"]

        return 404

    def scan(self, callback=None):

        paths = self.load_wordlist()

        total = len(paths)

        self.checked = 0
        self.found = 0
        self.errors = 0

        not_found_status = (
            self.baseline()
        )

        with ThreadPoolExecutor(
            max_workers=self.threads
        ) as executor:

            futures = {
                executor.submit(
                    self._request,
                    path
                ): path
                for path in paths
            }

            try:

                for future in as_completed(
                    futures
                ):

                    try:
                        result = (
                            future.result()
                        )

                    except Exception:
                        with self.lock:
                            self.errors += 1

                        result = None

                    with self.lock:
                        self.checked += 1
                        current = self.checked

                    if result is None:
                        continue

                    status = result["status"]

                    if status != not_found_status:

                        with self.lock:
                            self.found += 1

                        if callback:
                            callback(
                                result,
                                current,
                                total
                            )

            except KeyboardInterrupt:

                for future in futures:
                    future.cancel()

                raise

        return {
            "checked": self.checked,
            "found": self.found,
            "errors": self.errors,
            "total": total,
        }