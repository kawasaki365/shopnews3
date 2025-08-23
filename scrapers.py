"""Scrapers for various shopping sites.

Currently includes a scraper for eBay search results which
are available for scraping under eBay's terms of service.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Dict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


def scrape_ebay(query: str = "needles track pants") -> Iterable[Dict[str, str]]:
    """Scrape eBay for the given query sorted by newest listings.

    The function fetches the eBay search results page, parses the HTML and
    returns a list of items containing title, price, URL and listing date.
    """
    url = (
        "https://www.ebay.com/sch/i.html?_nkw="
        f"{quote_plus(query)}&_sop=10"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"eBay request failed: {exc}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for li in soup.select(".s-item"):
        title_elem = li.select_one(".s-item__title")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        if title == "Shop on eBay":
            # placeholder entries which do not represent actual products
            continue
        link_elem = li.select_one("a.s-item__link")
        price_elem = li.select_one(".s-item__price")
        date_elem = li.select_one(".s-item__listingDate")

        link = link_elem["href"] if link_elem else None
        price = price_elem.get_text(strip=True) if price_elem else None
        if date_elem:
            text = date_elem.get_text(strip=True)
            try:
                listing_dt = datetime.strptime(
                    f"{text} {datetime.utcnow().year}", "%b-%d %H:%M %Y"
                )
            except ValueError:
                listing_dt = datetime.utcnow()
        else:
            listing_dt = datetime.utcnow()
        items.append(
            {
                "site": "eBay",
                "title": title,
                "price": price,
                "url": link,
                "date": listing_dt.isoformat(),
            }
        )
    return items
