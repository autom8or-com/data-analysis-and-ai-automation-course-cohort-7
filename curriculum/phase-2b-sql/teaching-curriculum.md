# Phase 2b — SQL Teaching Curriculum
## PORA Academy Cohort 7 | 8 Weeks

**Duration:** 8 weeks (Wed + Thu × 2-hour sessions)
**Database:** SQLite (via Google Colab — no installation required)
**Dataset:** Olist Brazilian E-Commerce Dataset (11 tables, 99,441 orders)
**AI Tool:** DeepSeek (introduced Week 4, after 3-week foundation)
**Prerequisite:** Phase 2a Python complete

> **Curriculum principle:** Every query, every expected output, and every verified number in this document was produced by running SQL against the actual Olist dataset using SQLite. No answer is assumed or estimated.

---

## Dataset Overview (Verified)

| Table | Rows | Key Columns |
|---|---|---|
| `orders` | 99,441 | order_id, customer_id, order_status, order_purchase_timestamp, order_delivered_customer_date, order_estimated_delivery_date |
| `customers` | 99,441 | customer_id, customer_state, customer_city |
| `order_items` | 112,650 | order_id, product_id, seller_id, price, freight_value |
| `order_payments` | 103,886 | order_id, payment_type, payment_value, payment_installments |
| `order_reviews` | 99,224 | order_id, review_score, review_comment_message |
| `products` | 32,951 | product_id, product_category_name, product_name_lenght* |
| `sellers` | 3,095 | seller_id, seller_state |
| `product_category_translation` | 71 | product_category_name, product_category_name_english |

> **Data quality note:** The `products` table has two misspelled columns — `product_name_lenght` and `product_description_lenght` (missing the 'g'). This is a real-world data quality issue and is used as a teaching moment in Week 5.

### Key Verified Stats
| Fact | Value |
|---|---|
| Total orders | 99,441 |
| Delivered orders | 96,478 |
| Canceled orders | 625 |
| Orders with NULL delivery date | 2,965 |
| Top customer state | SP = 41,746 orders |
| Avg payment value | R$154.10 |
| Credit card % (by count) | 73.9% (76,795 of 103,886) |
| Overall avg review score | 4.09 |
| 5-star reviews | 57,328 (57.8%) |
| Total GMV (price + freight) | R$15,843,553.24 |
| Product revenue only | R$13,591,643.70 |
| Avg delivery days | 12.6 days |
| Late deliveries | 7,826 (8.1% of delivered) |
| Products with null category | 610 |
| 2016 orders | 329 (incomplete year) |
| 2017 orders | 45,101 |
| 2018 orders | 54,011 |
| November 2017 orders | 7,544 (Black Friday peak) |
| Top seller revenue | R$229,472.63 |
| Top category (English) | health_beauty = R$1,258,681.34 |

---

## Colab Setup (Used Every Session)

Students run this block at the start of every session:

```python
import sqlite3
import pandas as pd
import os

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

DATA_DIR = "/content/drive/MyDrive/cohort7/datasets/olist"

# Load all tables into SQLite in-memory database
conn = sqlite3.connect(":memory:")

tables = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
}

for table_name, filename in tables.items():
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {len(df):,} rows")

print("\nDatabase ready.")
```

**Verify output:**
```
Loaded orders: 99,441 rows
Loaded customers: 99,441 rows
Loaded order_items: 112,650 rows
Loaded order_payments: 103,886 rows
Loaded order_reviews: 99,224 rows
Loaded products: 32,951 rows
Loaded sellers: 3,095 rows
Loaded product_category_translation: 71 rows
Database ready.
```

### How to Run Queries

```python
# Template — use this pattern for every query in this course
result = pd.read_sql("""
    SELECT *
    FROM orders
    LIMIT 5
""", conn)
result
```

---

## WEEKS 1–3: FOUNDATION (No AI Assistance)

> Students must attempt all exercises independently. DeepSeek is not introduced until Week 4. The goal is to build genuine SQL intuition before AI shortcuts become available.

---

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

## Week 2 — GROUP BY, Aggregates, HAVING

### Wednesday Session: Summarising Data

**Objective:** Learn to compute summaries across groups. By end of session: students can write GROUP BY with SUM, COUNT, AVG, MIN, MAX, and filter groups with HAVING.

---

**Concept 1: COUNT with GROUP BY**

