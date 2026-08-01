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

