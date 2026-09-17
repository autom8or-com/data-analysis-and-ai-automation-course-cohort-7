# Week 7 — CTEs and Advanced Analytics: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-07-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-07-thu-exercises.ipynb`
- [ ] DeepSeek access confirmed for all students (this is a DeepSeek-guided session)
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Combine CTEs with window functions (LAG, RANK, NTILE) to answer multi-step business analytics questions.
2. Use `LAG()` inside a CTE to compare a row against the previous row in a defined order (e.g. month-over-month).
3. Use `RANK()` and a scalar CTE to compute a value's share of a total.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Wednesday's CTE patterns |
| 0:10–0:45 | Month-over-month order growth (LAG) | Demo + reading-the-result discussion (no fixed numeric answer — the pattern is the lesson) |
| 0:45–1:15 | Category revenue share + RANK | Demo + DeepSeek draft→run→verify protocol |
| 1:15–1:45 | Individual Exercises | Students work `week-07-thu-exercises.ipynb` Q1–Q5 |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Week 8 capstone (End-to-End Business Analysis) |

---

## Key Concepts

### Month-over-month order growth (LAG)

`monthly_orders` counts orders per month for 2017–2018; `with_prev` uses `LAG(order_count)
OVER (ORDER BY month)` to pull each row's previous-month count into the same row; the outer
query computes the percentage change. This is the standard pattern for any "how did this
change vs. last period" question.

```sql
WITH monthly_orders AS (
    SELECT strftime('%Y-%m', order_purchase_timestamp) AS month,
           COUNT(*) AS order_count
    FROM orders
    WHERE strftime('%Y', order_purchase_timestamp) IN ('2017', '2018')
    GROUP BY month
),
with_prev AS (
    SELECT month, order_count,
           LAG(order_count) OVER (ORDER BY month) AS prev_month_count
    FROM monthly_orders
)
SELECT month,
       order_count,
       prev_month_count,
       ROUND((order_count - prev_month_count) * 100.0 / prev_month_count, 1) AS growth_pct
FROM with_prev
WHERE prev_month_count IS NOT NULL
ORDER BY month
```

No specific expected output is documented for this query in the curriculum — run it live and
let students read the result: point out the November 2017 spike (Black Friday) and ask students
to spot which months show negative growth.

Common mistake to watch for: forgetting `WHERE prev_month_count IS NOT NULL` — the first row
in window order has no previous row, so `LAG()` returns NULL there and the growth-percentage
division would divide by NULL (silently producing NULL, not an error) if not filtered out.

### Category revenue share + RANK

`category_revenue` sums revenue per category (joining `order_items` → `products` →
`product_category_translation`, single fan-out table so no join-fan-out risk); `total` is a
one-row scalar CTE holding the platform-wide sum; the outer query computes each category's
percentage of that total via a correlated subquery on `total`, plus `RANK() OVER (ORDER BY
revenue DESC)`.

```sql
WITH category_revenue AS (
    SELECT t.product_category_name_english AS category,
           ROUND(SUM(oi.price), 2) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN product_category_translation t ON p.product_category_name = t.product_category_name
    GROUP BY category
),
total AS (
    SELECT SUM(revenue) AS total_revenue FROM category_revenue
)
SELECT category,
       revenue,
       ROUND(revenue * 100.0 / (SELECT total_revenue FROM total), 2) AS revenue_pct,
       RANK() OVER (ORDER BY revenue DESC) AS rank_num
FROM category_revenue
ORDER BY revenue DESC
LIMIT 10
```

No `revenue_pct`/`rank_num` value is documented in the curriculum — but the #1 category's raw
revenue IS independently verified: `health_beauty` = R$1,258,681.34 (top category, per
`olist_schema.md`). Use that as a live sanity check when the query runs (rank_num should be 1
for `health_beauty`).

**Using DeepSeek**: this is a DeepSeek-guided session — model the draft→run→verify protocol
live. Ask DeepSeek to draft a CTE + `RANK()` query, run what it drafts, and confirm the result
against the one verified number above (`health_beauty` revenue) before trusting the rest of the
output. Never let AI-drafted SQL bypass this check.

Common mistake to watch for: computing `revenue_pct` with integer division (no `* 100.0`) —
SQLite truncates `int / int` to `0` unless one operand is forced to REAL.

---

## Individual Exercises

Students work `week-07-thu-exercises.ipynb` (5 self-checking questions using CTEs + `RANK()`,
built on verified Olist facts rather than the demo's own — undocumented — LAG/RANK results).

**Expected outputs**:
1. Q1 — 2018 `order_count` (via `RANK() OVER (ORDER BY order_count DESC)` on a yearly CTE) = 54,011
2. Q2 — November 2017 `order_count` (Black Friday) = 7,544
3. Q3 — Top seller `total_revenue` (via `RANK()` on a seller-revenue CTE) = 229,472.63
4. Q4 — Top category `revenue` (via `RANK()` on a category-revenue CTE) = health_beauty, 1,258,681.34
5. Q5 — 5-star review count = 57,328

Solutions are in `week-07-thu-solutions.ipynb` (instructor-only, on Google Drive — do not share
with students).

---

## Weekly Assignment

1. Full seller analysis CTE: revenue, items sold, avg price, avg review score, tier classification. Show all 4 tiers with summary stats.
2. Which product categories showed month-over-month growth in orders for every month of 2018?
3. Using NTILE(4), split sellers into quartiles by revenue. What is the total revenue per quartile?
4. CTE: Find the top 3 product categories by revenue in each customer state (SP, RJ, MG, RS, PR).
5. Challenge: Build a "customer lifetime value" proxy — for each state, compute: total orders, total spent, avg days between orders (if they had multiple). Which state has the highest avg spend per customer?
