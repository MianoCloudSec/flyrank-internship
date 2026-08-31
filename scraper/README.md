# Polite Scraper

## Target Classification

- **Site**: Books to Scrape (https://books.toscrape.com)
- **Why this site**: it explicitly exists as a public sandbox built for
  people to practice scraping on — not a real production site with real
  commercial data.
- **Scope**: the first 3 catalogue pages only (roughly 60 book listings).
- **Data collected**: book title, price, availability, rating, and a
  product page link — all publicly displayed catalogue information.
- **robots.txt result**: requested https://books.toscrape.com/robots.txt —
  returned a 404 (no robots file found). A missing file isn't permission
  by itself; the site's own stated purpose as a scraping practice sandbox
  is what makes this appropriate.

I will not reuse this code on another site without checking its rules and
terms first.