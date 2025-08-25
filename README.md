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
newest listing date. The file is trimmed to the latest 200 entries, and
the web frontend displays at most that many listings.

Before scraping any website, ensure that doing so complies with the
website's terms of service.

## GitHub Pages

The contents of this repository are served on GitHub Pages at
`https://<username>.github.io/shopnews3/`.

GitHub Pages publishes straight from the `main` branch. To update the
live site:

1. Run `python feed.py` to scrape new listings and update `data.json`.
2. Commit the updated files and push to `main`.
3. GitHub Pages will automatically deploy the changes.

