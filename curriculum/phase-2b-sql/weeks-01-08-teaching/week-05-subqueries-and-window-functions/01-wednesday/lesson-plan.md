# Week 5 — Subqueries and Window Functions: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-05-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-05-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Write queries that use the result of another query (subqueries).
2. Understand when a subquery is appropriate versus a JOIN.
3. Use a scalar subquery in `WHERE`, a subquery as a derived table in `FROM`, and `IN`/`NOT IN` with a subquery.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py` |
| 0:10–0:45 | Scalar subquery in WHERE | Demo + DeepSeek-assisted mini-challenge (Week 4+) |
| 0:45–1:15 | Subquery in FROM, IN with subquery | Demo, NULL data-quality note on `products` |
| 1:15–1:45 | Individual exercises | `week-05-wed-exercises.ipynb`, 5 self-checking questions |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Thursday's window functions |

---

## Key Concepts

### Scalar subquery in WHERE
Use a subquery that returns a single value inside a `WHERE` clause comparison — e.g. finding orders with a payment value above the dataset average.

Expected outputs (verified against the Olist dataset):
- Orders with `payment_value` above average: **31,012**
- Average `payment_value`: **R$154.10**

Common mistake to watch for: a scalar subquery must return exactly one row/column — if it can return more than one, use `IN` instead.

### Subquery in FROM clause
Treat a subquery's result as a derived table so you can aggregate a value (like items per order) that a single `GROUP BY` cannot express directly.

Expected outputs: no single verified numeric target in the curriculum — students should reason about the shape of the result (average items per order lands just above 1).

Common mistake to watch for: forgetting to alias the derived table or its columns, which SQLite (and most engines) requires.

### IN with subquery
Filter rows using `IN` against the result set of a subquery — e.g. delivered orders whose customer is in São Paulo (`SP`).

Expected outputs (verified against the Olist dataset):
- Delivered orders from SP customers: **40,501**
- Products with NULL `product_category_name`: **610**
- Products with NULL `product_weight_g`: **2**

Common mistake to watch for: the `products` table has misspelled columns — `product_name_lenght` and `product_description_lenght` (missing the 'g'). Use the actual column names as they appear in the table. Also: `NULL` must be tested with `IS NULL` / `IS NOT NULL`, never `= NULL`.

---

## Group Exercise

Wednesday is individual-exercise focused (5 self-checking questions building on the subquery concepts above, in `week-05-wed-exercises.ipynb`). The week's group exercise runs Thursday, combining both days' material — see the Thursday lesson plan.

**Expected outputs**: see the exercises notebook's locked check cells for the verified values per question.

---
