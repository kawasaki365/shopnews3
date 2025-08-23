"""Simple newsfeed for Needles track pants.

The script scrapes supported shopping sites a few times per day
and prints the newest listings.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import schedule

from scrapers import scrape_ebay

DATA_FILE = Path("data.json")


def load_data() -> List[Dict[str, str]]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_data(data: List[Dict[str, str]]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


def scrape_once() -> List[Dict[str, str]]:
    """Fetch data from all scrapers and store new items."""
    data = load_data()
    known_urls = {item["url"] for item in data}
    new_items: List[Dict[str, str]] = []

    for item in scrape_ebay():
        if item["url"] not in known_urls:
            item["fetched_at"] = datetime.utcnow().isoformat()
            data.append(item)
            new_items.append(item)

    data.sort(key=lambda x: x.get("date"), reverse=True)
    save_data(data)
    return new_items


def print_feed(limit: int = 20) -> None:
    data = load_data()
    for item in data[:limit]:
        print(f"{item['date']} | {item['title']} | {item.get('price')} | {item['url']}")


def main(loop: bool = False) -> None:
    new_items = scrape_once()
    print(f"Fetched {len(new_items)} new items. Current feed:")
    print_feed()

    if loop:
        schedule.every(8).hours.do(scrape_once)
        while True:
            schedule.run_pending()
            # sleep for a minute between checks
            time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Needles track pants feed")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run continuously and scrape every few hours",
    )
    args = parser.parse_args()
    main(loop=args.loop)
