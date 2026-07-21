# Week 1 — SELECT, WHERE & ORDER BY: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-01-thu-demo.ipynb`
- [ ] `sql_setup.py` first cell runs and loads all 8 tables into `/content/olist.db`
- [ ] Student exercise link ready to share: `week-01-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Apply SELECT/WHERE/ORDER BY/LIMIT independently to answer business questions (group work)

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py` |
| 0:10–0:45 | Filtered exploration demo | New tables: `order_items`, `order_payments`, `customers`, `order_reviews` |
| 0:45–1:15 | Group Exercise | Filtered Exploration — 5 questions, 10 minutes each, verify answers as class |
| 1:15–1:45 | Debrief | Walk through each question's correct query and expected value together |
| 1:45–2:00 | Wrap-up & preview | Assign weekly assignment, preview Week 2 (GROUP BY, Aggregates, HAVING) |

---

## Key Concepts

Thursday reinforces Wednesday's clauses (`SELECT`, `WHERE`, `ORDER BY`, `LIMIT`) applied to four new tables: `order_items`, `order_payments`, `customers`, `order_reviews`.

Common mistake to watch for: `ORDER BY ... LIMIT` without an explicit sort direction can silently return the wrong "top" rows — always state `ASC`/`DESC`.

---

## Group Exercise

**Exercises (group work — 10 minutes each, verify answers as class):**

**Exercise 1:** How many orders have a NULL delivery date?
```sql
SELECT COUNT(*) AS null_delivery
FROM orders
WHERE order_delivered_customer_date IS NULL
```
**Expected: 2,965**

**Exercise 2:** List the 5 most expensive individual items (by price) from `order_items`.
```sql
SELECT order_id, product_id, price
FROM order_items
ORDER BY price DESC
LIMIT 5
```

**Exercise 3:** How many payments were made by `boleto`?
```sql
SELECT COUNT(*) AS boleto_count
FROM order_payments
WHERE payment_type = 'boleto'
```
**Expected: 19,784**

**Exercise 4:** How many customers are in the state of `SP`?
```sql
SELECT COUNT(*) AS sp_customers
FROM customers
WHERE customer_state = 'SP'
```
**Expected: 41,746**

**Exercise 5:** List the first 10 reviews with a score of 1 (the worst reviews). What column would contain the customer comment?
```sql
SELECT order_id, review_score, review_comment_message
FROM order_reviews
WHERE review_score = 1
LIMIT 10
```

**Expected outputs**: Exercise 1 → 2,965; Exercise 3 → 19,784; Exercise 4 → 41,746. Exercises 2 and 5 are open-ended list queries (verify row count and sort/filter correctness rather than a fixed number).

---

## Weekly Assignment

Write SQL queries to answer:
1. How many orders were placed in total? *(Answer: 99,441)*
2. How many orders are NOT delivered? *(Answer: 2,963)*
3. List the 3 payment types available in the data. What is the rarest?
4. How many sellers are there? *(Answer: 3,095)*
5. Write a query that finds all customers in the city of `sao paulo` (lowercase — check the data).

---