```sql
-- Count orders by status
SELECT order_status, COUNT(*) AS count
FROM orders
GROUP BY order_status
ORDER BY count DESC
```

**Expected output:**
| order_status | count |
|---|---|
| delivered | 96,478 |
| shipped | 1,107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |

---

**Concept 2: SUM, AVG, MIN, MAX**

```sql
-- Payment summary by type
SELECT payment_type,
       COUNT(*) AS transaction_count,
       ROUND(AVG(payment_value), 2) AS avg_value,
       ROUND(SUM(payment_value), 2) AS total_value,
       ROUND(MIN(payment_value), 2) AS min_value,
       ROUND(MAX(payment_value), 2) AS max_value
FROM order_payments
GROUP BY payment_type
ORDER BY transaction_count DESC
```

**Expected output:**
| payment_type | transaction_count | avg_value | total_value |
|---|---|---|---|
| credit_card | 76,795 | 163.32 | 12,542,084.19 |
| boleto | 19,784 | 145.03 | 2,869,361.27 |
| voucher | 5,775 | 65.70 | 379,436.87 |
| debit_card | 1,529 | 142.57 | 217,989.79 |
| not_defined | 3 | 0.00 | 0.00 |

---

**Concept 3: Counting customers by state**

```sql
SELECT customer_state, COUNT(*) AS order_count
FROM customers
GROUP BY customer_state
ORDER BY order_count DESC
LIMIT 10
```

**Expected top 5:**
| customer_state | order_count |
|---|---|
| SP | 41,746 |
| RJ | 12,852 |
| MG | 11,635 |
| RS | 5,466 |
| PR | 5,045 |

---

**Concept 4: HAVING — filtering groups**

> `WHERE` filters rows before grouping. `HAVING` filters groups after grouping.

```sql
-- Only payment types with more than 5,000 transactions
SELECT payment_type, COUNT(*) AS count
FROM order_payments
GROUP BY payment_type
HAVING COUNT(*) > 5000
ORDER BY count DESC
```

**Expected output:**
| payment_type | count |
|---|---|
| credit_card | 76,795 |
| boleto | 19,784 |
| voucher | 5,775 |

---

### Thursday Session: Review Score Analysis

**Review score distribution:**

```sql
SELECT review_score,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_reviews), 1) AS percentage
FROM order_reviews
GROUP BY review_score
ORDER BY review_score
```

**Expected output:**
| review_score | count | percentage |
|---|---|---|
| 1 | 11,424 | 11.5% |
| 2 | 3,151 | 3.2% |
| 3 | 8,179 | 8.2% |
| 4 | 19,142 | 19.3% |
| 5 | 57,328 | 57.8% |

```sql
-- Overall average
SELECT ROUND(AVG(review_score), 2) AS overall_avg
FROM order_reviews
```
**Expected: 4.09**

> **Discussion:** 57.8% of reviews are 5-star. Yet the average is 4.09, not 5.0 — because 1-star reviews (11.5%) pull it down disproportionately. How does this compare to the Amazon Reviews dataset from Phase 1?

---

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

---

**Weekly Assignment:**

1. How many distinct product categories exist in the `products` table?
2. What is the most common payment installment count for credit card payments?
3. Build a query showing total `price` and total `freight_value` from `order_items` grouped by `seller_id`. Show only the top 5 sellers.
4. What is the total revenue (price only) from the `order_items` table? *(Expected: R$13,591,643.70)*
5. Challenge: Write a query showing review score counts where the count is between 5,000 and 25,000.

---

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

---

## WEEKS 4–8: DEEPSEEK-ASSISTED LEARNING

> At the start of Week 4, DeepSeek is formally introduced. The same 5-minute rule from Python applies: always attempt the query independently first, then use DeepSeek for guidance. Always verify DeepSeek output against the expected values in this curriculum.

### DeepSeek Protocol for SQL

**Prompt template:**
> *"I am working with an SQLite database with these tables: [table names and key columns]. I need to write a SQL query to [describe the business question]. The tool is SQLite — please avoid MySQL/PostgreSQL-specific syntax. Show me the query and explain each clause."*

**5-minute rule:** Spend 5 minutes writing the query yourself. Use DeepSeek only when stuck. Always verify the result matches the expected output.

**Verification principle:** If DeepSeek generates a query that returns a different number than verified expected output, the query is wrong — debug it, don't accept it.

