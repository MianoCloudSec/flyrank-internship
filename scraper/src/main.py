import os
import requests

CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_PATH = "cache/catalogue-page-1.html"
HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/MianoCloudSec/flyrank-internship)"
}
TIMEOUT_SECONDS = 10


def fetch_page(url, cache_path):
    if os.path.exists(cache_path):
        print(f"CACHE: reading {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as file:
            return file.read()

    print(f"FETCH: requesting {url}")
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)

    if response.status_code != 200:
        raise Exception(f"Fetch failed: status code {response.status_code}")

    with open(cache_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    return response.text


if __name__ == "__main__":
    html = fetch_page(CATALOGUE_URL, CACHE_PATH)
    print(f"Got {len(html)} characters of HTML")