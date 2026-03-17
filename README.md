# Polymarket Miner

A tool to analyze sentiment in Polymarket prediction markets and find trading opportunities.

## Features

- 📡 Fetch fresh markets from Polymarket (active & open)
- 🤖 Analyze sentiment (BULLISH/BEARISH/NEUTRAL) using AI
- 🔍 Find trading opportunities by comparing sentiment vs market price
- 📊 Rate limiting to prevent API blocking
- 💾 Store all analysis in `data/` folder

## Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
export OPENROUTER_API_KEY='your-key-here'
```

## Usage

### 1. Fetch Markets
```bash
# Get latest markets
python3 src/main.py --tag crypto --limit 20

# Get markets from different categories
python3 src/main.py --tag politics --limit 20
python3 src/main.py --tag sports --limit 20
```

### 2. Analyze Sentiment
```bash
# Analyze the latest markets
python3 src/analysis.py

# View results
ls data/
```

### 3. Find Trading Opportunities
```bash
# Find where sentiment diverges from market price
python3 src/find_opportunities.py

# Check saved opportunities
cat data/opportunities-2026-03-17.jsonl
```

### 4. View Market Data
```bash
# Show recent market snapshots
python3 src/view_data.py
```

## Project Structure

```
polymarket-miner/
├── src/
│   ├── main.py          # Fetch markets
│   ├── analysis.py      # Analyze sentiment
│   ├── find_opportunities.py  # Find trading opportunities
│   ├── view_data.py     # View data
│   └── rate_limiter.py  # Prevent API blocking
├── data/
│   ├── markets-*.jsonl  # Raw market data
│   ├── analysis-*.jsonl # Sentiment analysis
│   ├── opportunities-*.jsonl  # Trading opportunities
│   └── .gitkeep
├── venv/               # Virtual environment
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Scripts

### Core Scripts
- `src/main.py` - Fetch market data from Polymarket API
- `src/analysis.py` - Analyze sentiment using OpenRouter API
- `src/find_opportunities.py` - Find trading opportunities
- `src/view_data.py` - Display stored market data
- `src/rate_limiter.py` - Utility to prevent API blocking

### Configuration
Edit in `src/analysis.py`:
- `LINES_TO_ANALYZE` - Number of markets to analyze (default: 5)
- `MODEL_ID` - Model to use for analysis (default: `z-ai/glm-4.7-flash`)

## Data Sources

**Primary:** Polymarket Gamma API (`https://gamma-api.polymarket.com/markets`)
- Official public API, not scraping
- Real-time market prices

**Secondary:** OpenRouter GLM-4.7 Model
- Analyzes market questions into sentiment
- Note: AI has bias and no live news access
- Verify opportunities with your own knowledge

## Getting Started

1. Run `python3 src/find_opportunities.py` to find opportunities
2. Review opportunities and evaluate with your own judgment
3. Start small (5-10% of budget per trade)
4. Track results and iterate

## Automation

Set up a cron job to run daily:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 8:00 AM)
0 8 * * * /path/to/polymarket-miner/automate.sh >> /path/to/polymarket-miner/logs/automate.log 2>&1
```

## Cost Estimation

- **API Cost:** ~2000 tokens per analysis (~$0.02)
- **Daily:** ~$0.05 (if running once daily)
- **Monthly:** ~$1.50 (if running once daily)

## Resources

- [TRADING_GUIDE.md](TRADING_GUIDE.md) - Manual trading strategy
- [DATA_ACCURACY.md](DATA_ACCURACY.md) - Data sources and limitations
- [SETUP.md](SETUP.md) - Full setup and automation guide

## Important Notes

⚠️ **NOT financial advice** - This tool helps identify opportunities but doesn't guarantee profit. Start small, track results, and only risk capital you can afford to lose.

- Data accuracy: Market prices 100%, sentiment analysis medium
- Blocking risk: LOW (rate limiters built-in)
- Start with $100 budget → $5 per trade max
- Verify opportunities with your own knowledge
- Cut losses quickly if price moves against you

## License

MIT