# gics-data

Official **GICS Sector + Sub-Industry** for the S&P 1500 (S&P 500 + 400 + 600),
scraped from Wikipedia and published as a single static JSON.

## Consume

```
https://raw.githubusercontent.com/imjnoenter/gics-data/main/gics.json
```

Served with `Access-Control-Allow-Origin: *`, so it can be fetched cross-origin
from any browser page (no proxy, no key).

### Shape

```json
{
  "AAPL": { "sector": "Information Technology", "subIndustry": "Technology Hardware, Storage & Peripherals" },
  "JPM":  { "sector": "Financials", "subIndustry": "Diversified Banks" }
}
```

Keys are tickers in dot notation (e.g. `BRK.B`).

## Coverage

~1,500 US large/mid/small-cap stocks. Anything outside the S&P 1500 (ETFs,
foreign/ADRs, micro-caps, recent IPOs) is **not** included — consumers should
fall back to their own source for those.

## Refresh

- `.github/workflows/update.yml` runs `scrape.py` every Monday (and on manual
  dispatch), committing `gics.json` only when it changes.
- `scrape.py` refuses to write a result with fewer than 1,000 symbols, so a
  broken scrape can't overwrite good data.

## Run locally

```
pip install pandas lxml requests
python scrape.py
```

## Source

GICS classification from the Wikipedia constituent lists:
[S&P 500](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) ·
[S&P 400](https://en.wikipedia.org/wiki/List_of_S%26P_400_companies) ·
[S&P 600](https://en.wikipedia.org/wiki/List_of_S%26P_600_companies).
GICS is a trademark of MSCI and S&P Dow Jones Indices.
