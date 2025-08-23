# Needles Track Pants Newsfeed

This project keeps track of newly listed **Needles track pants** from
shopping websites that permit scraping. It currently supports eBay and
is structured so that additional scrapers can be added easily.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run a single update and print the feed:

```bash
python feed.py
```

Run continuously and scrape every eight hours:

```bash
python feed.py --loop
```

Results are stored in `data.json`. Each entry contains the title, price,
URL and listing date. The feed printed to the console is sorted by the
newest listing date.

Before scraping any website, ensure that doing so complies with the
website's terms of service.
