# Week 2 — GROUP BY, Aggregates & HAVING: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-02-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-02-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Learn to compute summaries across groups. By end of session: students can write GROUP BY with SUM, COUNT, AVG, MIN, MAX, and filter groups with HAVING.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run the setup cell |
| 0:10–0:35 | COUNT with GROUP BY | Demo order counts per `order_status`; verify all 8 status counts live |
| 0:35–1:00 | SUM, AVG, MIN, MAX | Demo full payment profile per `payment_type`; discuss `ROUND()` for money |
| 1:00–1:25 | Top-N groups | Demo `GROUP BY` + `ORDER BY` + `LIMIT` to find top customer states |
| 1:25–1:45 | HAVING — filtering groups | Demo `WHERE` (rows) vs `HAVING` (groups) with the >5,000-transaction filter |
| 1:45–2:00 | Mini-challenge & wrap-up | Individual practice, debrief, preview Thursday's review-score analysis |

---

## Key Concepts

### COUNT with GROUP BY
Count rows per group using `GROUP BY` with `COUNT(*)`.

Expected outputs (verified against the Olist dataset):
- `SELECT order_status, COUNT(*) AS count FROM orders GROUP BY order_status ORDER BY count DESC` →
  delivered 96,478 | shipped 1,107 | canceled 625 | unavailable 609 | invoiced 314 | processing 301 | created 5 | approved 2

Common mistake to watch for: selecting a non-aggregated, non-grouped column — SQLite allows it silently but returns an arbitrary row per group, which is a classic learner trap.

### SUM, AVG, MIN, MAX
Compute multiple aggregate functions per group in a single query.

Expected outputs (verified against the Olist dataset):
- `SELECT payment_type, COUNT(*) AS transaction_count, ROUND(AVG(payment_value),2) AS avg_value, ROUND(SUM(payment_value),2) AS total_value FROM order_payments GROUP BY payment_type ORDER BY transaction_count DESC` →
  credit_card 76,795 tx (avg 163.32, total 12,542,084.19) | boleto 19,784 tx (avg 145.03, total 2,869,361.27) | voucher 5,775 tx (avg 65.70, total 379,436.87) | debit_card 1,529 tx (avg 142.57, total 217,989.79) | not_defined 3 tx (avg 0.00, total 0.00)

### Counting customers by state
`GROUP BY` with `ORDER BY` and `LIMIT` to find the top-N groups.

Expected outputs (verified against the Olist dataset):
- `SELECT customer_state, COUNT(*) AS order_count FROM customers GROUP BY customer_state ORDER BY order_count DESC LIMIT 10` → top 5: SP 41,746 | RJ 12,852 | MG 11,635 | RS 5,466 | PR 5,045

### HAVING — filtering groups
`WHERE` filters rows before grouping; `HAVING` filters groups after grouping.

Expected outputs (verified against the Olist dataset):
- `SELECT payment_type, COUNT(*) AS count FROM order_payments GROUP BY payment_type HAVING COUNT(*) > 5000 ORDER BY count DESC` → credit_card 76,795 | boleto 19,784 | voucher 5,775

Common mistake to watch for: trying to use an aggregate function directly in `WHERE` (it errors), or using `HAVING` to filter individual rows instead of groups. Also watch for integer-division truncation in percentage calculations — force REAL division with `* 1.0`.

---

## Group Exercise

Wednesday has no separate group exercise — it is an individual/paired practice session (mini-challenge in the demo notebook) building toward Thursday's group exercise on review score analysis.

---
