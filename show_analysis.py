import json

with open("data/analysis-2026-03-17.jsonl", "r") as f:
    entry = json.loads(f.readlines()[-1])

print(f"📊 Analysis Report")
print(f"=" * 50)
print(f"Timestamp: {entry['timestamp']}")
print(f"Markets analyzed: {entry['analyzed_count']}")
print(f"\nSentiment breakdown:")
bullish = sum(1 for e in entry['analysis'] if e.get('sentiment') == 'BULLISH')
bearish = sum(1 for e in entry['analysis'] if e.get('sentiment') == 'BEARISH')
neutral = sum(1 for e in entry['analysis'] if e.get('sentiment') == 'NEUTRAL')
print(f"  BULLISH: {bullish}")
print(f"  BEARISH: {bearish}")
print(f"  NEUTRAL: {neutral}")
print(f"\nDetailed analysis:")
for i, item in enumerate(entry['analysis'], 1):
    question = item.get('question', 'N/A')[:60]
    sentiment = item.get('sentiment', 'N/A')
    confidence = item.get('confidence', 'N/A')
    print(f"{i}. {question}...")
    print(f"   Sentiment: {sentiment} | Confidence: {confidence}")