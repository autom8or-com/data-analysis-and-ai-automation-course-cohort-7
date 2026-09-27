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
