# Week 2 — Collections & Control Flow: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Demo notebook open in Colab: `week-02-wed-demo.ipynb`
- [ ] Student exercise link ready to share: `week-02-wed-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] Olist data not required this week (Week 2 uses hardcoded values)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Create and manipulate lists
2. Use for loops and `range()`
3. Apply list comprehensions for simple transformations
4. Understand tuples and when to use them

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, recap Week 1 variables/strings |
| 0:10–0:45 | Lists (35 min) | Demo: creation, indexing, slicing, modification, aggregations |
| 0:45–1:20 | For Loops (35 min) | Demo: `zip()`, `range()`, `enumerate()` with Olist status data |
| 1:20–1:40 | List Comprehensions (20 min) | Demo: filter and transform in one line |
| 1:40–2:00 | Group Exercise (20 min intro) | Payment type analysis — full 30-min exercise may spill to start of next session |

---

## Key Concepts

### Lists
Ordered, mutable sequences for storing multiple values. Think of a spreadsheet column — all 8 order statuses together, all 8 counts together. Key operations: `len()`, indexing, slicing, `.append()`, `.insert()`, `.remove()`, `sum()`, `max()`, `min()`, `.count()`.

Expected outputs from the demo:
- `len(statuses)` → `8`
- `statuses[0]` → `delivered`
- `statuses[-1]` → `approved`
- `statuses[:3]` → `['delivered', 'shipped', 'canceled']`
- `sum(review_scores)` → `35`, average → `3.5`, `count(5)` → `4`

Common mistake to watch for: accessing `list[8]` on an 8-item list → IndexError. Remind students valid indices are 0–7.

### For Loops
Iterate over sequences using `for`, `zip()`, `range()`, `enumerate()`. The `zip()` function walks two lists in parallel — exactly like reading two spreadsheet columns side by side.

Expected outputs from the demo:
- Loop with `zip(statuses, counts)` → `"delivered: 96,478 orders (97.0%)"` etc.
- `enumerate(cities)` → `"1. Sao Paulo"`, `"2. Rio De Janeiro"`, `"3. Belo Horizonte"`

Common mistake: forgetting to add 1 to enumerate index when numbering from 1.

### List Comprehensions
Compact syntax: `[expression for item in list if condition]`. One-line filter or transform.

Expected outputs:
- `[s for s in review_scores if s >= 4]` → `[5, 4, 5, 5, 4, 5]`
- Labels count → `Positive: 6, Neutral: 1, Negative: 3`

Common mistake: using `[` instead of `(` confuses students used to function calls.

---

## Group Exercise

```python
# Verified data from Olist
payment_types = ["credit_card", "boleto", "voucher", "debit_card", "not_defined"]
payment_counts = [76795, 19784, 5775, 1529, 3]

# Tasks:
# 1. Print total payments: sum(payment_counts) → Expected: 103,886
# 2. Using a for loop with zip(), print each type and its % of total
#    Expected: credit_card = 73.9%, boleto = 19.0%, etc.
# 3. Using a list comprehension, create a list of only types with count > 1000
#    Expected: ['credit_card', 'boleto', 'voucher', 'debit_card']
# 4. Create a list comprehension that converts all type names to UPPER CASE
# 5. What is the average payment count per type?
#    Expected: 103886 / 5 = 20,777.2
```

**Expected outputs**: total = 103,886 | top types by volume: credit_card (73.9%), boleto (19.0%), voucher (5.6%), debit_card (1.5%)

---

## Notes

- No AI assistance this week (Weeks 1–3 are no-AI)
- Thursday session continues with Dictionaries & Conditionals
