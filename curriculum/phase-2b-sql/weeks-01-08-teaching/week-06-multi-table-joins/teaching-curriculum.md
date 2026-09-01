## Week 6 — Multi-table Joins and Complex Aggregations

### Wednesday Session: Three-Table Joins

**Objective:** Combine 3+ tables to answer real business questions that no single table can answer.

---

**Business question:** What is the revenue by product category (in English)?

This requires joining: `order_items` → `products` → `product_category_translation`

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

**Expected top 10:**
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

---

**Business question:** Does price differ by review score?

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

**Expected output:**
| review_score | order_count | avg_item_price | total_revenue |
|---|---|---|---|
| 1 | 10,854 | 127.35 | 1,812,828.22 |
| 2 | 3,086 | 115.85 | 448,799.56 |
| 3 | 8,107 | 110.06 | 1,037,092.59 |
| 4 | 19,065 | 118.60 | 2,528,015.01 |
| 5 | 57,006 | 121.22 | 7,700,489.39 |

> **Discussion:** Items in 1-star orders are actually slightly more expensive on average (R$127.35) than 5-star orders (R$121.22). Does price drive dissatisfaction? What other factors might explain this?

---

### Thursday Session: Geographic Revenue Analysis

**Full pipeline: customer state + payment + delivery**

```sql
SELECT c.customer_state,
       COUNT(DISTINCT o.order_id) AS order_count,
       ROUND(SUM(op.payment_value), 2) AS total_payment_value,
       ROUND(AVG(op.payment_value), 2) AS avg_order_value,
       ROUND(AVG(
           julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)
       ), 1) AS avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_payment_value DESC
LIMIT 8
```

---

**Exercises:**

1. Build a 4-table join: orders → customers → order_items → sellers. Find average freight value paid by customers in each state when ordering from sellers in SP.

2. Which product categories are most popular in SP vs RJ? (orders → customers → order_items → products → translation). Show top 5 categories per state.

3. What is the total GMV (price + freight) per seller state? Join order_items with sellers.

4. Find categories where the average item price is above R$150. Show category name, count, avg price.

---

**Weekly Assignment:**

1. Build a complete category performance table: category name (English), order count, seller count, total revenue, avg price, avg review score. *(This requires a 4-table join: order_items + products + translation + order_reviews via orders)*
2. Which seller state has the highest average review score from their customers?
3. Find the 3 categories with the highest freight-to-price ratio (freight / price).
4. How many distinct products has each seller sold? Show top 10 sellers by product variety.
5. Challenge: Find orders where the delivery took longer than 30 days AND the review score was 1. How many are there?

---
