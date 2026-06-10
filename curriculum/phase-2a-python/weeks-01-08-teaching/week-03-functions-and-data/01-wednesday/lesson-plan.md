# Week 3 — Functions & First Contact with Data: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Demo notebook open in Colab: `week03_wed_demo.ipynb`
- [ ] Student exercise link ready to share: `week03_wed_exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] No dataset needed today — all code uses hardcoded Olist values

---

## Learning Objectives

By the end of this session, students will be able to:
1. Write well-structured functions with parameters, defaults, and return values
2. Use docstrings for documentation
3. Handle edge cases with try/except
4. Chain functions together

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, quick Week 2 recap |
| 0:10–0:40 | Part 1 — Function Fundamentals | Demo §1–§2: `def`, docstrings, defaults |
| 0:40–1:05 | Part 2 — Multiple Return Values | Demo §3: tuples, try/except, datetime |
| 1:05–1:15 | Going Deeper + Common Mistakes | Demo §4–§5: chaining, forgetting `return` |
| 1:15–1:20 | Mini-Challenge | Students write `format_currency` (~5 min) |
| 1:20–2:00 | Group Exercise | 4-function Olist toolkit (40 min) |

---

## Key Concepts

### Function Fundamentals
Define functions with parameters, docstrings, and return values; use default parameters.

**Expected outputs:**
```
calculate_total_cost(58.90, 13.29)   → 72.19
calculate_total_cost(239.90, 19.93)  → 259.83
calculate_total_cost(199.00, 17.87)  → 216.87
classify_review(1) → Negative
classify_review(2) → Negative
classify_review(3) → Neutral
classify_review(4) → Positive
classify_review(5) → Positive
```

**Common mistake:** Forgetting `return` — the function prints but returns `None`.
Show students the difference between a function that prints and one that returns.

### Functions Returning Multiple Values
Return tuples from functions, unpack with multiple assignment, handle errors with try/except.

**Expected outputs:**
```
delivery_analysis("2017-10-02 10:56:33", "2017-10-10 21:25:13") → Days: 8, Status: Normal
delivery_analysis("2018-07-24 20:41:37", "2018-08-07 15:27:45") → Days: 13, Status: Normal
```

**Common mistake:** Students forget to unpack tuples — `days, status = function()`.
Also: using a bare `except` without understanding what error to catch.

---

## Group Exercise

## Wednesday Group Exercise: Build the Olist Toolkit

Write these 4 functions using what you have learned:

```python
# Function 1: summarise_orders(status_list, count_list)
# Takes two lists, returns a dict: {status: count}
# Test with the 8 Olist statuses and counts

# Function 2: top_n_items(data_dict, n=5)
# Takes a dict {key: numeric_value}, returns list of top n (key, value) tuples
# Test: top_n_items({"SP":41746,"RJ":12852,"MG":11635,"RS":5466,"PR":5045}, 3)
# Expected: [("SP",41746), ("RJ",12852), ("MG",11635)]

# Function 3: format_currency(amount, currency="R$")
# Returns formatted string: "R$1,234.56"
# Test: format_currency(5202955.05) → "R$5,202,955.05"

# Function 4: safe_divide(numerator, denominator, default=0.0)
# Returns numerator/denominator, returns default if denominator is 0
# Test: safe_divide(96478, 99441) → 0.9702...
# Test: safe_divide(100, 0) → 0.0
```

**Expected outputs:**
- `top_n_items({"SP":41746,"RJ":12852,"MG":11635,"RS":5466,"PR":5045}, 3)` → `[("SP",41746), ("RJ",12852), ("MG",11635)]`
- `format_currency(5202955.05)` → `"R$5,202,955.05"`
- `safe_divide(96478, 99441)` → `0.9702...`
- `safe_divide(100, 0)` → `0.0`

---

## Session Notes

- No dataset loading today — all values are hardcoded Olist numbers. This is intentional.
- Thursday is the payoff: they'll load the real 99,441-row CSV by hand and see why functions matter.
- The mini-challenge (`format_currency`) is the same function used in the group exercise — build confidence before the group work.
