#!/usr/bin/env python3
"""Scrape official GICS Sector + Sub-Industry for the S&P 1500
(S&P 500 + S&P 400 + S&P 600) from Wikipedia and emit gics.json keyed by ticker.

    Local run:  pip install pandas lxml requests && python scrape.py
    CI:         see .github/workflows/update.yml (weekly)

Output shape:
    { "AAPL": { "sector": "Information Technology",
                "subIndustry": "Technology Hardware, Storage & Peripherals" }, ... }
"""
import json
import sys
from io import StringIO

import pandas as pd
import requests

PAGES = [
    "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (gics-data scraper; +https://github.com/imjnoenter/gics-data)"
}

REQUIRED = {"Symbol", "GICS Sector", "GICS Sub-Industry"}

# A full scrape yields ~1,500 rows. Anything well below that means a page changed
# format or a fetch failed — refuse to overwrite good data with a broken partial.
MIN_EXPECTED = 1000


def find_constituents_table(tables):
    """Pick the table whose columns include Symbol / GICS Sector / GICS Sub-Industry,
    rather than trusting a fixed index (Wikipedia reorders tables over time)."""
    for df in tables:
        cols = {str(c).strip() for c in df.columns}
        if REQUIRED.issubset(cols):
            return df
    return None


def scrape():
    out = {}
    for url in PAGES:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        df = find_constituents_table(pd.read_html(StringIO(resp.text)))
        if df is None:
            print(f"WARN: no constituents table on {url}", file=sys.stderr)
            continue
        for _, row in df.iterrows():
            sym = str(row["Symbol"]).strip().upper()
            if not sym or sym == "NAN":
                continue
            out[sym] = {
                "sector": str(row["GICS Sector"]).strip(),
                "subIndustry": str(row["GICS Sub-Industry"]).strip(),
            }
    return out


def main():
    data = scrape()
    if len(data) < MIN_EXPECTED:
        print(
            f"ERROR: only {len(data)} symbols scraped (< {MIN_EXPECTED}); "
            "refusing to overwrite gics.json",
            file=sys.stderr,
        )
        sys.exit(1)
    with open("gics.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(f"Wrote gics.json with {len(data)} symbols.")


if __name__ == "__main__":
    main()