---

## Week 4 — CASE WHEN, String Functions, Date Functions

### Wednesday Session: Conditional Logic with CASE WHEN

**Objective:** Classify and group data using conditional SQL. Build business categories directly in SQL.

---

**Concept 1: CASE WHEN**

```sql
-- Classify order statuses into business categories
SELECT order_status,
       CASE
           WHEN order_status = 'delivered' THEN 'Completed'
           WHEN order_status IN ('shipped', 'invoiced', 'processing', 'approved') THEN 'In Progress'
           WHEN order_status = 'canceled' THEN 'Canceled'
           ELSE 'Other'
       END AS status_group,
       COUNT(*) AS count
FROM orders
GROUP BY order_status
ORDER BY count DESC
```

**Expected output:**
| order_status | status_group | count |
|---|---|---|
| delivered | Completed | 96,478 |
| shipped | In Progress | 1,107 |
| canceled | Canceled | 625 |
| unavailable | Other | 609 |
| invoiced | In Progress | 314 |
| processing | In Progress | 301 |

---

**Classify payment values:**

```sql
SELECT
    CASE
        WHEN payment_value < 50 THEN 'Low (< R$50)'
        WHEN payment_value < 200 THEN 'Mid (R$50–200)'
        WHEN payment_value < 500 THEN 'High (R$200–500)'
        ELSE 'Premium (R$500+)'
    END AS value_category,
    COUNT(*) AS count,
    ROUND(AVG(payment_value), 2) AS avg_value
FROM order_payments
GROUP BY value_category
ORDER BY avg_value
```

---

### Thursday Session: Date Functions

**Objective:** Extract year, month, and compute date differences in SQLite.

---

**Concept 2: Date extraction with strftime()**

> In SQLite, dates are stored as text (ISO format). Use `strftime()` to extract parts.

```sql
-- Orders by year
SELECT strftime('%Y', order_purchase_timestamp) AS year,
       COUNT(*) AS order_count
FROM orders
GROUP BY year
ORDER BY year
```

**Expected output:**
| year | order_count |
|---|---|
| 2016 | 329 |
| 2017 | 45,101 |
| 2018 | 54,011 |

> **Note:** 2016 has only 329 orders — the dataset starts in September 2016. This is an incomplete year and should not be compared directly to 2017/2018.

---

**Monthly orders — 2017 only:**

```sql
SELECT strftime('%Y-%m', order_purchase_timestamp) AS month,
       COUNT(*) AS orders
FROM orders
WHERE strftime('%Y', order_purchase_timestamp) = '2017'
GROUP BY month
ORDER BY month
```

**Expected — full 2017:**
| month | orders |
|---|---|
| 2017-01 | 800 |
| 2017-02 | 1,780 |
| 2017-03 | 2,682 |
| 2017-04 | 2,404 |
| 2017-05 | 3,700 |
| 2017-06 | 3,245 |
| 2017-07 | 4,026 |
| 2017-08 | 4,331 |
| 2017-09 | 4,285 |
| 2017-10 | 4,631 |
| 2017-11 | **7,544** |
| 2017-12 | 5,673 |

> **Discussion:** November 2017 = 7,544 orders — the Black Friday peak. This is nearly 2× the typical month. Same pattern seen in Python curriculum.

---

**Concept 3: Date difference — delivery time**

```sql
-- Average delivery days (delivered orders only)
SELECT ROUND(AVG(
    julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
), 1) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_status = 'delivered'
```
**Expected: 12.6 days**

```sql
-- Late deliveries: delivered after estimated date
SELECT COUNT(*) AS late_orders
FROM orders
WHERE order_delivered_customer_date > order_estimated_delivery_date
  AND order_status = 'delivered'
```
**Expected: 7,826** (8.1% of delivered orders)

---

**Exercises:**

1. Classify customers into geographic regions using CASE WHEN:
   - Southeast: SP, RJ, MG, ES
   - South: RS, SC, PR
   - Northeast: BA, CE, PE, MA, RN, PB, AL, SE, PI
   - Other: everything else

2. How many orders were placed on weekends vs weekdays? *(Hint: `strftime('%w', ...)` returns 0=Sunday, 6=Saturday)*

3. What is the average delivery time by customer state? Show the 5 fastest and 5 slowest states.

