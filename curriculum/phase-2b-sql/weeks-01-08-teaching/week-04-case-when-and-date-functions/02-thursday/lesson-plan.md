# Week 4 — CASE WHEN & Date Functions: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-04-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-04-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Extract year and month from SQLite's TEXT-based timestamps using `strftime()`.
2. Compute date differences with `julianday()` to measure delivery time.
3. Combine `CASE WHEN` (from Wednesday) with date arithmetic to classify records by time-based rules.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Wednesday's `CASE WHEN` |
| 0:10–0:40 | Date extraction with strftime() | Demo: orders by year, monthly 2017 breakdown (Black Friday spike) |
| 0:40–1:05 | Date differences with julianday() | Demo: avg delivery days, late deliveries |
| 1:05–1:20 | DeepSeek prompt-then-verify | Practice prompting for a `strftime` query and verifying against 45,101 |
| 1:20–1:45 | Exercises | Students work `week-04-thu-exercises.ipynb` |
| 1:45–2:00 | Group Exercise + debrief | CASE WHEN + date functions combined; preview Week 5 (subqueries & window functions) |

---

## Key Concepts

### Date extraction with strftime() — orders by year

SQLite stores dates as TEXT (ISO format). Use `strftime()` to extract parts.

Expected outputs (verified against the Olist dataset):
| year | order_count |
|---|---|
| 2016 | 329 |
| 2017 | 45,101 |
| 2018 | 54,011 |

Note: 2016 has only 329 orders — the dataset starts in September 2016. This is an incomplete year and should not be compared directly to 2017/2018.

### Monthly orders — 2017 only

Expected — full 2017:
| month | orders |
|---|---|
| 2017-01 | 800 | 2017-02 | 1,780 | 2017-03 | 2,682 | 2017-04 | 2,404 |
| 2017-05 | 3,700 | 2017-06 | 3,245 | 2017-07 | 4,026 | 2017-08 | 4,331 |
| 2017-09 | 4,285 | 2017-10 | 4,631 | 2017-11 | **7,544** | 2017-12 | 5,673 |

November 2017 = 7,544 orders — the Black Friday peak, nearly 2x a typical month.

### Date difference — delivery time

- Average delivery days (delivered orders only): **12.6 days**
- Late deliveries (delivered after estimated date): **7,826** (8.1% of delivered orders)

Common mistake to watch for: subtracting two TEXT date columns directly does not work as expected — always wrap both sides in `julianday()`. A `WHERE` guard on delivery date silently narrows every other column in the same query — filter inside a `CASE`/subquery when you need to preserve the full row count.

---

## Group Exercise

1. Classify customers into geographic regions using CASE WHEN (Southeast: SP, RJ, MG, ES; South: RS, SC, PR; Northeast: BA, CE, PE, MA, RN, PB, AL, SE, PI; Other: everything else).
2. How many orders were placed on weekends vs weekdays? (Hint: `strftime('%w', ...)` returns 0=Sunday, 6=Saturday.)
3. What is the average delivery time by customer state? Show the 5 fastest and 5 slowest states.
4. For each month of 2018: order count, total revenue from `order_payments`, and a CASE WHEN flag for whether it was a "peak month" (≥6,000 orders).

**Expected outputs**: not documented in the curriculum for these four questions — do not assert specific numbers; treat as open-ended analytical practice. (Two useful reconciliation checks: regions must sum to 99,441 customers; the 2018 monthly counts must sum to 54,011 orders.)

---

## Weekly Assignment

1. Build a complete status summary: count and % of each status_group (Completed / In Progress / Canceled / Other).
2. What is the average delivery time for SP vs RJ customers?
3. How many orders were delivered within 7 days? Within 14 days? Over 30 days?
4. Build a month-by-month table for all of 2017 and 2018. Which month had the highest order count?
5. Challenge: Create a CASE WHEN that classifies delivery as 'Fast' (≤7 days), 'Standard' (8–14 days), 'Slow' (15–30 days), 'Very Slow' (>30 days). Count orders in each category.
