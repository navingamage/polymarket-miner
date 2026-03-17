import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load the latest analysis
latest_analysis_file = "data/analysis-2026-03-17.jsonl"

with open(latest_analysis_file, "r") as f:
    entry = json.loads(f.readlines()[-1])

markets = entry['analysis']

# Extract sentiment data
sentiments = [m['sentiment'] for m in markets]
confidences = [m['confidence'] for m in markets]

# Count sentiment frequencies
sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}

# Create chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Sentiment Breakdown (Pie Chart)
colors = {'BULLISH': '#22c55e', 'BEARISH': '#ef4444', 'NEUTRAL': '#f59e0b'}
pie_colors = [colors.get(s, '#94a3b8') for s in sentiments]

ax1.pie(sentiment_counts.values(), labels=sentiment_counts.keys(),
        autopct='%1.1f%%', colors=[colors[s] for s in sentiment_counts.keys()], startangle=90)
ax1.set_title('Market Sentiment Distribution', fontweight='bold')

# Chart 2: Sentiment by Market (Bar Chart)
market_names = [m['question'][:30] + "..." for m in markets]
x = range(len(markets))
ax2.bar(x, [colors[s] for s in sentiments], color=[colors[s] for s in sentiments])
ax2.set_xticks(x)
ax2.set_xticklabels(market_names, rotation=45, ha='right', fontsize=8)
ax2.set_title('Sentiment by Market', fontweight='bold')
ax2.set_ylabel('Sentiment', rotation=0, labelpad=40)

plt.tight_layout()
plt.savefig('data/sentiment_chart.png', dpi=150, bbox_inches='tight')
print(f"✅ Chart saved to: data/sentiment_chart.png")

# Save sentiment frequencies as JSON
freq_file = "data/sentiment_frequencies.json"
with open(freq_file, 'w') as f:
    json.dump({k: v for k, v in sentiment_counts.items()}, f, indent=2)
print(f"✅ Sentiment frequencies saved to: {freq_file}")

# Print summary
print(f"\n📊 Analysis Summary ({entry['analyzed_count']} markets):")
print(f"  BULLISH: {sentiment_counts.get('BULLISH', 0)} markets")
print(f"  BEARISH: {sentiment_counts.get('BEARISH', 0)} markets")
print(f"  NEUTRAL: {sentiment_counts.get('NEUTRAL', 0)} markets")