4. Create a query that shows for each month of 2018: order count, total revenue from `order_payments`, and a CASE WHEN flag for whether it was a "peak month" (≥6,000 orders).

---

**Weekly Assignment:**

1. Build a complete status summary: count and % of each status_group (Completed / In Progress / Canceled / Other).
2. What is the average delivery time for SP vs RJ customers?
3. How many orders were delivered within 7 days? Within 14 days? Over 30 days?
4. Build a month-by-month table for all of 2017 and 2018. Which month had the highest order count?
5. Challenge: Create a CASE WHEN that classifies delivery as 'Fast' (≤7 days), 'Standard' (8–14 days), 'Slow' (15–30 days), 'Very Slow' (>30 days). Count orders in each category.

---

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

## Week 8 — End-to-End Business Analysis (Capstone Week)

### Wednesday Session: The Full Pipeline

**Objective:** Combine all skills — JOINs, CTEs, Window Functions, CASE WHEN, Date functions — into a single coherent business analysis. Students work in groups.

---

**The Business Brief:**
> *You are a data analyst presenting to Olist's leadership team. They want to understand: (1) How has the platform grown? (2) Which sellers drive the most value? (3) Which product categories are the real revenue drivers? (4) How does delivery performance affect customer satisfaction? Your analysis must be SQL-only and all numbers must be verified.*

---

**Analysis 1: Platform Growth (2017 vs 2018)**

```sql
WITH yearly_summary AS (
    SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
           COUNT(DISTINCT o.order_id) AS total_orders,
           ROUND(SUM(op.payment_value), 2) AS total_revenue,
           ROUND(AVG(op.payment_value), 2) AS avg_order_value,
           COUNT(DISTINCT o.customer_id) AS unique_customers
    FROM orders o
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE strftime('%Y', o.order_purchase_timestamp) IN ('2017', '2018')
    GROUP BY year
)
SELECT year, total_orders, total_revenue, avg_order_value, unique_customers
FROM yearly_summary
ORDER BY year
```

---

**Analysis 2: Delivery Performance by State**

```sql
WITH delivery_stats AS (
    SELECT c.customer_state,
           COUNT(*) AS delivered_orders,
           ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_days,
           SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS late_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY c.customer_state
)
SELECT customer_state,
       delivered_orders,
       avg_days,
       late_count,
       ROUND(late_count * 100.0 / delivered_orders, 1) AS late_pct,
       ROUND(AVG(avg_days) OVER (), 1) AS national_avg_days
FROM delivery_stats
ORDER BY avg_days ASC
LIMIT 10
```

---

**Analysis 3: Review Score and Delivery Relationship**

```sql
WITH delivery_and_review AS (
    SELECT r.review_score,
           ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_delivery_days,
           COUNT(*) AS order_count,
           SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS late_count
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY r.review_score
)
SELECT review_score, avg_delivery_days, order_count,
       ROUND(late_count * 100.0 / order_count, 1) AS late_pct
FROM delivery_and_review
ORDER BY review_score
```

---

### Thursday Session: Presentation Preparation

**Groups prepare a 10-minute SQL-driven business analysis presentation.**

Each group must produce (in SQL only — no pandas manipulation beyond display):
1. Platform overview KPIs (total orders, total revenue, avg order value, delivered %)
2. Top 5 product categories by revenue
3. Seller tier breakdown (use the CTE from Week 7)
4. Delivery performance: avg days, late %, review score correlation
5. One additional business question chosen by the group

**Verified KPIs for final check:**

```sql
-- Final verification query — all numbers must match
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS canceled,
    ROUND(SUM(CASE WHEN order_status = 'delivered' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS delivered_pct
FROM orders
```

**Expected:**
| total_orders | delivered | canceled | delivered_pct |
|---|---|---|---|
| 99,441 | 96,478 | 625 | 97.0% |

```sql
-- Total GMV verification
SELECT ROUND(SUM(price), 2) AS product_revenue,
       ROUND(SUM(freight_value), 2) AS freight_revenue,
       ROUND(SUM(price + freight_value), 2) AS total_gmv
FROM order_items
```

**Expected:**
| product_revenue | freight_revenue | total_gmv |
|---|---|---|
| 13,591,643.70 | 2,251,909.54 | 15,843,553.24 |

---

## Summary of Key SQL Skills by Week

