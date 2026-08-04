## Week 3 — JOINs

### Wednesday Session: Connecting Tables

**Objective:** Learn INNER JOIN and LEFT JOIN. By end of session: students can join two tables and filter/group across both.

---

**Concept 1: INNER JOIN**

The `orders` table has `customer_id` but not the customer's state. The `customers` table has the state. Join them:

```sql
SELECT o.order_id, o.order_status, c.customer_state, c.customer_city
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LIMIT 10
```

> **Note:** `JOIN` and `INNER JOIN` are identical in SQLite. Always use table aliases (o, c) when joining — it prevents column name conflicts and makes queries readable.

---

**Delivered orders by state:**

```sql
SELECT c.customer_state, COUNT(*) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY order_count DESC
LIMIT 5
```

**Expected top 5:**
| customer_state | order_count |
|---|---|
| SP | 40,501 |
| RJ | 12,350 |
| MG | 11,354 |
| RS | 5,345 |
| PR | 4,923 |

---

**Sellers and their revenue:**

```sql
SELECT oi.seller_id, s.seller_state,
       COUNT(*) AS items_sold,
       ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY oi.seller_id, s.seller_state
ORDER BY total_revenue DESC
LIMIT 10
```

---

**Revenue by seller state:**

```sql
SELECT s.seller_state,
       COUNT(DISTINCT oi.seller_id) AS seller_count,
       ROUND(SUM(oi.price), 2) AS total_revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_state
ORDER BY total_revenue DESC
LIMIT 8
```

**Expected top 5:**
| seller_state | seller_count | total_revenue |
|---|---|---|
| SP | 1,849 | 8,753,396.21 |
| PR | 349 | 1,261,887.21 |
| MG | 244 | 1,011,564.74 |
| RJ | 171 | 843,984.22 |
| SC | 190 | 632,426.07 |

---

### Thursday Session: LEFT JOIN and NULL Handling

**Concept 2: LEFT JOIN — keeping all rows from the left table**

```sql
-- Find orders that have NO items in order_items
SELECT COUNT(*) AS orders_without_items
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL
```
**Expected: 775**

> **Discussion:** 775 orders have no items. These likely correspond to canceled or unavailable orders. This is why LEFT JOIN is valuable — an INNER JOIN would silently drop these rows.

---

**Verify: what statuses do these 775 orders have?**

```sql
SELECT o.order_status, COUNT(*) AS count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL
GROUP BY o.order_status
ORDER BY count DESC
```

---

**Three-table join (preview):**

```sql
-- Orders with customer state AND payment type
SELECT o.order_id, c.customer_state, op.payment_type, op.payment_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.order_status = 'delivered'
LIMIT 10
```

---

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

---

**Weekly Assignment:**

1. Join `orders` and `customers`. Count total orders per city. Show only cities with 500+ orders.
2. Join `order_items` and `sellers`. What is the total freight value by seller state? Show top 5.
3. LEFT JOIN: find orders that have a review score of 1 but were still delivered (join `orders` and `order_reviews`).
4. What is the most common payment type used by customers in `RJ`? (3-table join: orders + customers + order_payments)
5. Challenge: How many orders have both a review AND an item record? Use JOIN and compare to total orders.

