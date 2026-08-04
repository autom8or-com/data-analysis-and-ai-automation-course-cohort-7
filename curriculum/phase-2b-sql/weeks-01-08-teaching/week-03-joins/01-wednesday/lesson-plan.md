# Week 3 — JOINs: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-03-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-03-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Learn INNER JOIN and LEFT JOIN. By end of session: students can join two tables and filter/group across both.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run the setup cell |
| 0:10–0:30 | INNER JOIN basics | Demo joining `orders` to `customers` on `customer_id`; aliases (`o`, `c`) and why they matter |
| 0:30–0:55 | Filter/group across joined tables | Demo delivered orders by customer state (top 5: SP, RJ, MG, RS, PR) |
| 0:55–1:20 | Many-to-one joins & revenue | Demo `order_items` joined to `sellers`; revenue and seller counts per state |
| 1:20–1:45 | Going deeper & common mistakes | Missing `ON` clause (cartesian explosion), ambiguous column names, `COUNT(*)` fan-out after a one-to-many join |
| 1:45–2:00 | Mini-challenge & wrap-up | Individual practice, debrief, preview Thursday's LEFT JOIN session |

---

## Key Concepts

### INNER JOIN
The `orders` table has `customer_id` but not the customer's state; `customers` has it. `JOIN`/`INNER JOIN` are identical in SQLite. Always alias joined tables to avoid ambiguous-column errors and keep queries readable.

Expected outputs (verified against the Olist dataset):
- `SELECT o.order_id, o.order_status, c.customer_state, c.customer_city FROM orders o JOIN customers c ON o.customer_id = c.customer_id LIMIT 10` → 10 rows, one per order, each now carrying the customer's state and city.
- A join-cardinality sanity check (`COUNT(*)` after the join) returns 99,441 — identical to the `orders` row count, confirming this is a clean 1:1 join.

Common mistake to watch for: omitting the `ON` clause produces a cartesian product (99,441 × 99,441 ≈ 9.9 billion rows) instead of an error — SQLite will happily try to compute it. Referencing an unqualified column that exists in both tables (e.g. `customer_id`) raises `ambiguous column name`.

### Delivered orders by state
Join, filter, then group — `WHERE o.order_status = 'delivered'` before `GROUP BY c.customer_state`.

Expected outputs (verified against the Olist dataset):
- `SELECT c.customer_state, COUNT(*) AS order_count FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.order_status = 'delivered' GROUP BY c.customer_state ORDER BY order_count DESC LIMIT 5` →
  SP 40,501 | RJ 12,350 | MG 11,354 | RS 5,345 | PR 4,923

### Sellers and their revenue
Joining `order_items` (many rows per order) to `sellers` (one row per seller) to compute per-seller totals.

Expected outputs (verified against the Olist dataset):
- `SELECT oi.seller_id, s.seller_state, COUNT(*) AS items_sold, ROUND(SUM(oi.price), 2) AS total_revenue FROM order_items oi JOIN sellers s ON oi.seller_id = s.seller_id GROUP BY oi.seller_id, s.seller_state ORDER BY total_revenue DESC LIMIT 10` → top seller ~R$229,472.63 across 1,156 items (an SP seller).

Common mistake to watch for: after a one-to-many join, `COUNT(*)` counts line items, not orders — e.g. counting rows after `orders JOIN order_items` returns 112,650 line items, not 99,441 orders. Use `COUNT(DISTINCT order_id)` when the order count is what's wanted.

### Revenue by seller state
Rolling the seller-level join up to state level with `COUNT(DISTINCT oi.seller_id)`.

Expected outputs (verified against the Olist dataset):
- `SELECT s.seller_state, COUNT(DISTINCT oi.seller_id) AS seller_count, ROUND(SUM(oi.price), 2) AS total_revenue FROM order_items oi JOIN sellers s ON oi.seller_id = s.seller_id GROUP BY s.seller_state ORDER BY total_revenue DESC LIMIT 8` →
  SP 1,849 sellers / R$8,753,396.21 | PR 349 / R$1,261,887.21 | MG 244 / R$1,011,564.74 | RJ 171 / R$843,984.22 | SC 190 / R$632,426.07

---

## Group Exercise

Wednesday has no separate group exercise — it is an individual/paired practice session (mini-challenge in the demo notebook) building toward Thursday's LEFT JOIN and three-table join exercises.

---
