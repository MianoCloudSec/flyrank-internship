# Polite Scraper

A small scraping pipeline that downloads the first three catalogue pages of
[Books to Scrape](https://books.toscrape.com), pulls out clean structured
data for all 60 books, checks every record against a schema, and ends every
run with an honest report — all without being rude to the site.

This project is part of my FlyRank internship track. It's a deliberate
shift from the backend API work in the rest of this repo: instead of
serving data, this project's job is *collecting* it responsibly.

---

## Target Classification

- **Site**: Books to Scrape (https://books.toscrape.com)
- **Why this site**: it explicitly exists as a public sandbox built for
  people to practice scraping on — not a real production site with real
  commercial data.
- **Scope**: the first 3 catalogue pages only (60 book listings).
- **Data collected**: book title, price, availability, star rating, and a
  product page link — all publicly displayed catalogue information.
- **robots.txt result**: I requested
  `https://books.toscrape.com/robots.txt` myself and got back a **404** —
  no robots file exists at all. A missing file isn't automatic permission
  by itself; what actually makes this appropriate is the site's own
  stated purpose as a scraping practice sandbox.

I will not reuse this code on another site without checking its rules and
terms first.

---

## The pipeline

This scraper is built as six small, separate steps, matching a real
production pattern (FlyRank runs this exact shape for audits and content
pipelines): **fetch → extract → normalize → validate → store → report**.

Each step only does one job, and each one can prove it worked:

| Step      | What it answers                          | Proof                              |
|-----------|-------------------------------------------|-------------------------------------|
| Fetch     | Did the page really arrive?               | A saved HTML file + status code     |
| Extract   | Which parts of the page do I need?        | Raw text fields                     |
| Normalize | How does `"£51.77"` become a number?      | 60 clean typed values, absolute URLs |
| Validate  | Is every record safe to store?            | A schema check; bad records set aside |
| Store     | Can another program use this?             | `books.json`                        |
| Report    | Did the run actually work?                | A few honest numbers                |

## Being a polite guest

Three habits are baked into how this scraper behaves, on purpose:

- **It identifies itself.** Every request sends a real `User-Agent`
  (`FlyRankInternshipA9/1.0 (+link-to-this-repo)`), so anyone looking at
  the site's server logs can tell who's making the request and why.
- **It gives up if the site doesn't respond.** Every request has a
  timeout — it never waits forever for a page that isn't coming.
- **It only ever asks the real site once per page.** Every fetched page
  is cached to disk. While I was developing and restarting this script
  dozens of times, the real site only ever saw one genuine request per
  page — every other run read my own saved copy instead.

## Trusting nothing I scraped

A web page is untrusted input, the same way an API request body is. Every
record goes through an explicit validation step (Pydantic) before it's
allowed anywhere near the final output file. If a record doesn't match the
expected shape, it's set aside — not silently dropped, and not allowed to
crash the whole run.

---

## Project structure

```text
scraper/
│
├── src/
│   └── main.py         ← the full pipeline
├── cache/                ← saved HTML (gitignored, regenerates on first run)
├── books.json             ← the final, validated output
└── README.md
```

## How to run it

```bash
git clone https://github.com/MianoCloudSec/flyrank-internship.git
cd flyrank-internship/scraper
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install requests beautifulsoup4 pydantic
python src/main.py
```

The first run fetches all 3 catalogue pages for real and prints `FETCH`
for each one. Run it again and every page prints `CACHE` instead — no
second request ever reaches the real site.

Output lands in `books.json`, and a run report prints at the end:

```text
--- Run Report ---
Pages fetched: 3
Books extracted: 60
Valid books: 60
Invalid books: 0
Price range: £12.84 - £57.31
Average price: £35.00
```

## Example record

```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "in_stock": true,
  "rating": 3,
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

---

## A real bug I hit: character encoding

My first working extraction returned prices like `"Â£51.77"` instead of
`"£51.77"` — an extra, garbled character in front of every price.

**Why it happened**: `£` isn't a plain ASCII character — it needs a
specific text encoding (UTF-8) to display correctly. `requests` guessed
the wrong encoding when converting the page's raw bytes into text,
interpreting the two bytes that make up `£` as two separate characters
instead of one.

**The fix**: explicitly setting `response.encoding = "utf-8"` before
reading `response.text`, so `requests` uses the correct encoding instead
of guessing. I also had to clear my already-cached HTML files and refetch,
since the corrupted text had already been saved to disk — fixing the code
alone didn't fix data that was already cached with the bug baked in.

This is a common real-world scraping gotcha, and a good reminder that
"it looks like it worked" isn't the same as actually checking the output
character by character.

---

## What I learned

Building this as six separate functions — one per pipeline stage — made
debugging far easier than one large script would have. When the encoding
bug showed up, I knew immediately it had to be in `fetch_page`, not
anywhere else, because that's the only function that touches raw HTTP
responses. Extract, normalize, and validate never needed to change at all.

I also came away with a clearer sense of what "trust nothing you scraped"
actually means in practice — it's not a vague warning, it's a concrete
step (schema validation) that sits between raw scraped data and anything
downstream ever seeing it.