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
