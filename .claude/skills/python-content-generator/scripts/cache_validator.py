"""
Validation Cache Management

Manages validation cache file with dataset hash checking.
Cache location: .claude/cache/phase2a-validation-cache.json
"""

import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime


REPO_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
CACHE_DIR = REPO_ROOT / ".claude" / "cache"
CACHE_FILE = CACHE_DIR / "phase2a-validation-cache.json"


def compute_hash(zip_path: str) -> str:
    """Compute MD5 hash of olist-data.zip."""
    hash_md5 = hashlib.md5()
    with open(zip_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_cache() -> dict:
    """Load validation cache from file. Return empty dict if file doesn't exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not CACHE_FILE.exists():
        return {"dataset_hash": None, "timestamp": None, "weeks": {}}

    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"dataset_hash": None, "timestamp": None, "weeks": {}}


def save_cache(cache: dict) -> None:
    """Write validation cache to file."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)


def check_cache_hit(zip_path: str, week_number: int, force_validate: bool = False) -> bool:
    """
    Check if validation cache is valid for this week.

    Returns True if cache hit (use cached results).
    Returns False if cache miss or force_validate flag set.
    """
    if force_validate:
        return False

    try:
        current_hash = compute_hash(zip_path)
    except FileNotFoundError:
        return False

    cache = load_cache()
    cached_hash = cache.get("dataset_hash")

    # Hash mismatch = cache miss
    if cached_hash != current_hash:
        return False

    # Check if this week is in cache
    week_key = str(week_number)
    if week_key not in cache.get("weeks", {}):
        return False

    return True


def update_cache(zip_path: str, week_number: int, validation_results: dict) -> None:
    """
    Update cache with new validation results for a week.

    Args:
        zip_path: Path to olist-data.zip
        week_number: Week number (1-8)
        validation_results: Dict with validation results for each code cell
    """
    current_hash = compute_hash(zip_path)
    cache = load_cache()

    # Update dataset hash and timestamp
    cache["dataset_hash"] = current_hash
    cache["timestamp"] = datetime.now().isoformat()

    # Update week-specific results
    week_key = str(week_number)
    cache["weeks"][week_key] = {
        "status": "validated",
        "timestamp": datetime.now().isoformat(),
        "cells": validation_results
    }

    save_cache(cache)


def invalidate_cache() -> None:
    """Clear entire cache (e.g., if dataset changes)."""
    cache = {"dataset_hash": None, "timestamp": None, "weeks": {}}
    save_cache(cache)


if __name__ == "__main__":
    zip_path = str(REPO_ROOT / "datasets" / "phase-2-python-sql" / "olist-data.zip")

    # Test hash computation
    h = compute_hash(zip_path)
    print(f"Dataset hash: {h}")

    # Test cache operations
    cache_hit = check_cache_hit(zip_path, week_number=1)
    print(f"Cache hit for Week 1: {cache_hit}")
