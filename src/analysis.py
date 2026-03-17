import requests
import json
from datetime import datetime
import os

# Configuration
MARKETS_FILE = "data/markets.jsonl"
OUTPUT_DIR = "data"
LINES_TO_ANALYZE = 10  # Analyze latest N markets

# OpenRouter Configuration
# Using the generic GLM-4.7-Flash model ID
MODEL_ID = "openrouter/z-ai/glm-4.7-flash"
API_KEY = os.environ.get("OPENROUTER_API_KEY")

def analyze_markets():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(OUTPUT_DIR, f"analysis-{timestamp}.jsonl")

    # Get today's markets from the log
    try:
        with open(MARKETS_FILE, "r") as f:
            # Read the last N entries
            lines = f.readlines()[-LINES_TO_ANALYZE:]
            entries = [json.loads(line) for line in lines]
    except FileNotFoundError:
        print(f"❌ No market data found in {MARKETS_FILE}")
        return

    print(f"📊 Analyzing {len(entries)} markets from {MARKETS_FILE}...")

    # Prepare batch for analysis
    # We send all markets in one prompt to save on API calls (efficient)
    market_questions = "\n\n".join([
        f"{i+1}. {entry['question']}"
        for i, entry in enumerate(entries)
    ])

    prompt = f"""
    Act as a professional trading analyst. Analyze the following Polymarket questions.
    For each question, determine if the market outcome is:
    - BULLISH (market expects YES to happen)
    - BEARISH (market expects NO to happen)
    - NEUTRAL (uncertain or event-based)
    
    Respond ONLY as a valid JSON list. Do not add extra text.
    
    Format: [{"question": "...", "sentiment": "BULLISH", "confidence": "high"}]
    
    Questions to analyze:
    {market_questions}
    """

    try:
        # Call OpenRouter API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are a trading sentiment analyzer. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1  # Low temperature for more deterministic, factual answers
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Parse the response content
        analysis_text = result['choices'][0]['message']['content']
        analysis_data = json.loads(analysis_text)

        # Write analysis to output file
        with open(output_file, "a") as f:
            analysis_entry = {
                "timestamp": datetime.now().isoformat(),
                "analyzed_count": len(analysis_data),
                "analysis": analysis_data
            }
            f.write(json.dumps(analysis_entry) + "\n")

        print(f"✅ Analysis complete. Saved to: {output_file}")
        print(f"   - Analyzed {len(analysis_data)} markets.")
        print(f"   - Costs approx. {response.json()['usage']['total_tokens']} tokens.")

    except Exception as e:
        print(f"❌ Error analyzing markets: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ Error: OPENROUTER_API_KEY not set in environment.")
        print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
    else:
        analyze_markets()