# Week 6 — Multi-table Joins and Complex Aggregations: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-06-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-06-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Combine 3+ tables to answer real business questions that no single table can answer.
2. Recognize and reason about join fan-out (`order_items`, `order_payments`, `order_reviews` all hold multiple rows per `order_id`) and know when `COUNT(DISTINCT order_id)` and a `WITH` CTE pre-aggregation step are required.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Week 5 subqueries/window functions |
| 0:10–0:45 | Concept 1 — Three-table join: revenue by category | `order_items → products → product_category_translation`; demo + mini-challenge |
| 0:45–1:15 | Concept 2 — Price vs review score | `order_items JOIN order_reviews`; demo + discussion of the fan-out caveat |
| 1:15–1:45 | Group Exercise | Trace the join chain, then predict the fan-out (see notebook §Group Exercise) |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Thursday's geographic revenue analysis |

---

## Key Concepts

### Three-table join — revenue by product category (English)

Business question: What is the revenue by product category (in English)? Requires joining `order_items` → `products` → `product_category_translation`.

```sql
SELECT t.product_category_name_english AS category,
       COUNT(DISTINCT oi.order_id) AS order_count,
       COUNT(DISTINCT oi.seller_id) AS seller_count,
       ROUND(SUM(oi.price), 2) AS total_revenue,
       ROUND(AVG(oi.price), 2) AS avg_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN product_category_translation t ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10
```

Expected top 10 (verified against the Olist dataset):

| category | order_count | seller_count | total_revenue | avg_price |
|---|---|---|---|---|
| health_beauty | 8,836 | 492 | 1,258,681.34 | 130.16 |
| watches_gifts | 5,624 | 101 | 1,205,005.68 | 201.14 |
| bed_bath_table | 9,417 | 196 | 1,036,988.68 | 93.30 |
| sports_leisure | 7,720 | 481 | 988,048.97 | 114.34 |
| computers_accessories | 6,689 | 287 | 911,954.32 | 116.51 |
| furniture_decor | 6,449 | 370 | 729,762.49 | 87.56 |
| cool_stuff | 3,632 | 267 | 635,290.85 | 167.36 |
| housewares | 5,884 | 468 | 632,248.66 | 90.79 |
| auto | 3,897 | 383 | 592,720.11 | 139.96 |
| garden_tools | 3,518 | 237 | 485,256.46 | 111.63 |

Common mistake to watch for: reaching for `COUNT(*)` instead of `COUNT(DISTINCT oi.order_id)` — a category with many multi-item orders will report an inflated order count.

### Price vs review score

Business question: Does price differ by review score? Joins `order_items` to `order_reviews` on `order_id`.

```sql
SELECT r.review_score,
       COUNT(DISTINCT oi.order_id) AS order_count,
       ROUND(AVG(oi.price), 2) AS avg_item_price,
       ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY r.review_score
ORDER BY r.review_score
```

Expected output (verified against the Olist dataset):

| review_score | order_count | avg_item_price | total_revenue |
|---|---|---|---|
| 1 | 10,854 | 127.35 | 1,812,828.22 |
| 2 | 3,086 | 115.85 | 448,799.56 |
| 3 | 8,107 | 110.06 | 1,037,092.59 |
| 4 | 19,065 | 118.60 | 2,528,015.01 |
| 5 | 57,006 | 121.22 | 7,700,489.39 |

Discussion: items in 1-star orders are actually slightly more expensive on average (R$127.35) than 5-star orders (R$121.22). Does price drive dissatisfaction? What other factors might explain this?

Common mistake to watch for — **join fan-out**: this query joins two tables that both hold multiple rows per `order_id` (`order_items` and `order_reviews`). This is fine for *comparing* scores as the curriculum documents it, but 547 orders carry more than one review row, so those orders get counted under multiple scores and `total_revenue` is slightly inflated for them. When an exact number is required, pre-aggregate the non-base table in a `WITH` CTE first and use `COUNT(DISTINCT order_id)` — see the notebook's "Going Deeper" section for the safe pattern.

**Instructor note**: the demo notebook's automated validation flagged this exact query (Cell 10) under a static join-fan-out lint. This is a known, accepted exception — the query reproduces the curriculum's own verified numbers verbatim and cannot be rewritten without changing them. See `NEEDS_HUMAN_REVIEW.md` in the week folder.

---

## Group Exercise

Trace the chain, then predict the fan-out (~8 min, pairs/threes):
- **Part A** (ties to Concept 1): for a São Paulo seller, name the join chain from `order_items` to `product_category_translation` — which tables, which keys, how many `JOIN`s.
- **Part B** (ties to Concept 2): predict whether `COUNT(*)` over `orders JOIN order_payments` would be too high or too low relative to `COUNT(DISTINCT order_id)`, and roughly by how much, using the grain table in the notebook.

Expected outputs: see the notebook's Group Exercise section and the "Going Deeper" grain table (orders 99,441/99,441; order_items 112,650/98,666; order_payments 103,886/99,440; order_reviews 99,224/98,673).

---
