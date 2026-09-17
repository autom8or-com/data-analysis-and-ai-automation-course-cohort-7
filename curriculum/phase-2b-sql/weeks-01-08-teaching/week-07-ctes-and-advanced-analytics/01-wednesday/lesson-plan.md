# Week 7 — CTEs and Advanced Analytics: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-07-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-07-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Use CTEs to break complex queries into readable, named steps.
2. Write a single `WITH` block to pre-aggregate a table before filtering or ranking it.
3. Chain two CTEs together, where the second CTE reads from the first.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Week 6's multi-table joins |
| 0:10–0:45 | Basic CTE — state-level revenue summary | Demo + mini-challenge (`customer_orders` CTE, states ranked by spend) |
| 0:45–1:15 | Multi-step CTE — Seller Tiers | Demo + mini-challenge (`seller_revenue` → `seller_tiers` chained CTEs) |
| 1:15–1:45 | Individual Exercises | Students work `week-07-wed-exercises.ipynb` Q1–Q5 |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Thursday's window functions (LAG, RANK) |

---

## Key Concepts

### Basic CTE — state-level revenue summary

A single CTE named `customer_orders` pre-aggregates order count, total spent, and average
order value per `customer_state` (delivered orders only, joining `orders` → `customers` →
`order_payments`). The outer query then reads from that named result set to sort and limit it —
this is the core CTE idea: name an intermediate result, then query the name instead of repeating
the subquery logic.

```sql
WITH customer_orders AS (
    SELECT c.customer_state,
           COUNT(o.order_id) AS total_orders,
           ROUND(SUM(op.payment_value), 2) AS total_spent
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state
)
SELECT customer_state,
       total_orders,
       total_spent,
       ROUND(total_spent / total_orders, 2) AS avg_order_value
FROM customer_orders
ORDER BY total_spent DESC
LIMIT 8
```

Expected outputs (verified against the Olist dataset):
| customer_state | total_orders | total_spent | avg_order_value |
|---|---|---|---|
| SP | 42,308 | 5,770,266.19 | 136.39 |
| RJ | 13,004 | 2,055,690.45 | 158.08 |
| MG | 11,804 | 1,819,277.61 | 154.12 |

Common mistake to watch for: a CTE lives for exactly one statement — students will try to
reference `customer_orders` in a later, separate cell and get "no such table" once the kernel
state doesn't carry it over as expected, or they'll put a trailing comma after the last CTE
before the outer `SELECT` (only commas *between* CTEs are valid).

### Multi-step CTE — Seller Tiers

Two chained CTEs: `seller_revenue` aggregates per-seller revenue and items sold from
`order_items`; `seller_tiers` reads *from* `seller_revenue` and classifies each seller into a
tier with `CASE`. The outer query then aggregates per tier. This is the pattern for any
"first compute X, then classify/rank by X" business question.

```sql
WITH seller_revenue AS (
    SELECT seller_id,
           ROUND(SUM(price), 2) AS total_revenue,
           COUNT(*) AS items_sold
    FROM order_items
    GROUP BY seller_id
),
seller_tiers AS (
    SELECT seller_id,
           total_revenue,
           items_sold,
           CASE
               WHEN total_revenue >= 100000 THEN 'Top Seller'
               WHEN total_revenue >= 50000 THEN 'High Performer'
               WHEN total_revenue >= 10000 THEN 'Mid Tier'
               ELSE 'Standard'
           END AS tier
    FROM seller_revenue
)
SELECT tier,
       COUNT(*) AS seller_count,
       ROUND(AVG(total_revenue), 2) AS avg_revenue,
       ROUND(SUM(total_revenue), 2) AS tier_total_revenue
FROM seller_tiers
GROUP BY tier
ORDER BY avg_revenue DESC
```

Expected outputs (verified against the Olist dataset):
| tier | seller_count | avg_revenue | tier_total_revenue |
|---|---|---|---|
| Top Seller | 18 | 149,574.75 | 2,692,345.55 |
| High Performer | 22 | 60,117.14 | 1,322,577.15 |
| Mid Tier | 252 | 19,812.97 | 4,992,867.56 |
| Standard | 2,803 | 1,635.34 | 4,583,853.44 |

Business insight to surface with the class: 18 top sellers generate R$2.7M in revenue. 2,803
standard sellers generate R$4.6M combined. The top 18 (0.6% of sellers) generate nearly 20% of
total product revenue.

Common mistake to watch for: forgetting that `seller_tiers` can only select columns
`seller_revenue` actually exposed — if a student wants `items_sold` in the final output, it has
to be carried through both CTEs' `SELECT` lists, not just the first.

---

## Individual Exercises

Students work `week-07-wed-exercises.ipynb` (5 self-checking questions built on the two CTE
patterns above — state revenue and seller tiers). Each question is auto-graded: a green
`✅ Qn correct` print means the query is right.

**Expected outputs**:
1. Q1 — RJ `total_spent` = 2,055,690.45
2. Q2 — MG `avg_order_value` = 154.12
3. Q3 — Top Seller `seller_count` = 18
4. Q4 — Standard tier `tier_total_revenue` = 4,583,853.44
5. Q5 — High Performer `avg_revenue` = 60,117.14

Solutions are in `week-07-wed-solutions.ipynb` (instructor-only, on Google Drive — do not share
with students).

---
