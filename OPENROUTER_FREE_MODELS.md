# OpenRouter Free Models Guide

## 🆓 Current Status

**Your OpenRouter API Key**: ✅ Configured and Working  
**Current Model**: `openrouter/free` (Auto-router)  
**Test Result**: ✅ Successfully generated script

---

## 📊 Rate Limits (All Free Models)

| Credits Purchased (lifetime) | Requests / Minute | Requests / Day |
|------------------------------|-------------------|----------------|
| Less than $10                | 20                | **50**         |
| $10 or more                  | 20                | **1,000**      |

**Note**: Limits are account-wide. To get 1,000 requests/day, just purchase $10 in credits once (you don't have to spend them).

---

## 🎯 RECOMMENDED FREE MODELS

### For Script Generation (Best to Worst)

1. **`openrouter/free`** ⭐ **RECOMMENDED**
   - Auto-selects best available free model
   - Smart filtering (supports your requirements)
   - Fastest and most reliable
   - **Currently configured in your project**

2. **`meta-llama/llama-3.3-70b-instruct:free`**
   - 70B parameters, high quality
   - Good speed
   - ⚠️ Deprecating July 19, 2026

3. **`nvidia/nemotron-3-super-120b-a12b:free`**
   - 120B MoE (12B active)
   - Great for creative tasks
   - Good balance of quality/speed

4. **`nvidia/nemotron-3-ultra-550b-a55b:free`**
   - Largest model (550B MoE)
   - Best quality
   - ⚠️ VERY SLOW (60+ seconds)

5. **`poolside/laguna-m.1:free`**
   - Best for coding tasks
   - Highest token volume
   - Good general purpose

---

## 📋 COMPLETE LIST OF FREE MODELS (21 Total)

### General Purpose / Reasoning (10 models)

| Model ID | Context | Active Params | Notes |
|----------|---------|---------------|-------|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 1M | 55B/550B | Largest, slowest |
| `nvidia/nemotron-3-super-120b-a12b:free` | 262K | 12B/120B | Multi-agent apps |
| `tencent/hy3:free` | 262K | 21B/295B | ⚠️ Dep. July 2026 |
| `qwen/qwen3-next-80b-a3b-instruct:free` | 262K | 3B/80B | Multilingual |
| `openai/gpt-oss-20b:free` | 131K | 3.6B/21B | Apache 2.0 |
| `meta-llama/llama-3.3-70b-instruct:free` | 65K | 70B | ⚠️ Dep. July 2026 |
| `meta-llama/llama-3.2-3b-instruct:free` | 131K | 3B | Smallest |
| `nvidia/nemotron-nano-9b-v2:free` | 128K | 9B | Unified reasoning |
| `nvidia/nemotron-3-nano-30b-a3b:free` | 256K | 3B/30B | High efficiency |
| `nousresearch/hermes-3-llama-3.1-405b:free` | 131K | 405B | ⚠️ Dep. July 2026 |

### Coding (4 models)

| Model ID | Context | Active Params | Notes |
|----------|---------|---------------|-------|
| `qwen/qwen3-coder:free` | 262K | 35B/480B | ⚠️ Dep. July 2026 |
| `poolside/laguna-m.1:free` | 262K | Flagship | Highest usage |
| `poolside/laguna-xs-2.1:free` | 262K | 3B/33B | Compact |
| `cohere/north-mini-code:free` | 256K | 3B/30B | Content moderation |

### Multimodal (Vision/Video/Audio) (4 models)

| Model ID | Modalities | Active Params | Notes |
|----------|-----------|---------------|-------|
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Text + Image + Audio + Video | 3B/30B | Most versatile |
| `nvidia/nemotron-nano-12b-v2-vl:free` | Text + Image + Video | 12B | Video understanding |
| `google/gemma-4-31b-it:free` | Text + Image + Video | 31B | Function calling |
| `google/gemma-4-26b-a4b-it:free` | Text + Image + Video | 4B/26B | Near-31B quality |

### Specialized (2 models)

| Model ID | Purpose | Params |
|----------|---------|--------|
| `nvidia/nemotron-3.5-content-safety:free` | Content moderation | 4B |
| `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` | Uncensored chat | 24B |

### Router (1 model)

| Model ID | Purpose |
|----------|---------|
| `openrouter/free` | Auto-routes to best free model |

---

## 🔄 HOW TO CHANGE MODELS

### Option 1: Edit config.py (Permanent)

```python
# In config.py, change this line:
OPENROUTER_MODEL = "your-model-choice"

# Examples:
OPENROUTER_MODEL = "openrouter/free"  # Auto-router (current)
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"  # Fast
OPENROUTER_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"  # Better
```

### Option 2: Command Line (Temporary)

```bash
# Use --provider openrouter to use OpenRouter
python pipeline.py --prompt "Your topic" --provider openrouter

# Or stick with Groq (faster, also free)
python pipeline.py --prompt "Your topic" --provider groq
```

---

## ⚖️ GROQ vs OPENROUTER

### Groq (Current Primary)
- ✅ **Faster**: 5-10 seconds per script
- ✅ **Higher quality**: Llama 3.3 70B Versatile
- ✅ **Free tier**: Generous limits
- ✅ **Your choice**: Currently configured as default

### OpenRouter (Current Alternative)
- ✅ **More options**: 21 free models
- ✅ **Auto-router**: Smart model selection
- ⚠️ **Slower**: 10-15 seconds per script
- ✅ **Backup**: Good fallback if Groq limits hit

### Recommendation
**Keep current setup**:
- Primary: Groq (`groq`)
- Alternative: OpenRouter (`openrouter`)
- Switch with: `--provider openrouter`

---

## 🔮 DEPRECATION SCHEDULE

Models being removed around July 19-21, 2026:
- `tencent/hy3:free`
- `qwen/qwen3-coder:free`
- `cognitivecomputations/dolphin-mistral-24b-venice-edition:free`
- `meta-llama/llama-3.3-70b-instruct:free`
- `meta-llama/llama-3.2-3b-instruct:free`
- `nousresearch/hermes-3-llama-3.1-405b:free`

**Action**: No action needed, you're using `openrouter/free` auto-router which will automatically switch to new models.

---

## 💡 TIPS

1. **Use `openrouter/free`** - Easiest and most reliable
2. **Purchase $10 credits** - Bumps daily limit from 50 to 1,000 requests (one-time)
3. **Don't use Ultra model** - Way too slow for script generation
4. **Stick with Groq for speed** - Switch to OpenRouter only if needed

---

## 📝 EXAMPLE USAGE

```bash
# Current default (Groq - fast)
python script_gen.py --prompt "Your topic"

# Switch to OpenRouter (auto-selects free model)
python script_gen.py --prompt "Your topic" --provider openrouter

# Or run full pipeline with OpenRouter
python pipeline.py --prompt "Your topic" --provider openrouter
```

---

## ✅ YOUR CURRENT SETUP

```
Primary LLM: Groq (Llama 3.3 70B Versatile)
├─ Speed: ⚡⚡⚡ Fast (5-10s)
├─ Quality: ⭐⭐⭐⭐⭐ Excellent
└─ Status: ✅ Working

Backup LLM: OpenRouter (openrouter/free)
├─ Speed: ⚡⚡ Good (10-15s)
├─ Quality: ⭐⭐⭐⭐ Good-Excellent (auto-selected)
└─ Status: ✅ Working
```

**Recommendation**: Keep using Groq as primary. Perfect setup! 🎯
