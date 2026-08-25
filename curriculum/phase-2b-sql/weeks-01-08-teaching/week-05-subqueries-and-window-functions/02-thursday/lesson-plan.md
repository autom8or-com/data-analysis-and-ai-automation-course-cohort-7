# Week 5 — Subqueries and Window Functions: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-05-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-05-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Compute rankings, running totals, and comparisons without losing row-level detail.
2. Use `RANK()` and `ROW_NUMBER()` with `OVER (ORDER BY ...)` and explain how they differ on ties.
3. Build a running total with `SUM(...) OVER (ORDER BY ...)`.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Wednesday's subqueries |
| 0:10–0:45 | RANK() | Demo: rank sellers by total revenue |
| 0:45–1:15 | Running total with SUM() OVER, ROW_NUMBER() vs RANK() | Demo: monthly running total through 2017; ties comparison |
| 1:15–1:45 | Group Exercise | Combines subqueries (Wed) + window functions (Thu) |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Week 6 multi-table joins |

---

## Key Concepts

### RANK()
Rank sellers by total revenue using `RANK() OVER (ORDER BY SUM(price) DESC)`.

Expected outputs (verified against the Olist dataset):
- Top seller: `4869f7a5dfa277a7dca6462dcf3b52b2` = **R$229,472.63**

Common mistake to watch for: filtering a window function's own output directly in `WHERE` (window functions cannot be referenced in the same query's `WHERE` clause) — wrap the query in a CTE and filter the outer query instead.

### Running total with SUM() OVER
Compute a running total of monthly orders through 2017 using a window function layered over a `GROUP BY` aggregate.

Expected outputs (verified against the Olist dataset — selected rows):
| month | monthly_orders | running_total |
|---|---|---|
| 2017-01 | 800 | 800 |
| 2017-06 | 3,245 | 14,611 |
| 2017-11 | 7,544 | 39,428 |
| 2017-12 | 5,673 | 45,101 |

Common mistake to watch for: dates in SQLite are stored as TEXT — use `strftime()` to extract year/month, not date-type functions.

### ROW_NUMBER() vs RANK()
Compare `ROW_NUMBER()` (unique sequential number even with ties) against `RANK()` (ties share a rank, next rank skips) over the same `ORDER BY`.

Expected outputs: no single verified numeric target in the curriculum — students should observe how the two functions diverge whenever `customer_state` order counts tie.

Common mistake to watch for: assuming `RANK()` and `ROW_NUMBER()` always agree — they only diverge on ties, so a naive demo query can look identical to `ROW_NUMBER()` until a tie appears.

---

## Group Exercise

This week's group exercise brings subqueries (Wednesday) and window functions (Thursday) together, in `week-05-thu-exercises.ipynb`:

1. Find all sellers whose total revenue is above the average seller revenue (use subquery).
2. Rank customer states by average review score (join orders, customers, order_reviews first, then rank).
3. Compute a running total of payment revenue through 2018 (month by month).
4. Use ROW_NUMBER() to number each review within its review score group (partition by review_score).

**Expected outputs** (verified against the Olist dataset):
1. **628 sellers** have total revenue above the average seller revenue (R$4,391.48).
2. **27 states** ranked by average review score; top-ranked state is **AM** at **4.21**.
3. **10 months** of 2018 payment revenue (Jan–Oct); January revenue **R$1,115,004.18**, October running total **R$8,699,763.05**.
4. **99,224** total rows numbered; within the 5-star partition, row numbers run 1 to **57,328**.

> **Data-quality note for Q2**: `order_reviews` has 547 orders with more than one review row. Joining it directly to `orders`/`customers` before aggregating fans out those orders and produces the wrong ranking (a naive join ranks AP first at 4.19 instead of the correct AM at 4.21). Collapse `order_reviews` to one row per `order_id` in a CTE first, then join.

---

## Weekly Assignment

1. Which states have more delivered orders than the national average by state?
2. Use RANK() to rank payment types by total revenue. Show rank, type, and total.
3. Build a monthly running total for order payments in 2017.
4. Find the top 20 sellers by item count. Do they also rank top 20 by revenue?
5. Challenge: Use a subquery to find products that have been sold more than the average product's sales count. How many such products exist?

---
