#!/bin/bash
# Daily Polymarket Miner Automation
# Run: crontab -e to add this line (0 8 * * * /path/to/automate.sh)

# Set up paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment and set API key
source venv/bin/activate
export OPENROUTER_API_KEY

echo "=== Polymarket Miner Job ($(date)) ==="

# Fetch markets (alternating tags for variety)
TAGS=("crypto" "politics" "sports" "tech")
TAG="${TAGS[$RANDOM % ${#TAGS[@]}]}"

echo "Fetching markets with tag: $TAG"
python3 src/main.py --tag "$TAG" --limit 20

echo "Analyzing markets"
python3 src/analysis.py

echo "Job completed at $(date)"
echo "============================"