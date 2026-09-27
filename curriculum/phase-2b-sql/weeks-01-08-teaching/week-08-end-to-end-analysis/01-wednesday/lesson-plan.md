# Week 8 — End-to-End Business Analysis (Capstone Week): Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-08-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-08-wed-exercises.ipynb`
- [ ] Project groups assigned/confirmed (same 4 groups carrying over from Phase 1)
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Combine all skills — JOINs, CTEs, Window Functions, CASE WHEN, and date functions — into a single coherent business analysis.
2. Work in groups to answer a leadership-style business brief using only SQL-verified numbers.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Week 7's CTEs and window functions |
| 0:10–0:15 | The Business Brief | Present the leadership brief (growth, top sellers, top categories, delivery vs. satisfaction) |
| 0:15–1:00 | Analysis 1–3 walkthrough | Demo: Platform Growth, Delivery Performance by State, Review Score vs. Delivery — instructor-led, `week-08-wed-demo.ipynb` |
| 1:00–1:45 | Group Exercise | Groups split the 4 brief questions and begin building their own queries, `week-08-wed-exercises.ipynb` |
| 1:45–2:00 | Debrief & preview | Share verification anchors, preview Thursday's presentation-prep session |

---

## Key Concepts

### Analysis 1: Platform Growth (2017 vs 2018)

A `yearly_summary` CTE joins `orders` to `order_payments`, groups by year (`strftime('%Y', ...)`),
and reports total orders, total revenue, average order value, and unique customers for 2017 and
2018 only (2016 is excluded — it only has 329 orders, not a fair year-over-year comparison).

```sql
WITH yearly_summary AS (
    SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
           COUNT(DISTINCT o.order_id) AS total_orders,
           ROUND(SUM(op.payment_value), 2) AS total_revenue,
           ROUND(AVG(op.payment_value), 2) AS avg_order_value,
           COUNT(DISTINCT o.customer_id) AS unique_customers
    FROM orders o
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE strftime('%Y', o.order_purchase_timestamp) IN ('2017', '2018')
    GROUP BY year
)
SELECT year, total_orders, total_revenue, avg_order_value, unique_customers
FROM yearly_summary
ORDER BY year
```

Expected outputs (verified against the Olist dataset): 2017 `total_orders` = 45,101; 2018
`total_orders` = 54,011 (per `olist_schema.md`'s verified stats — no per-year revenue/AOV figure
is separately documented in the curriculum, so present those columns live rather than quoting a
fixed number).

Common mistake to watch for: joining `order_payments` risks losing the one order that has no
payment row — but that order is a 2016 order, already excluded by the `WHERE` clause, so the
order counts above match exactly. Use this to teach "which rows could this JOIN have dropped?"

### Analysis 2: Delivery Performance by State

`delivery_stats` aggregates delivered orders per `customer_state`: count, average delivery days
(`julianday` difference), and late-delivery count. The outer query adds the late percentage and
a `national_avg_days` column via `AVG(avg_days) OVER ()` — an empty-frame window function that
averages across all rows in the result set.

```sql
WITH delivery_stats AS (
    SELECT c.customer_state,
           COUNT(*) AS delivered_orders,
           ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_days,
           SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS late_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY c.customer_state
)
SELECT customer_state,
       delivered_orders,
       avg_days,
       late_count,
       ROUND(late_count * 100.0 / delivered_orders, 1) AS late_pct,
       ROUND(AVG(avg_days) OVER (), 1) AS national_avg_days
FROM delivery_stats
ORDER BY avg_days ASC
LIMIT 10
```

Expected output: exactly 10 rows (LIMIT 10), SP is fastest. `national_avg_days` evaluates to
**18.8**, not the dataset-wide verified 12.6 days — because `AVG(avg_days) OVER ()` averages the
27 *state averages* with equal weight per state, not per order. Use this discrepancy as the
teaching moment: "how long does a typical order take?" (12.6, order-weighted) vs. "how long does
a typical state wait?" (18.8, state-weighted) are two different, both legitimate, questions.

Common mistake to watch for: assuming `AVG(...) OVER ()` reproduces an order-weighted average —
it doesn't, unless every group has the same number of rows.

### Analysis 3: Review Score and Delivery Relationship

`delivery_and_review` groups delivered orders by `review_score` and computes average delivery
days, order count, and late-delivery percentage per score.

```sql
WITH delivery_and_review AS (
    SELECT r.review_score,
           ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_delivery_days,
           COUNT(*) AS order_count,
           SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS late_count
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY r.review_score
)
SELECT review_score, avg_delivery_days, order_count,
       ROUND(late_count * 100.0 / order_count, 1) AS late_pct
FROM delivery_and_review
ORDER BY review_score
```

Expected output: 5 rows, monotone relationship — 1-star reviews average ~21.3 days late-delivery
(~37.8% late), 5-star reviews average ~10.7 days (~3.0% late). The 5-star `order_count` (57,059)
sits slightly below the dataset-wide verified 5-star count (57,328) because this query filters
to delivered orders only.

Common mistake to watch for: this query joins `orders` to `order_reviews` only (one fan-out
table, not two), so no fan-out risk here — but remind students that adding a second fan-out
join (e.g. `order_items`) without first collapsing it to one row per `order_id` in a CTE would
inflate these counts. See `olist_schema.md`'s "Join cardinality & fan-out" section.

---

## Group Exercise

**The Business Brief**: You are a data analyst presenting to Olist's leadership team. They want
to understand: (1) How has the platform grown? (2) Which sellers drive the most value? (3) Which
product categories are the real revenue drivers? (4) How does delivery performance affect
customer satisfaction? Your analysis must be SQL-only and all numbers must be verified.

Groups split the four leadership questions one owner each, using JOINs, CTEs, window functions,
CASE WHEN, and date functions as needed — the three analyses above are the group's shared toolkit
(reuse their *shape*, not their exact numbers, for each group member's assigned question).

**Expected outputs (anchors to verify against)**: 99,441 total orders / 96,478 delivered / 625
canceled / 97.0% delivered; R$15,843,553.24 total GMV; R$1,258,681.34 top category
(`health_beauty`) revenue; R$229,472.63 top seller revenue; 12.6 avg delivery days; 7,826 (8.1%)
late deliveries.

Students continue this work in `week-08-wed-exercises.ipynb` (guided practice on Analyses 1–3
plus two locked self-checking KPI-verification questions reusing the exact final verification
queries from the curriculum).

Solutions are in `week-08-wed-solutions.ipynb` (instructor-only, on Google Drive — do not share
with students).

---
