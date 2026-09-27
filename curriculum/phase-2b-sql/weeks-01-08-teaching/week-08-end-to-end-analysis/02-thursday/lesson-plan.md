# Week 8 — End-to-End Business Analysis (Capstone Week): Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-08-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-08-thu-exercises.ipynb`
- [ ] DeepSeek access confirmed for all students (this is a DeepSeek-guided session)
- [ ] Projector + timer ready for 10-minute group presentations

---

## Learning Objectives

By the end of this session, students will be able to:
1. Finalise and present a 10-minute SQL-driven business analysis synthesising the full course's SQL skills.
2. Verify every headline number against a locked SQL query before presenting it.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Wednesday's 3 analyses |
| 0:10–0:20 | The 5 deliverables | Walk through `week-08-thu-demo.ipynb`: platform KPIs, top 5 categories, seller tiers, delivery performance, open question |
| 0:20–0:50 | Verification pass | Demo the two locked final-verification queries; DeepSeek draft→run→verify protocol |
| 0:50–1:40 | Group Exercise | Groups finalise their 5 analyses using `week-08-thu-exercises.ipynb`, then rehearse |
| 1:40–2:00 | Group Presentations | Each group presents (time permitting; otherwise continue into a follow-up session) |

---

## Key Concepts

### The 5 presentation deliverables

Each group must produce, in SQL only (no pandas manipulation beyond display):
1. Platform overview KPIs (total orders, total revenue, avg order value, delivered %)
2. Top 5 product categories by revenue
3. Seller tier breakdown (reuse the Week 7 CTE pattern)
4. Delivery performance: avg days, late %, review score correlation
5. One additional business question chosen by the group

**Deliverable 2 — Top 5 product categories by revenue**: join `order_items` → `products` →
`product_category_translation`, group by the English category name, order by revenue
descending, limit 5. The top row reproduces the verified top category: `health_beauty` =
R$1,258,681.34.

**Deliverable 3 — Seller tier breakdown**: collapse `order_items` to seller grain (`SUM(price)`
per `seller_id`), then `NTILE(4) OVER (ORDER BY seller_revenue DESC)` to split sellers into 4
tiers, then aggregate per tier. Tier 1's top seller reproduces the verified top-seller revenue:
R$229,472.63.

**Deliverable 4 — Delivery performance & review correlation**: reuses Wednesday's Analysis
2/3 pattern — collapse `order_reviews` to one row per `order_id` in a CTE first (fan-out safe),
join to delivered orders, and split average review score by on-time vs. late delivery. Reproduces
the verified anchors: avg delivery days = 12.6, late deliveries = 7,826 (8.1%).

**Deliverable 5 — open business question**: no fixed answer — groups choose their own question
and must show the query, not just the number.

Common mistake to watch for: directly joining two of `order_items` / `order_payments` /
`order_reviews` and then aggregating without collapsing to one row per `order_id` first — this
fans out rows and silently inflates SUM/AVG/COUNT results (see `olist_schema.md`'s "Join
cardinality & fan-out" section; this is the exact defect class that shipped in a Phase 2a Week 7
notebook).

### The verification pass — final KPIs

Before presenting, every group must reproduce these two locked queries exactly:

```sql
-- Final verification query — all numbers must match
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS canceled,
    ROUND(SUM(CASE WHEN order_status = 'delivered' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS delivered_pct
FROM orders
```

Expected: `total_orders` = 99,441 | `delivered` = 96,478 | `canceled` = 625 | `delivered_pct` = 97.0%

```sql
-- Total GMV verification
SELECT ROUND(SUM(price), 2) AS product_revenue,
       ROUND(SUM(freight_value), 2) AS freight_revenue,
       ROUND(SUM(price + freight_value), 2) AS total_gmv
FROM order_items
```

Expected: `product_revenue` = 13,591,643.70 | `freight_revenue` = 2,251,909.54 | `total_gmv` = 15,843,553.24

**Using DeepSeek**: this is a DeepSeek-guided session — model the draft→run→verify protocol live.
Ask DeepSeek to draft SQL for any deliverable, run what it drafts, and confirm the result against
the closest verified anchor before trusting the rest of the output. Never let AI-drafted SQL
reach a slide unverified.

---

## Group Exercise

Groups finalise their 10-minute presentation using `week-08-thu-exercises.ipynb`: guided
practice on the top-5-categories, seller-tier, and delivery-performance queries (Part A), plus
the two locked self-checking KPI/GMV verification questions (Part B), plus an open scaffold for
their self-chosen fifth analysis.

Solutions are in `week-08-thu-solutions.ipynb` (instructor-only, on Google Drive — do not share
with students).

---

## Week 8 Group Presentation (summative)

- 10-minute SQL-driven business analysis, presented by each group
- All KPIs must match the verified expected values above
- Groups present 5 analyses (4 guided + 1 self-chosen)

| Criteria | Marks |
|---|---|
| SQL correctness (verified outputs) | 15 |
| Business insight quality | 15 |
| Query readability and structure | 10 |
| **Total** | **40** |

This is Phase 2b SQL's capstone week — there is no individual Weekly Assignment this week (unlike
Weeks 1–7); the group presentation is the deliverable. Phase 2c (Capstone) follows, bringing
Python and SQL together into a Streamlit dashboard with the same 4 project groups.
