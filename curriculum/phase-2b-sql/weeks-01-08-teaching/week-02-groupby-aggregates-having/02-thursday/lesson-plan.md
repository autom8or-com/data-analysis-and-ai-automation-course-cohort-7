# Week 2 — GROUP BY, Aggregates & HAVING: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-02-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-02-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Apply GROUP BY and aggregate functions to analyse review score distribution; understand why average and distribution shape can diverge.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run the setup cell |
| 0:10–0:35 | Review score distribution | Demo `GROUP BY review_score` with COUNT and percentage-of-total |
| 0:35–0:55 | Overall average vs distribution | Demo the single `AVG(review_score)` query; discuss why 4.09 ≠ 5.0 despite 57.8% five-star |
| 0:55–1:15 | HAVING recap | Demo isolating high-count score buckets with `HAVING` |
| 1:15–1:45 | Group Exercise | Review Score Analysis — students work through Exercises 1–5 in pairs |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview next session (Week 3 — JOINs) |

---

## Key Concepts

### Review score distribution
`GROUP BY` with a correlated scalar subquery to compute each group's percentage of the whole table.

Expected outputs (verified against the Olist dataset):
- `SELECT review_score, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_reviews), 1) AS percentage FROM order_reviews GROUP BY review_score ORDER BY review_score` →
  1: 11,424 (11.5%) | 2: 3,151 (3.2%) | 3: 8,179 (8.2%) | 4: 19,142 (19.3%) | 5: 57,328 (57.8%)

Common mistake to watch for: forgetting `* 100.0` (or `* 1.0`) in the percentage calculation — SQLite truncates integer division, silently producing 0s or wrong rounding.

### Overall average review score
A single aggregate over the whole table, contrasted with the distribution above.

Expected outputs (verified against the Olist dataset):
- `SELECT ROUND(AVG(review_score), 2) AS overall_avg FROM order_reviews` → **4.09**

Discussion point: 57.8% of reviews are 5-star, yet the average is 4.09, not 5.0 — because 1-star reviews (11.5%) pull it down disproportionately. Compare to the Amazon Reviews dataset discussion from Phase 1.

---

## Group Exercise

**Exercises:**

**Exercise 1:** What is the average number of items per order?
```sql
SELECT ROUND(AVG(item_count), 2) AS avg_items_per_order
FROM (
    SELECT order_id, COUNT(*) AS item_count
    FROM order_items
    GROUP BY order_id
)
```

**Exercise 2:** Which customer state has the highest average review score?
```sql
-- Requires thinking — can't do this yet without JOINs. Note for next week.
-- This is a teaser exercise: discuss WHY this query can't be written yet.
```

**Exercise 3:** How many payment records use more than 6 installments?
```sql
SELECT COUNT(*) AS high_installment_count
FROM order_payments
WHERE payment_installments > 6
```

**Exercise 4:** What is the total freight revenue across all orders?
```sql
SELECT ROUND(SUM(freight_value), 2) AS total_freight_revenue
FROM order_items
```
**Expected: R$2,251,909.54**

**Exercise 5:** Find states where more than 3,000 customers placed orders.
```sql
SELECT customer_state, COUNT(*) AS order_count
FROM customers
GROUP BY customer_state
HAVING COUNT(*) > 3000
ORDER BY order_count DESC
```

**Expected outputs**: Exercise 4 is the only one with a curriculum-verified numeric answer (R$2,251,909.54); Exercises 1, 3, and 5 have no documented expected value and are for group discussion/derivation, not graded self-check. Exercise 2 is intentionally unanswerable with this week's tools — discuss why.

---

## Weekly Assignment

**Weekly Assignment:**

1. How many distinct product categories exist in the `products` table?
2. What is the most common payment installment count for credit card payments?
3. Build a query showing total `price` and total `freight_value` from `order_items` grouped by `seller_id`. Show only the top 5 sellers.
4. What is the total revenue (price only) from the `order_items` table? *(Expected: R$13,591,643.70)*
5. Challenge: Write a query showing review score counts where the count is between 5,000 and 25,000.

---
