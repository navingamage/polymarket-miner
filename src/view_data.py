import json
import sys

# Data file location
DATA_FILE = "data/markets.jsonl"

def view_latest_markets(lines=5):
    """Prints the last N market snapshots from the log file."""
    try:
        with open(DATA_FILE, "r") as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Data file not found: {DATA_FILE}")
        print("Run: python3 src/main.py --output data/markets.jsonl")
        return

    # Show last N entries
    recent = all_lines[-lines:] if len(all_lines) > lines else all_lines

    for line in recent:
        entry = json.loads(line.strip())
        timestamp = entry.get('timestamp', 'N/A')
        markets = entry.get('markets', [])
        
        print(f"\n--- Snapshot: {timestamp} ---")
        for idx, market in enumerate(markets, 1):
            question = market.get('question', 'N/A')
            volume_str = market.get('volume', '0')
            try:
                volume = float(volume_str)
                print(f"{idx}. {question}")
                print(f"   Volume: ${volume:.2f}")
            except ValueError:
                print(f"{idx}. {question}")
                print(f"   Volume: {volume_str}")

if __name__ == "__main__":
    print(f"📖 Viewing latest market snapshots from: {DATA_FILE}")
    view_latest_markets()