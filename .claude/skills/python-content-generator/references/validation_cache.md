# Validation Cache Strategy

## Motivation

Olist dataset (99,441 rows) doesn't change. Validating every week's code cells against the full dataset is slow (~30 seconds per week). Caching makes subsequent runs instant.

## Cache Mechanism

**File location:** `.claude/cache/phase2a-validation-cache.json` (project-level, gitignored — each machine builds its own cache)

**Strategy:**
1. Compute MD5 hash of `olist-data.zip`
2. Load cache; check if hash matches + week is cached
3. **Cache hit**: Return cached results immediately
4. **Cache miss**: Load data, execute cells, validate, update cache
5. **force_validate flag**: Override cache, re-validate regardless

## Cache File Structure

```json
{
  "dataset_hash": "a1b2c3d4e5f6g7h8i9j0...",
  "timestamp": "2026-04-26T10:30:00.123456",
  "weeks": {
    "1": {
      "status": "validated",
      "timestamp": "2026-04-25T09:15:00.123456",
      "cells": {
        "cell_1": {
          "status": "pass",
          "expected": "72.19",
          "actual": "72.19",
          "error": null
        }
      }
    }
  }
}
```

## Performance

- **Cache hit**: ~0.1 seconds (file I/O only)
- **Cache miss**: ~30 seconds (full dataset load + cell execution)
- **Typical workflow**: Week 1–8 → 1st run ~4 min, 2nd run ~0.8 sec
