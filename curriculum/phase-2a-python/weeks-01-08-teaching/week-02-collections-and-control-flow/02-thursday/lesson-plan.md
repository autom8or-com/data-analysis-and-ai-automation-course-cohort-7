# Week 2 — Collections & Control Flow: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Demo notebook open in Colab: `week-02-thu-demo.ipynb`
- [ ] Student exercise link ready to share: `week-02-thu-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] Olist data not required this week (Week 2 uses hardcoded values)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Create and manipulate dictionaries
2. Use if/elif/else for business logic
3. Combine loops with conditionals
4. Nest dictionaries for structured data

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Recap Wednesday: lists, loops, comprehensions |
| 0:10–0:45 | Dictionaries (35 min) | Demo: basic access, nested dicts, iteration |
| 0:45–1:20 | Conditionals (35 min) | Demo: classify_delivery, classify_order_value, combining loops + conditionals |
| 1:20–2:00 | Group Exercise (40 min) | Build a status summary dict from scratch |

---

## Key Concepts

### Dictionaries
Key-value stores for structured data. One dict = one row. Keys are field names, values are field values. Core operations: `dict["key"]`, `dict.get("key", default)`, `dict["key"] = value`, `for k, v in dict.items()`.

Expected outputs from the demo:
- `order["status"]` → `delivered`
- `order.get("seller", "unknown")` → `unknown`
- `order["total"]` = 58.90 + 13.29 → `72.19`
- `state_summary["SP"]["orders"]` → `41746`
- `state_summary["SP"]["revenue"]` → `5202955.05`

Common mistake: `KeyError` when accessing a missing key — always use `.get()` for optional fields.

### Nested Dictionaries
Dict values can themselves be dicts. Access with two keys: `state_summary["SP"]["revenue"]`. Each outer key is like a row identifier; inner dict holds columns.

Expected outputs:
- State loop: `SP: 41,746 orders | R$5.2M revenue`, `RJ: 12,852 orders | R$1.8M revenue`, `MG: 11,635 orders | R$1.6M revenue`

### Conditionals
`if/elif/else` for business classification logic. Most restrictive condition first.

Expected outputs from `classify_delivery()`:
- 0, 5 days → `Fast` | 10 days → `Normal` | 20 days → `Slow` | 50 days → `Very Slow` | None → `Unknown`

Expected outputs from `classify_order_value()` (avg R$120.65, max R$6,735.00):
- R$58.90 → `Economy` | R$120.65 → `Standard` | R$500.00, R$6735.00 → `Premium`

Common mistake: stacking `if/if` instead of `if/elif` causes double-counting.

### Combining Loops with Conditionals
Loop over data, apply classifier, accumulate results. Foundation of all row-level data processing.

Expected outputs for sample_prices:
- `Economy: 4, Standard: 4, Premium: 2`

---

## Group Exercise

```python
# Build a status summary dict from scratch
statuses = ["delivered", "shipped", "canceled", "unavailable",
            "invoiced", "processing", "created", "approved"]
counts = [96478, 1107, 625, 609, 314, 301, 5, 2]

# Task 1: Create a dict mapping status → count
# Expected: {"delivered": 96478, "shipped": 1107, ...}

# Task 2: Using a loop, print only statuses where count > 500
# Expected: delivered (96478), shipped (1107), canceled (625), unavailable (609)

# Task 3: Write a function classify_status(status) that returns:
# "Active" if status in ["delivered", "shipped", "invoiced", "processing"]
# "Problem" if status in ["canceled", "unavailable"]
# "Other" otherwise

# Task 4: Create a nested dict: {"delivered": {"count": 96478, "pct": 97.0}, ...}
```

**Expected outputs**: status_dict["delivered"] = 96478 | 4 statuses with count > 500 | nested dict with count + pct for all 8 statuses

---

## Weekly Assignment

Submit `week2_assignment.ipynb`:

1. Create a dictionary representing 3 Olist orders (make up order_ids but use realistic prices from R$20–R$500). Include: order_id, city, state, price, freight, review_score.

2. Write a function `order_report(order_dict)` that calculates total cost and returns a formatted string.

3. Using `review_scores = [5, 4, 1, 5, 3, 2, 5, 4, 5, 1]`: count positives/neutrals/negatives both with a loop and with a list comprehension. Expected: positive=6, neutral=1, negative=3.

4. Write `top_states(state_dict, n)` — returns top n states by order count. Test: `top_states({"SP": 41746, "RJ": 12852, "MG": 11635, "RS": 5466, "PR": 5045}, 3)` → `[("SP", 41746), ("RJ", 12852), ("MG", 11635)]`

---

## Notes

- No AI assistance this week (Weeks 1–3 are no-AI)
- Next week: Functions & First Contact with Data — students write reusable functions and load their first CSV
