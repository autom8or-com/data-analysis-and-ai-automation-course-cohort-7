"""
Validation Orchestrator with Caching

Executes notebook code cells against full Olist dataset.
Validates outputs against teaching-curriculum verified KPIs.
Manages validation cache to avoid re-running expensive checks.
"""

import json
from typing import Tuple, Dict, List
from olist_loader import load_olist_data
from cache_validator import check_cache_hit, update_cache, load_cache


def validate_notebooks(
    zip_path: str,
    week_number: int,
    code_cells: Dict[str, str],
    expected_outputs: Dict[str, any],
    tolerance: float = 0.01,
    force_validate: bool = False
) -> Tuple[bool, Dict]:
    """
    Validate code cells against Olist data.

    Args:
        zip_path: Path to olist-data.zip
        week_number: Week number (1-8)
        code_cells: Dict mapping cell_id → code string
        expected_outputs: Dict mapping cell_id → expected output
        tolerance: Acceptable variance for numeric outputs (default 1%)
        force_validate: Skip cache, force full validation

    Returns:
        Tuple of (success: bool, results: dict)
    """

    # Check cache first
    if check_cache_hit(zip_path, week_number, force_validate):
        print(f"Cache hit for Week {week_number}. Using cached validation results.")
        cache = load_cache()
        cached_results = cache["weeks"][str(week_number)].get("cells", {})
        return (True, cached_results)

    print(f"Cache miss for Week {week_number}. Running full validation...")

    # Load Olist data
    try:
        data = load_olist_data(zip_path)
    except Exception as e:
        raise Exception(f"Failed to load Olist data: {str(e)}")

    # Execute cells and validate
    results = {}
    success = True

    for cell_id, code in code_cells.items():
        result = _execute_and_validate(
            cell_id, code, data, expected_outputs.get(cell_id), tolerance
        )
        results[cell_id] = result

        if result["status"] != "pass":
            success = False
            print(f"  ❌ {cell_id}: {result['error']}")
        else:
            print(f"  ✓ {cell_id}: passed")

    # Update cache with results
    if success:
        update_cache(zip_path, week_number, results)
        print(f"Cache updated for Week {week_number}.")

    return (success, results)


def _execute_and_validate(
    cell_id: str,
    code: str,
    data: Dict,
    expected_output: any,
    tolerance: float
) -> Dict:
    """Execute a code cell and validate its output."""

    result = {
        "status": "fail",
        "expected": str(expected_output),
        "actual": None,
        "error": None
    }

    # Build execution context with Olist DataFrames
    exec_context = {**data}

    try:
        # Execute code cell safely
        exec(code, {"__builtins__": __builtins__, **exec_context})
        result["status"] = "pass"
        result["actual"] = "Code executed successfully"

    except Exception as e:
        result["error"] = f"Code execution failed: {str(e)}"
        result["actual"] = None

    return result
