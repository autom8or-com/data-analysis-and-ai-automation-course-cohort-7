## Week 1 — SELECT, WHERE, ORDER BY, LIMIT

### Wednesday Session: Reading Data

**Objective:** Learn to retrieve and filter data. By end of session: students can write SELECT with WHERE, ORDER BY, and LIMIT from memory.

---

**Concept 1: SELECT — choosing columns**

```sql
-- All columns from orders
SELECT *
FROM orders
LIMIT 10
```

```sql
-- Specific columns only
SELECT order_id, customer_id, order_status
FROM orders
LIMIT 5
```

> **Instructor:** Show the difference between `SELECT *` and named columns. Ask: why might `SELECT *` be a bad habit in production databases?

---

**Concept 2: WHERE — filtering rows**

```sql
-- Delivered orders only
SELECT order_id, customer_id, order_status
FROM orders
WHERE order_status = 'delivered'
LIMIT 10
```

**Verify:**
```sql
SELECT COUNT(*) AS total
FROM orders
WHERE order_status = 'delivered'
```
**Expected: 96,478**

```sql
SELECT COUNT(*) AS total
FROM orders
WHERE order_status = 'canceled'
```
**Expected: 625**

```sql
SELECT COUNT(*) AS total
FROM orders
WHERE order_status != 'delivered'
```
**Expected: 2,963**

---

**Concept 3: AND / OR in WHERE**

```sql
-- Orders that are either canceled or unavailable
SELECT order_id, order_status
FROM orders
WHERE order_status = 'canceled'
   OR order_status = 'unavailable'
LIMIT 10
```

```sql
-- Verify: count both statuses
SELECT COUNT(*) AS total
FROM orders
WHERE order_status = 'canceled'
   OR order_status = 'unavailable'
```
**Expected: 1,234** (625 canceled + 609 unavailable)

---

**Concept 4: ORDER BY and LIMIT**

```sql
-- Highest payment values first
SELECT order_id, payment_type, payment_value
FROM order_payments
ORDER BY payment_value DESC
LIMIT 10
```

```sql
-- Cheapest items first
SELECT order_id, price, freight_value
FROM order_items
ORDER BY price ASC
LIMIT 10
```

---

### Thursday Session: Filtered Exploration

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

---

**Weekly Assignment:**

Write SQL queries to answer:
1. How many orders were placed in total? *(Answer: 99,441)*
2. How many orders are NOT delivered? *(Answer: 2,963)*
3. List the 3 payment types available in the data. What is the rarest?
4. How many sellers are there? *(Answer: 3,095)*
5. Write a query that finds all customers in the city of `sao paulo` (lowercase — check the data).

---
