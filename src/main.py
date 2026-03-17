import requests
import argparse
import json
import os
from datetime import datetime

def fetch_top_markets(limit=10, tag=None):
    """Fetches active markets from Polymarket with optional tag filter."""
    url = f"https://gamma-api.polymarket.com/markets?active=true&limit={limit}"
    if tag:
        url += f"&tag={tag}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket Miner")
    parser.add_argument("--limit", type=int, default=10, help="Number of markets to fetch")
    parser.add_argument("--tag", type=str, help="Tag filter (e.g., politics, crypto)")
    args = parser.parse_args()

    markets = fetch_top_markets(limit=args.limit, tag=args.tag)

    # Create unique filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/markets-{date_str}.jsonl"

    if markets:
        with open(filename, "a") as f:
            entry = {"timestamp": datetime.now().isoformat(), "markets": markets}
            f.write(json.dumps(entry) + "\n")
        print(f"✅ Logged {len(markets)} markets to {filename}")
    else:
        print("⚠️  No markets fetched or error occurred.")
        print(f"Check the file: {filename}")
