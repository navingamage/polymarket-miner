import requests

def fetch_top_markets():
    """Fetches the top 10 active markets from Polymarket."""
    # Gamma API endpoint for active markets
    url = "https://gamma-api.polymarket.com/markets?active=true&limit=10"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    print("Fetching top 10 active markets on Polymarket...")
    markets = fetch_top_markets()
    for idx, market in enumerate(markets, 1):
        question = market.get('question', 'N/A')
        volume = market.get('volume', '0')
        print(f"{idx}. {question} (Volume: {volume})")
