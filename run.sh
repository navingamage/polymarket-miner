#!/bin/bash
# Wrapper script for Polymarket Miner
# Use this to run scripts with the correct environment setup

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Ensure API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  Warning: OPENROUTER_API_KEY not set"
    echo "Please set it: export OPENROUTER_API_KEY='your-key-here'"
    exit 1
fi

# Execute the script
python3 "$@"