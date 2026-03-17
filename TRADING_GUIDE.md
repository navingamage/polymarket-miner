---
# Trading Analysis Quick Start Guide
# Use this guide to manually trade based on sentiment analysis

## How to Use the Opportunity Finder

### Step 1: Run the Opportunity Finder
```bash
cd polymarket-miner
source venv/bin/activate
export OPENROUTER_API_KEY
python3 src/find_opportunities.py
```

This will:
- ✅ Fetch latest markets
- ✅ Analyze sentiment (using rate limiting)
- ✅ Find BUY/SELL opportunities where market price ≠ crowd sentiment
- ✅ Save opportunities to `data/opportunities-YYYY-MM-DD.jsonl`

### Step 2: Review the Opportunities
Look at the output:
```
1. 📈 BUY_OPPORTUNITY
   Market: Will Bitcoin reach $100k by end of year?
   Price: 35.00% (BET YES at 35.00% - market is cheap!)
   Sentiment: BULLISH | Confidence: high
```

**What this means:**
- Crowd sentiment says "YES" (bullish)
- Market price is only 35% (actually, this would be a BEARISH opportunity - the market is too low for BULLISH)
- Correction: Actually, if price is 35% and sentiment is BULLISH, the market IS cheap → BUY opportunity

### Step 3: Place Trades Manually
1. Go to Polymarket website/app
2. Search for the market
3. Place your bet based on the recommendation

**Example:**
```
If opportunity says: "BET YES at 40%"
→ Place YES bet at 40% (buy low)
```

### Step 4: Track Your Results
Check the saved JSONL file:
```bash
cat data/opportunities-2026-03-17.jsonl
```

---

## Understanding the Logic

### When to BUY (Long the Crowd)
```
✅ GOOD BUY: Price < 40% AND Sentiment = BULLISH
   → Crowd thinks it will happen, but market price is cheap
   → You're betting with the crowd at a discount

❌ BAD BUY: Price > 60% AND Sentiment = BULLISH
   → Crowd thinks it will happen, but market is overpriced
   → This is a BEARISH opportunity (sell high)
```

### When to SELL (Short the Crowd)
```
✅ GOOD SELL: Price > 60% AND Sentiment = BEARISH
   → Crowd thinks it won't happen, but market is overpriced
   → You're betting against the crowd at a premium

❌ BAD SELL: Price < 40% AND Sentiment = BEARISH
   → Crowd thinks it won't happen, but market is cheap
   → This is a BUY opportunity (buy low)
```

---

## Risk Management

### Only Trade What You Can Afford to Lose
- Start with small amounts (5-10% of trading capital)
- Never risk more than 1-2% per trade

### Example: $100 Budget
```
Position size = $100 × 0.05 = $5 per trade
```

### Filter by Confidence
- Only act on "high" confidence opportunities (ignore "medium" for now)
- You'll get better results by being selective

---

## Limitations to Know

### 1. LLM Bias
The sentiment analysis comes from an AI that may have its own worldview:
- ✅ Can detect general trends
- ❌ May misinterpret specific nuances
- ❌ Doesn't know about today's breaking news

### 2. Timing Lag
Your data is 10-30 minutes old:
- Market prices are current
- Sentiment analysis takes time

### 3. Market Liquidity
Some markets have low volume:
- Prices can be manipulated
- Betting opportunities exist but are riskier

---

## Monitoring & Iteration

### Check Daily
Run `find_opportunities.py` every day to see new opportunities

### Track Your Performance
Record your wins/losses:
```json
{
  "date": "2026-03-17",
  "opportunity_id": 1,
  "market": "Bitcoin $100k",
  "bet": "YES",
  "price_entered": 0.40,
  "price_exited": 0.45,
  "result": "WIN (+12.5%)"
}
```

### Adjust Strategy
If you're losing money, adjust:
- Change confidence threshold (more or less strict)
- Add additional filters (volume, liquidity)
- Only trade on "high" confidence opportunities

---

## Example Trading Session

### 1. Run Opportunity Finder
```bash
python3 src/find_opportunities.py
```

Output:
```
🎯 Found 3 opportunity(ies):

1. 📈 BUY_OPPORTUNITY
   Market: Will BTC hit $100k by end of year?
   Price: 35.00% (BET YES at 35.00%)
   Sentiment: BULLISH | Confidence: high
```

### 2. Evaluate
- Is this news/relevant?
- Do you agree with the market?
- What's the potential upside/downside?

### 3. Place Bet
- Go to Polymarket → Search "BTC $100k"
- Place YES bet at 35%
- Bet amount: $5 (5% of $100 budget)

### 4. Monitor
- Check the market periodically
- If price rises to 45%, exit with profit
- If price falls below 25%, exit with loss (cut losses)

---

## Next Steps

1. ✅ Run `find_opportunities.py` today
2. ✅ Review the opportunities
3. ✅ Start with 1-2 small trades
4. ✅ Track your results
5. ✅ Iterate and improve

**Remember:** This is NOT financial advice. Betting involves risk. Start small and learn!