"""
Opportunity Finder - Compares sentiment vs market prices
Finds mispriced markets for manual trading
"""

import json
import requests
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rate_limiter import POLYMARKET_LIMITER, OPENROUTER_LIMITER

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

def check_api_key():
    """Check if API key is properly configured"""
    if not API_KEY:
        print("❌ ERROR: OPENROUTER_API_KEY not found in environment!")
        print("Please set it: export OPENROUTER_API_KEY='your-key-here'")
        exit(1)

    if len(API_KEY) < 20:
        print("❌ ERROR: API key appears too short")
        print(f"Length: {len(API_KEY)}")
        print("Please check your API key")
        exit(1)

    print(f"✅ API Key: {API_KEY[:15]}... (length: {len(API_KEY)})")
    return API_KEY

MODEL_ID = "z-ai/glm-4.7-flash"
MARKETS_FILE = "data/markets-2026-03-17.jsonl"

def load_markets():
    """Load latest markets from file"""
    with open(MARKETS_FILE, "r") as f:
        entry = json.loads(f.readlines()[-1])
        return entry['markets']

def analyze_sentiment(markets):
    """Get sentiment for markets using OpenRouter API"""
    prompt = f"""Analyze the sentiment for these Polymarket questions:
{chr(10).join([f'{i+1}. {m["question"]}' for i, m in enumerate(markets[:20])])}

For each, determine: BULLISH, BEARISH, or NEUTRAL.
Return valid JSON: [{{"question": "...", "sentiment": "BULLISH", "confidence": "high"}}]"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a sentiment analyzer. Output JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 5000
    }

    OPENROUTER_LIMITER.wait_if_needed()

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"📥 Received response: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")

        response.raise_for_status()
        result = response.json()

        # Clean markdown
        text = result['choices'][0]['message']['content']
        text = text.strip()
        if text.startswith("```json"): text = text[7:]
        elif text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return []

def find_opportunities(markets, sentiment):
    """Find trading opportunities based on sentiment vs market prices"""
    opportunities = []

    for market, sent in zip(markets, sentiment):
        question = market['question']

        # Parse outcome prices (might be stringified JSON array)
        outcome_prices = market.get('outcomePrices', ['0', '0'])

        if isinstance(outcome_prices, str):
            try:
                outcome_prices = json.loads(outcome_prices)
            except:
                outcome_prices = ['0', '0']

        price_yes = outcome_prices[0] if len(outcome_prices) > 0 else '0'
        price_no = outcome_prices[1] if len(outcome_prices) > 1 else '0'
        volume = market.get('volumeNum', 0)

        # Simple logic: if price is low and sentiment is BULLISH, it's undervalued
        if sent['sentiment'] == 'BULLISH' and float(price_yes) < 0.5:
            opportunities.append({
                'type': 'BUY_OPPORTUNITY',
                'market': question[:80],
                'price': float(price_yes),
                'sentiment': sent['sentiment'],
                'confidence': sent['confidence'],
                'action': f"BET YES at {float(price_yes):.2%} (market is cheap!)"
            })
        elif sent['sentiment'] == 'BEARISH' and float(price_no) < 0.5:
            opportunities.append({
                'type': 'SELL_OPPORTUNITY',
                'market': question[:80],
                'price': float(price_no),
                'sentiment': sent['sentiment'],
                'confidence': sent['confidence'],
                'action': f"BET NO at {float(price_no):.2%} (market is cheap!)"
            })

    return opportunities

def main():
    """Main execution"""
    # Check API key first
    check_api_key()

    print("🔍 Finding Trading Opportunities...\n")

    # Load markets
    markets = load_markets()
    print(f"📊 Loaded {len(markets)} markets")

    # Analyze sentiment
    print("🤖 Analyzing sentiment...")
    sentiment = analyze_sentiment(markets)
    print(f"✅ Sentiment analyzed for {len(sentiment)} markets\n")

    # Find opportunities
    opportunities = find_opportunities(markets, sentiment)

    # Display results
    if not opportunities:
        print("✨ No clear trading opportunities found.")
        print("Check sentiment vs prices for specific markets.")
        return

    print(f"🎯 Found {len(opportunities)} opportunity(ies):\n")

    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. 📈 {opp['type']}")
        print(f"   Market: {opp['market']}...")
        print(f"   Price: {opp['price']:.2%} ({opp['action']})")
        print(f"   Sentiment: {opp['sentiment']} | Confidence: {opp['confidence']}")
        print()

    # Save to file
    output_file = f"data/opportunities_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(output_file, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "opportunities": opportunities
        }) + "\n")
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    main()