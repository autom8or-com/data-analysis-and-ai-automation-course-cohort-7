## Week 5 — Subqueries and Window Functions

### Wednesday Session: Subqueries

**Objective:** Write queries that use the result of another query. Understand when subqueries are appropriate vs JOINs.

---

**Concept 1: Scalar subquery in WHERE**

```sql
-- Orders with payment value above average
SELECT COUNT(*) AS high_value_orders
FROM order_payments
WHERE payment_value > (SELECT AVG(payment_value) FROM order_payments)
```
**Expected: 31,012**

```sql
-- Verify the average
SELECT ROUND(AVG(payment_value), 2) AS avg_payment FROM order_payments
```
**Expected: R$154.10**

---

**Concept 2: Subquery in FROM clause**

```sql
-- Average items per order (can't do directly with one GROUP BY)
SELECT ROUND(AVG(item_count), 2) AS avg_items_per_order
FROM (
    SELECT order_id, COUNT(*) AS item_count
    FROM order_items
    GROUP BY order_id
)
```

---

**Concept 3: IN with subquery**

```sql
-- Delivered orders from SP customers
SELECT COUNT(*) AS sp_delivered
FROM orders
WHERE order_status = 'delivered'
  AND customer_id IN (
      SELECT customer_id FROM customers WHERE customer_state = 'SP'
  )
```
**Expected: 40,501**

> **Note on data quality:** The `products` table has misspelled columns — `product_name_lenght` and `product_description_lenght` (missing 'g'). This is real-world data. When querying these columns, you must use the actual names as they appear in the table.

```sql
-- Find products with NULL category
SELECT COUNT(*) AS null_category_products
FROM products
WHERE product_category_name IS NULL
```
**Expected: 610**

```sql
-- Products with NULL other fields
SELECT COUNT(*) AS null_weight
FROM products
WHERE product_weight_g IS NULL
```
**Expected: 2**

---

### Thursday Session: Window Functions

**Objective:** Compute rankings, running totals, and comparisons without losing row-level detail.

---

**Concept 4: RANK()**

```sql
-- Rank sellers by total revenue
SELECT seller_id,
       ROUND(SUM(price), 2) AS total_revenue,
       RANK() OVER (ORDER BY SUM(price) DESC) AS revenue_rank
FROM order_items
GROUP BY seller_id
LIMIT 10
```

**Top seller verified:** seller `4869f7a5dfa277a7dca6462dcf3b52b2` = R$229,472.63

---

**Concept 5: Running total with SUM() OVER**

```sql
-- Running total of orders through 2017
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       COUNT(*) AS monthly_orders,
       SUM(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', o.order_purchase_timestamp)) AS running_total
FROM orders o
WHERE strftime('%Y', o.order_purchase_timestamp) = '2017'
GROUP BY month
ORDER BY month
```

**Expected (selected rows):**
| month | monthly_orders | running_total |
|---|---|---|
| 2017-01 | 800 | 800 |
| 2017-06 | 3,245 | 14,611 |
| 2017-11 | 7,544 | 39,428 |
| 2017-12 | 5,673 | 45,101 |

---

**Concept 6: ROW_NUMBER() vs RANK()**

```sql
-- ROW_NUMBER: unique sequential number even with ties
SELECT customer_state,
       COUNT(*) AS order_count,
       ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_num
FROM customers
GROUP BY customer_state
ORDER BY order_count DESC
LIMIT 8
```

---

**Exercises:**

1. Find all sellers whose total revenue is above the average seller revenue (use subquery).
2. Rank customer states by average review score (join orders, customers, order_reviews first, then rank).
3. Compute a running total of payment revenue through 2018 (month by month).
4. Use ROW_NUMBER() to number each review within its review score group (partition by review_score).

---

**Weekly Assignment:**

1. Which states have more delivered orders than the national average by state?
2. Use RANK() to rank payment types by total revenue. Show rank, type, and total.
3. Build a monthly running total for order payments in 2017.
4. Find the top 20 sellers by item count. Do they also rank top 20 by revenue?
5. Challenge: Use a subquery to find products that have been sold more than the average product's sales count. How many such products exist?

---
