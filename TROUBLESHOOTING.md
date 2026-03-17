# API Key Troubleshooting

## Issue: 401 Unauthorized Error

**Symptom:**
```
❌ Analysis error: 401 Client Error: Unauthorized for url: https://openrouter.ai/api/v1/chat/completions
```

**Cause:** The OPENROUTER_API_KEY is not set in the environment when the script runs.

---

## Quick Fix

**In your terminal:**

```bash
cd polymarket-miner
export OPENROUTER_API_KEY='your-key-here'  # Replace with actual key from openrouter.ai
./run.sh src/find_opportunities.py
```

---

## Better Option: Load from Shell

**If you already have OPENROUTER_API_KEY set in your shell:**

```bash
cd polymarket-miner

# Just run the script - it will automatically find the API key
./run.sh src/find_opportunities.py
```

**Check if it's already set:**
```bash
echo $OPENROUTER_API_KEY
```

If this shows your key, you don't need to set it again.

---

## What is OPENROUTER_API_KEY?

It's the key you use to access OpenRouter's API.
- Get it free from: [https://openrouter.ai/](https://openrouter.ai/)
- Format: `sk-or-v1-xxxxx...`
- Free to use for small projects

---

## Common Issues

### 1. Key not set in current shell
```bash
# Wrong
cd polymarket-miner
./run.sh src/find_opportunities.py
# ❌ Error: 401 Unauthorized

# Right
export OPENROUTER_API_KEY='your-key-here'
./run.sh src/find_opportunities.py
# ✅ Works!
```

### 2. Key set in different shell
```bash
# If you set it in .zshrc but not in current shell:
source ~/.zshrc
export OPENROUTER_API_KEY  # Load from config
./run.sh src/find_opportunities.py
```

### 3. Key is wrong or expired
```bash
# Check your key:
echo $OPENROUTER_API_KEY

# If it's missing or wrong:
export OPENROUTER_API_KEY='correct-key-here'
./run.sh src/find_opportunities.py
```

---

## Persistent Setup

**To avoid setting it every time:**

Add to `~/.zshrc`:
```bash
export OPENROUTER_API_KEY='your-key-here'
```

Then restart your terminal or run:
```bash
source ~/.zshrc
```

Now the key will be available in all new shell sessions.

---

## Running from Different Terminals

**New terminal:**
```bash
cd polymarket-miner
source venv/bin/activate  # Important!
export OPENROUTER_API_KEY='your-key-here'
python3 src/find_opportunities.py
```

---

## Verify API Key is Working

Test it manually:
```bash
cd polymarket-miner
source venv/bin/activate
python3 debug_key.py
```

This will tell you:
- Is the API key found?
- Is the key format correct?
- Is the API working?

If it says "NOT SET", you need to set it with:
```bash
export OPENROUTER_API_KEY='your-key-here'
```

---

## Solution Summary

1. **Check if API key is set:**
   ```bash
   echo $OPENROUTER_API_KEY
   ```

2. **If it shows your key:**
   ```bash
   cd polymarket-miner
   ./run.sh src/find_opportunities.py
   ```

3. **If it doesn't show:**
   ```bash
   export OPENROUTER_API_KEY='your-key-here'
   cd polymarket-miner
   ./run.sh src/find_opportunities.py
   ```

---

## Using Without run.sh (Alternative)

If run.sh is giving you issues:

```bash
cd polymarket-miner
source venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
python3 src/find_opportunities.py
```

This is the manual way but it always works.