# Week 3 — JOINs: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-03-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-03-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Learn LEFT JOIN and NULL handling across joined tables; combine three tables in one query.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run the setup cell |
| 0:10–0:35 | LEFT JOIN — keeping unmatched rows | Demo finding the 775 orders with no items via `LEFT JOIN ... WHERE oi.order_id IS NULL` |
| 0:35–0:55 | Anti-join as a data-quality tool | Demo grouping the 775 order-less orders by status; discuss why INNER JOIN would have silently hidden them |
| 0:55–1:15 | Three-table joins | Demo `orders` + `customers` + `order_payments` in one query; going deeper into `IS NULL` vs `= NULL` and `LEFT JOIN` accidentally demoted to `INNER JOIN` by a `WHERE` on the right table |
| 1:15–1:45 | Group Exercise | Students work through Exercises 1–5 in pairs |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview next session (Week 4 — CASE WHEN, string & date functions, DeepSeek intro) |

---

## Key Concepts

### LEFT JOIN — keeping all rows from the left table
`LEFT JOIN` keeps every row from `orders` even when there's no matching `order_items` row; the anti-join pattern (`LEFT JOIN ... WHERE right.key IS NULL`) isolates exactly the unmatched rows.

Expected outputs (verified against the Olist dataset):
- `SELECT COUNT(*) AS orders_without_items FROM orders o LEFT JOIN order_items oi ON o.order_id = oi.order_id WHERE oi.order_id IS NULL` → **775**

Discussion point: 775 orders have no items — these likely correspond to canceled or unavailable orders. An `INNER JOIN` would have silently dropped these rows instead of surfacing them.

### Verify: statuses of orderless orders
Grouping the anti-join result by `order_status` to confirm the hypothesis above.

Expected outputs (verified against the Olist dataset):
- `SELECT o.order_status, COUNT(*) AS count FROM orders o LEFT JOIN order_items oi ON o.order_id = oi.order_id WHERE oi.order_id IS NULL GROUP BY o.order_status ORDER BY count DESC` → status breakdown of the 775 order-less orders (no single curriculum-verified figure per status; the total across statuses must sum to 775).

### Three-table join (preview)
Chaining two `JOIN`s in one query — `orders` → `customers` → `order_payments` — to pull customer geography and payment details together.

Expected outputs (verified against the Olist dataset):
- `SELECT o.order_id, c.customer_state, op.payment_type, op.payment_value FROM orders o JOIN customers c ON o.customer_id = c.customer_id JOIN order_payments op ON o.order_id = op.order_id WHERE o.order_status = 'delivered' LIMIT 10` → 10 rows combining order, customer, and payment columns.

Common mistake to watch for: writing `... = NULL` or `... != NULL` instead of `IS NULL` / `IS NOT NULL` — SQL's three-valued logic means `= NULL` never matches, silently returning zero rows instead of an error. Also watch for a `WHERE` clause on the right-hand table of a `LEFT JOIN` (e.g. filtering on an `order_items` column) accidentally demoting it back to an `INNER JOIN` by discarding the NULL-filled unmatched rows — filter conditions on the outer table belong in the `ON` clause, not `WHERE`, if the unmatched rows must be kept.

---

## Group Exercise

**Exercises:**

**Exercise 1:** How many delivered orders came from customers in `MG`?
```sql
SELECT COUNT(*) AS mg_delivered
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND c.customer_state = 'MG'
```
**Expected: 11,354**

**Exercise 2:** What is the average payment value for orders from `SP` customers?
```sql
SELECT ROUND(AVG(op.payment_value), 2) AS avg_payment
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
WHERE c.customer_state = 'SP'
```

**Exercise 3:** How many sellers are in each state? Show only states with 50+ sellers.
```sql
SELECT seller_state, COUNT(*) AS seller_count
FROM sellers
GROUP BY seller_state
HAVING COUNT(*) >= 50
ORDER BY seller_count DESC
```

**Exercise 4:** Do orders with reviews have different average item prices than orders without reviews? (Think through the JOIN type needed before writing.)

**Exercise 5:** Join `order_items` with `order_reviews` on `order_id`. Find the average item price for each review score (1–5).
```sql
SELECT r.review_score,
       COUNT(DISTINCT oi.order_id) AS order_count,
       ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY r.review_score
ORDER BY r.review_score
```

**Expected outputs**: Exercise 1 is the only one with a curriculum-verified numeric answer (11,354). Exercises 2, 3, and 5 have no documented expected value and are for group discussion/derivation, not graded self-check — note that Exercise 5's naive join (`order_items` directly to `order_reviews`) fans out rows because both tables carry many rows per `order_id`; the correct approach pre-aggregates each side to one row per `order_id` (e.g. in a CTE) before joining. Exercise 4 is intentionally open-ended — discuss why a `LEFT JOIN` (not `INNER JOIN`) is required to compare reviewed vs. unreviewed orders.

---

## Weekly Assignment

**Weekly Assignment:**

1. Join `orders` and `customers`. Count total orders per city. Show only cities with 500+ orders.
2. Join `order_items` and `sellers`. What is the total freight value by seller state? Show top 5.
3. LEFT JOIN: find orders that have a review score of 1 but were still delivered (join `orders` and `order_reviews`).
4. What is the most common payment type used by customers in `RJ`? (3-table join: orders + customers + order_payments)
5. Challenge: How many orders have both a review AND an item record? Use JOIN and compare to total orders.

---
