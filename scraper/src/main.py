import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
CACHE_DIR = "cache"
HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/MianoCloudSec/flyrank-internship)"
}
TIMEOUT_SECONDS = 10
NUM_PAGES = 3

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url, cache_path):
    if os.path.exists(cache_path):
        print(f"CACHE: reading {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as file:
            return file.read()

    print(f"FETCH: requesting {url}")
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)

    if response.status_code != 200:
        raise Exception(f"Fetch failed: status code {response.status_code}")

    response.encoding = "utf-8"

    with open(cache_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    return response.text


def fetch_all_catalogue_pages():
    pages = []
    for page_number in range(1, NUM_PAGES + 1):
        url = BASE_CATALOGUE_URL.format(page_number)
        cache_path = os.path.join(CACHE_DIR, f"catalogue-page-{page_number}.html")
        html = fetch_page(url, cache_path)
        pages.append({"url": url, "html": html})
    return pages


def extract_books(page_url, html):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        title = title_tag["title"] if title_tag else None

        relative_link = title_tag["href"] if title_tag else None
        absolute_link = urljoin(page_url, relative_link) if relative_link else None

        price_tag = article.select_one("p.price_color")
        price_text = price_tag.get_text(strip=True) if price_tag else None

        availability_tag = article.select_one("p.instock.availability")
        availability_text = availability_tag.get_text(strip=True) if availability_tag else None

        rating_tag = article.select_one("p.star-rating")
        rating_word = None
        if rating_tag:
            classes = rating_tag.get("class", [])
            for word in RATING_WORDS:
                if word in classes:
                    rating_word = word
                    break

        books.append({
            "title": title,
            "price_text": price_text,
            "availability_text": availability_text,
            "rating_word": rating_word,
            "url": absolute_link,
        })

    return books


def normalize_book(raw_book):
    price = None
    if raw_book["price_text"]:
        price_digits = re.sub(r"[^\d.]", "", raw_book["price_text"])
        price = float(price_digits) if price_digits else None

    in_stock = None
    if raw_book["availability_text"]:
        in_stock = "in stock" in raw_book["availability_text"].lower()

    rating = RATING_WORDS.get(raw_book["rating_word"])

    return {
        "title": raw_book["title"],
        "price": price,
        "in_stock": in_stock,
        "rating": rating,
        "url": raw_book["url"],
    }


if __name__ == "__main__":
    pages = fetch_all_catalogue_pages()

    all_raw_books = []
    for page in pages:
        raw_books = extract_books(page["url"], page["html"])
        all_raw_books.extend(raw_books)

    all_books = [normalize_book(raw_book) for raw_book in all_raw_books]

    print(f"Extracted and normalized {len(all_books)} books")
    print(all_books[0])