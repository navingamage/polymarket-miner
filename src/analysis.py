import requests
import json
from datetime import datetime
import os

# Configuration
# Use the most recent market log file
import os
import glob
market_files = glob.glob("data/markets-*.jsonl")
MARKETS_FILE = sorted(market_files)[-1] if market_files else "data/markets.jsonl"
OUTPUT_DIR = "data"
LINES_TO_ANALYZE = 5  # Reduced from 10 for better API compliance

# OpenRouter Configuration
MODEL_ID = "z-ai/glm-4.7-flash"
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
            # Parse the entries (each entry is a timestamp + markets list)
            entries_data = [json.loads(line) for line in lines]

        # Extract the markets list from the first entry
        if not entries_data:
            print(f"❌ No data found in {MARKETS_FILE}")
            return

        markets_list = entries_data[0].get('markets', [])

    except FileNotFoundError:
        print(f"❌ No market data found in {MARKETS_FILE}")
        return

    print(f"📊 Analyzing {len(markets_list)} markets from {MARKETS_FILE}...")

    # Prepare batch for analysis
    market_questions_list = []
    for i, market in enumerate(markets_list):
        question = market.get('question', 'N/A')
        # Escape any curly braces to prevent formatting errors
        question = question.replace('{', '{{').replace('}', '}}')
        market_questions_list.append(f"{i+1}. {question}")

    market_questions = "\n\n".join(market_questions_list)

    prompt_lines = [
        "Act as a professional trading analyst. Analyze the following Polymarket questions.",
        "For each question, determine if the market outcome is:",
        "- BULLISH (market expects YES to happen)",
        "- BEARISH (market expects NO to happen)",
        "- NEUTRAL (uncertain or event-based)",
        "",
        "Respond ONLY as a valid JSON list. Do not add extra text.",
        "",
        "Format: [{'question': '...', 'sentiment': 'BULLISH', 'confidence': 'high'}]",
        "",
        "Questions to analyze:",
        market_questions
    ]
    prompt = "\n".join(prompt_lines)

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
            "temperature": 0.1,  # Low temperature for more deterministic, factual answers
            "max_tokens": 5000  # Allow enough tokens for JSON output
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        # Parse the response content
        analysis_text = result['choices'][0]['message']['content']

        # Debug: print response if JSON parsing fails
        if not analysis_text or analysis_text.strip() == "":
            print(f"❌ Empty response from API")
            print(f"Response: {result}")
            return

        # Strip markdown code blocks if present
        analysis_text = analysis_text.strip()
        if analysis_text.startswith("```json"):
            analysis_text = analysis_text[7:]  # Remove ```json
        elif analysis_text.startswith("```"):
            analysis_text = analysis_text[3:]  # Remove ```
        if analysis_text.endswith("```"):
            analysis_text = analysis_text[:-3]  # Remove trailing ```
        analysis_text = analysis_text.strip()

        try:
            analysis_data = json.loads(analysis_text)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response")
            print(f"Response text (first 500 chars): {analysis_text[:500]}")
            print(f"JSON error: {e}")
            return

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