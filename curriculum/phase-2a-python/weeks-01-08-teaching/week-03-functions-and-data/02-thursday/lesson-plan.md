# Week 3 — Functions & First Contact with Data: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week03_thu_demo.ipynb`
- [ ] Student exercise link ready to share: `week03_thu_exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] Dataset needed: `olist_orders_dataset.csv` (99,441 rows) — students mount Drive

---

## Learning Objectives

By the end of this session, students will be able to:
1. Open and read CSV files using `open()` and the `csv` module
2. Build a list of dicts from a CSV file
3. Apply functions to CSV data
4. Understand why pandas will make all of this easier

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup | Students mount Drive, open Colab |
| 0:10–0:40 | Part 1 — Reading CSV with `open()` | Demo: headers, row count = 99,441 |
| 0:40–1:15 | Part 2 — Building Data Structures | Demo: `load_orders()`, sample then all rows |
| 1:15–1:45 | Part 3 — Applying Functions to CSV | Demo: classify 99,441 rows, Counter results |
| 1:45–2:00 | Group Exercise | 4 tasks on the loaded orders list |

---

## Key Concepts

### Reading CSV with open()
Use the `csv` module and `DictReader` to iterate over real CSV files row by row.

**Expected outputs:**
```
Headers: ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
          'order_approved_at', 'order_delivered_carrier_date',
          'order_delivered_customer_date', 'order_estimated_delivery_date']
Total rows: 99,441
```

**Common mistake:** Forgetting to loop inside the `with` block — file closes before reading.

### Building Data Structures from CSV
Load CSV rows into a list of dicts with a reusable `load_orders` function; use `limit` for exploration.

**Expected outputs:**
```
Loaded: 1000 orders
Status of first order: delivered
```

**Common mistake:** Using `i >= limit` without checking `if limit` first — crashes when `limit=None`.

### Applying Functions to CSV Data
Load all 99,441 rows, apply classification functions to every row, aggregate results with Counter.

**Expected outputs:**
```
Total: 99,441
```

**Key teaching moment** (end of Part 3):
> *"We just did something real: we read 99,441 rows, applied a classification function to every row, and counted the results. But notice how much code that took — 25+ lines. Next week, we'll do the same thing in 3 lines using pandas. That's why pandas exists."*

---

## Group Exercise

## Thursday Group Exercise: Analyse the Orders Dataset

Using the loaded orders list (all 99,441 rows):

```python
# Task 1: Count how many orders have a blank order_delivered_customer_date
#    (Hint: check if the value is an empty string "")
#    Expected: ~2,965 rows have no delivery date

# Task 2: Write a function count_by_status(orders_list) that returns a dict
#    of {status: count} for all statuses in the list
#    Verify: delivered should be 96,478

# Task 3: Using a list comprehension, create a list of all unique order statuses
#    How many distinct statuses are there?

# Task 4: From the orders list, filter to only "canceled" orders
#    How many are there? Expected: 625
```

**Expected outputs:**
- Blank delivery dates: ~2,965
- `count_by_status` → delivered: 96,478
- Unique statuses: 8 distinct values
- Canceled orders: 625

---

## Weekly Assignment

## Weekly Assignment 3

Submit `week3_assignment.ipynb`:

1. Write a function `load_csv(filepath, limit=None)` that loads any CSV file into a list of dicts. Test it on `olist_orders_dataset.csv`. Verify row count = **99,441**.

2. Using the loaded orders, write a function `status_report(orders_list)` that:
   - Counts each status
   - Calculates each status as a % of total
   - Returns a list of dicts: `[{"status": "delivered", "count": 96478, "pct": 97.0}, ...]`
   - Print each item as: `"delivered: 96,478 orders (97.0%)"`

3. Write a function `find_orders_by_status(orders_list, status)` that filters and returns only orders matching a given status. Test: `find_orders_by_status(orders, "canceled")` should return a list of **625** orders.

4. **Reflection question** (1 paragraph in a text cell): You just processed 99,441 rows using pure Python. What were the most tedious parts of this work? What would you want a tool to do automatically?

---

## Session Notes

- Emphasise that everything from CSV is a **string** — no automatic type conversion.
- The `~2,965` blank delivery dates is approximate since a few more orders may be "not yet delivered" depending on the snapshot date; `96,478 delivered` is the exact verified count.
- The reflection question (Assignment Q4) is intentional: students should arrive at "I want something to load the file in one line" — which is exactly what pandas does next week.
