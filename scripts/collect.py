import argparse
import json
import os
import time
import requests
from pathlib import Path

API_URL = "https://api.openbrewerydb.org/v1/breweries"

def fetch_breweries(per_page=200, max_pages=10, delay=0.5):
    all_rows = []
    for page in range(1, max_pages + 1):
        params = {"per_page": per_page, "page": page}
        r = requests.get(API_URL, params=params, timeout=30)
        r.raise_for_status()
        rows = r.json()
        if not rows:
            break
        all_rows.extend(rows)
        time.sleep(delay)
    return all_rows

def main(out_path="data/raw/breweries.json", per_page=200, max_pages=10):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    rows = fetch_breweries(per_page=per_page, max_pages=max_pages)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(rows)} records to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/raw/breweries.json")
    parser.add_argument("--per-page", type=int, default=200)
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()
    main(out_path=args.out, per_page=args.per_page, max_pages=args.max_pages)