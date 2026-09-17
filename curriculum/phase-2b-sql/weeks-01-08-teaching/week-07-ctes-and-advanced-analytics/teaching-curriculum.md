## Week 7 — CTEs and Advanced Analytics

### Wednesday Session: Common Table Expressions (CTEs)

**Objective:** Use CTEs to break complex queries into readable, named steps.

---

**Concept 1: Basic CTE**

```sql
-- CTE: state-level revenue summary
WITH customer_orders AS (
    SELECT c.customer_state,
           COUNT(o.order_id) AS total_orders,
           ROUND(SUM(op.payment_value), 2) AS total_spent
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state
)
SELECT customer_state,
       total_orders,
       total_spent,
       ROUND(total_spent / total_orders, 2) AS avg_order_value
FROM customer_orders
ORDER BY total_spent DESC
LIMIT 8
```

**Expected top 3:**
| customer_state | total_orders | total_spent | avg_order_value |
|---|---|---|---|
| SP | 42,308 | 5,770,266.19 | 136.39 |
| RJ | 13,004 | 2,055,690.45 | 158.08 |
| MG | 11,804 | 1,819,277.61 | 154.12 |

---

**Concept 2: Multi-step CTE — Seller Tiers**

```sql
WITH seller_revenue AS (
    SELECT seller_id,
           ROUND(SUM(price), 2) AS total_revenue,
           COUNT(*) AS items_sold
    FROM order_items
    GROUP BY seller_id
),
seller_tiers AS (
    SELECT seller_id,
           total_revenue,
           items_sold,
           CASE
               WHEN total_revenue >= 100000 THEN 'Top Seller'
               WHEN total_revenue >= 50000 THEN 'High Performer'
               WHEN total_revenue >= 10000 THEN 'Mid Tier'
               ELSE 'Standard'
           END AS tier
    FROM seller_revenue
)
SELECT tier,
       COUNT(*) AS seller_count,
       ROUND(AVG(total_revenue), 2) AS avg_revenue,
       ROUND(SUM(total_revenue), 2) AS tier_total_revenue
FROM seller_tiers
GROUP BY tier
ORDER BY avg_revenue DESC
```

**Expected output:**
| tier | seller_count | avg_revenue | tier_total_revenue |
|---|---|---|---|
| Top Seller | 18 | 149,574.75 | 2,692,345.55 |
| High Performer | 22 | 60,117.14 | 1,322,577.15 |
| Mid Tier | 252 | 19,812.97 | 4,992,867.56 |
| Standard | 2,803 | 1,635.34 | 4,583,853.44 |

> **Business insight:** 18 top sellers generate R$2.7M in revenue. 2,803 standard sellers generate R$4.6M combined. The top 18 (0.6% of sellers) generate nearly 20% of total product revenue.

---

### Thursday Session: Advanced Analytics — DeepSeek Guided

**Business questions to answer using CTEs + Window Functions:**

**Question 1:** For each month, what was the growth rate in orders compared to the previous month?

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

---

**Question 2:** What percentage of total platform revenue does each product category represent?

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

---

**Exercises:**

1. Build a CTE that calculates average delivery days per seller state, then rank states by speed (fastest first).

2. Multi-CTE: first calculate total items sold per product, then classify into 'Best Seller' (>100 items), 'Good Seller' (50–100), 'Low Volume' (<50). Report counts per tier.

3. Using LAG(): calculate month-over-month revenue growth using order_payments. Were there any months with negative growth?

4. CTE + Window: For each review score, calculate: count of reviews, % of total reviews, and running % total (cumulative from score 1 upward).

---

**Weekly Assignment:**

1. Full seller analysis CTE: revenue, items sold, avg price, avg review score, tier classification. Show all 4 tiers with summary stats.
2. Which product categories showed month-over-month growth in orders for every month of 2018?
3. Using NTILE(4), split sellers into quartiles by revenue. What is the total revenue per quartile?
4. CTE: Find the top 3 product categories by revenue in each customer state (SP, RJ, MG, RS, PR).
5. Challenge: Build a "customer lifetime value" proxy — for each state, compute: total orders, total spent, avg days between orders (if they had multiple). Which state has the highest avg spend per customer?

---