| Week | Skills | Key Business Questions |
|---|---|---|
| 1 | SELECT, WHERE, ORDER BY, LIMIT | What orders exist? Filter by status. |
| 2 | GROUP BY, Aggregates, HAVING | How many orders per status/state? Payment totals by type. |
| 3 | INNER JOIN, LEFT JOIN | Orders + customer location. Seller revenue. Unmatched records. |
| 4 | CASE WHEN, Date functions | Classify order values. Monthly trends. Delivery time. |
| 5 | Subqueries, RANK, Running totals | Above-average payers. Seller rankings. Cumulative growth. |
| 6 | 3+ table JOINs, Complex aggregations | Category revenue (English names). Price vs review score. |
| 7 | CTEs, LAG, NTILE | Seller tiers. Month-over-month growth. Revenue share. |
| 8 | End-to-end analysis | Full business intelligence pipeline. |

---

## Common Mistakes and Instructor Notes

### Week 1–2
- **Forgetting quotes around string values:** `WHERE order_status = delivered` fails; need single quotes: `'delivered'`
- **COUNT(*) vs COUNT(column):** `COUNT(*)` counts all rows including NULLs. `COUNT(column)` skips NULLs. Show this with `review_comment_message` which has many nulls.
- **WHERE vs HAVING:** Students frequently try to filter groups with WHERE. Use the payment type example (HAVING COUNT > 5000) to reinforce.

### Week 3
- **ON vs WHERE for filters:** Filtering in the ON clause vs WHERE clause produces different results with LEFT JOIN. Always demonstrate with the 775 orders-without-items example.
- **Aliases are required with self-referencing:** When joining a table to itself (not in this curriculum), aliases prevent ambiguity.
- **INNER JOIN silently drops unmatched rows:** Use the 775 missing-items example to prove this point visually.

### Week 4
- **SQLite dates are stored as text:** Students from MySQL backgrounds try `YEAR()` or `MONTH()` — these don't exist in SQLite. Only `strftime()` works.
- **julianday() for date math:** This is the SQLite-specific way to compute date differences. R$14 to days: `julianday(date2) - julianday(date1)`
- **2016 data is incomplete:** Only 329 orders vs 45,101 in 2017. Warn students not to include 2016 in year-over-year growth calculations.

### Week 5–6
- **Subquery performance:** For large datasets, JOINs often outperform subqueries. In this dataset, both work fine — but introduce the concept.
- **Product column typo:** `product_name_lenght` — students will inevitably make an error here. Remind them to always inspect column names before writing queries.
- **610 products with NULL category:** These won't appear in category revenue analysis when using INNER JOIN with the translation table. Should they be handled? Discuss.

### Week 7–8
- **CTE vs subquery:** CTEs are not faster than equivalent subqueries in SQLite — they're primarily a readability tool. The benefit is modularity and reuse.
- **LAG() requires partitioning knowledge:** If students try to partition by something unexpected, they get surprising results. Walk through the ORDER BY inside OVER() carefully.
- **November 2017 = Black Friday:** 7,544 orders. If a student's month-over-month growth analysis shows a massive spike here, they should be able to explain it.

---

## Assessment

### Weekly Assignments (formative)
- One assignment per week (5 questions, verified expected outputs)
- Self-checked against the verified values in this curriculum
- Groups review each other's queries and flag discrepancies

### Week 8 Group Presentation (summative)
- 10-minute SQL-driven business analysis
- All KPIs must match verified expected values
- Groups present 5 analyses (4 guided + 1 self-chosen)

| Criteria | Marks |
|---|---|
| SQL correctness (verified outputs) | 15 |
| Business insight quality | 15 |
| Query readability and structure | 10 |
| **Total** | **40** |

---

## Transition to Phase 2c Capstone

After completing Phase 2b, students will have:
- 3 months Python (Olist dataset: pandas, groupby, merging, visualisation)
- 2 months SQL (Olist dataset: SELECT through CTEs, window functions, multi-table joins)

The Phase 2c Capstone (1 month) will bring both skills together into a Streamlit dashboard. Students will:
- Query the Olist database using SQL
- Process and transform data using pandas
- Visualise using matplotlib/seaborn or plotly
- Deploy a functional dashboard answering the same business questions explored in both Python and SQL phases

The same 4 project groups from Phase 1 continue into Phase 2c.
