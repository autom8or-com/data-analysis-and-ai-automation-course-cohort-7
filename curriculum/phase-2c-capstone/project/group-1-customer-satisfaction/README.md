# Group 1 — Customer Satisfaction

**Focus:** Order reviews, delivery performance, satisfaction drivers
**Carries forward from:** Phase 1 Excel — Amazon Reviews — 50,000 reviews, 20,290 products, 2002–2012

> **12 starter queries below, every one pre-validated against this dataset.** The result
> shown is what you will get. Use them as your floor — if you write your own, it must
> still return these numbers unless you can justify the difference.

---

## Your Five Required Charts

1. Review score distribution — bar, 1 to 5 stars with counts and %
2. Monthly average review score — line, look for the Nov 2017 dip
3. Average review score by state — horizontal bar, top 10 by order volume
4. On-time vs late delivery by state — grouped bar, top 5 states
5. **Delivery punctuality vs satisfaction** (Q6) — the advanced feature, required

Charts 1–4 are the common core. **Chart 5 is your advanced feature and it is required** —
its SQL is already written and verified below as Q6, so it is one hour of work, not a
redesign. The query number in brackets is the one to use.

**Four is a floor, not a target.** Add a 6th and 7th chart if you have insight worth
showing and can make them filter-driven and SQL-correct. Extra charts that are wrong cost
you marks.

**Sub-group ownership:** Q1–Q4 feed the four required charts. Q6 is your advanced feature. Q9, Q10, Q12 are bonus analysis — use them if you have insight to add.

---

## The Shape of Your App

One file, one URL, three tabs:

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "Customer Satisfaction", "Detail & Method"])

with tab_overview:
    ...   # 4 KPI metrics + chart 1 (your headline)
with tab_theme:
    ...   # charts 2, 3, 4
with tab_detail:
    ...   # chart 5 — the advanced feature — plus a written data-limitation note
```

Write **every chart as a function** from the first one, and put the `?` filter guards in
every query from day one. Passing `params=("All", "All", ...)` until the sidebar exists
means the Week 3 filter work is a two-line change, not a rewrite of every query. That is
the single biggest determinant of whether your dashboard ends up with working filters.

---

## Your Headline KPIs

Everything in the dashboard should reconcile to these **when filters are set to `All`**.
If a number disagrees at `All`, the chart is wrong.

| Total Orders | Delivered Orders | Avg Review Score | Late Deliveries | Avg Delivery Days |
|---|---|---|---|---|
| 99,441 | 96,478 | 4.09 | 7,826 | 12.56 |

Your dashboard will also show **filtered** values as users change the sidebar, with the
active filter visible on screen. A `Total Orders` metric reading 45,101 when the year
filter is on 2017 is correct behaviour, not a bug — but a team that can toggle back to
`All` and reproduce the table above is demonstrating they understand their own dashboard.

---


## Your Headline Story

Late deliveries cost you **1.73 stars**. On-time orders average 4.294; late ones average
2.566. That is the single strongest satisfaction driver in this dataset, and it is the
insight your presentation should be built around.

Three supporting facts to have ready:

- **7,826** delivered orders (8.1%) arrived after their estimated delivery date.
- When late, orders average **9.55 days** past the estimate.
- Reviews are a fan-out table — 99,224 rows for 98,673 orders. Use
  `COUNT(DISTINCT order_id)` or your order counts will be wrong.

Your Q9 (delivery-time buckets) will show the score decline more smoothly than the binary
on-time/late split. Use both: the split for the headline, the buckets for the nuance.

---

## Data Rules That Bite Your Team

Read these before writing queries. Full list in the [project README](../README.md).

- `reviews` and `payments` are **fan-out tables** — use `COUNT(DISTINCT order_id)` across
  any join, never `COUNT(*)`.
- Count customers by **`customer_unique_id`** (96,096), not `customer_id` (99,441).
- GMV is **all orders**, `SUM(price + freight_value)` = 15,843,553.24. Adding a delivered
  filter gives 15,419,773.75 — correct for a different question, wrong for this one.
- **2016 and 2018 are partial years.** 2016 has only 3 active months (Sep, Oct, Dec) and
  **November 2016 has zero orders** — a gap in a monthly chart is real, not a bug. Do not
  interpolate across it.
- **Never label an `order_items` row count "orders."** The `orders` table, orders-with-items,
  and `order_items` rows are three different numbers (329 / 312 / 370 for 2016).
- **Use the shared filter contract** below. Do not build SQL from f-strings; the state
  filter is exactly the case where that breaks.

### The filter contract

Your starter queries are the **unfiltered reference** — that is what makes the result
tables trustworthy. When you wire a chart up, add these guards. Everyone uses this:

```python
import json

selected_year  = st.sidebar.selectbox("Year", ["All", "2016", "2017", "2018"])
selected_state = st.sidebar.multiselect("State", STATES, default=["All"])
state_json = json.dumps([] if "All" in selected_state else list(selected_state))

def year_params(year):                 # year guard only  -> 2 placeholders
    return (year, year)

def multi_params(multi_json):          # multiselect guard only -> 2 placeholders
    return (multi_json, multi_json)

def year_multi(year, multi_json):      # both guards -> 4 placeholders
    return (year, year, multi_json, multi_json)
```

```sql
-- Year guard - 2 placeholders
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
-- Multi-select guard - 2 placeholders (the same JSON string twice)
  AND (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
```

**Three helpers, and match the one your query needs.** A query can carry a year guard, a
multiselect guard, or both — so `year_params` (2 placeholders), `multi_params` (2), or
`year_multi` (4). Passing the wrong tuple raises `Incorrect number of bindings`; that error
*means* the helper and the guards disagree, and it is the most common filter bug there is.
**Your 12 queries below are already filterable** — each is labelled with its helper, or
marked *not filterable* where the question is a whole-dataset fact. With filters set to
`All`, your charts reproduce the tables in this README exactly. That is the contract.

---

## Your 12 Starter Queries

#### Q1. Headline KPIs

*KPI row* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT COUNT(DISTINCT o.order_id) AS total_orders,
       COUNT(DISTINCT CASE WHEN o.order_status='delivered' THEN o.order_id END) AS delivered_orders,
       (SELECT ROUND(AVG(CAST(review_score AS REAL)),2) FROM reviews) AS avg_review_score,
       SUM(CASE WHEN o.order_status='delivered'
                 AND o.order_delivered_customer_date > o.order_estimated_delivery_date
                THEN 1 ELSE 0 END) AS late_deliveries,
       ROUND(AVG(CASE WHEN o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
                 THEN julianday(o.order_delivered_customer_date)
                    - julianday(o.order_purchase_timestamp) END),2) AS avg_delivery_days
FROM orders o
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
```

**Verified result** (1 row):

| Total Orders | Delivered Orders | Avg Review Score | Late Deliveries | Avg Delivery Days |
|---|---|---|---|---|
| 99,441 | 96,478 | 4.09 | 7,826 | 12.56 |

#### Q2. Review score distribution

*Chart 1* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT CAST(review_score AS INTEGER) AS score,
       COUNT(*)                     AS reviews,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM reviews),1) AS pct
FROM reviews GROUP BY 1 ORDER BY 1
```

**Verified result** (5 rows):

| Score | Reviews | Pct |
|---|---|---|
| 1 | 11,424 | 11.50 |
| 2 | 3,151 | 3.20 |
| 3 | 8,179 | 8.20 |
| 4 | 19,142 | 19.30 |
| 5 | 57,328 | 57.80 |

#### Q3. Monthly average review score

*Chart 2* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       COUNT(*) AS reviews,
       ROUND(AVG(CAST(r.review_score AS REAL)),3) AS avg_score
FROM orders o JOIN reviews r ON o.order_id = r.order_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY month ORDER BY month
```

**Verified result** (25 rows):

| Month | Reviews | Avg Score |
|---|---|---|
| 2016-09 | 4 | 1.00 |
| 2016-10 | 321 | 3.57 |
| 2016-12 | 1 | 5.00 |
| 2017-01 | 797 | 4.07 |
| 2017-02 | 1,776 | 4.02 |
| 2017-03 | 2,676 | 4.07 |
| 2017-04 | 2,394 | 4.04 |
| 2017-05 | 3,703 | 4.14 |
| _… | _… | _…_ |

#### Q4. Average review score by state (top 10 by orders)

*Chart 3* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT c.customer_state AS state,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(AVG(CAST(r.review_score AS REAL)),3) AS avg_score
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN reviews r  ON o.order_id  = r.order_id
WHERE (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
GROUP BY state ORDER BY orders DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Orders | Avg Score |
|---|---|---|
| SP | 41,472 | 4.17 |
| RJ | 12,687 | 3.88 |
| MG | 11,554 | 4.14 |
| RS | 5,443 | 4.13 |
| PR | 5,019 | 4.18 |
| SC | 3,609 | 4.07 |
| BA | 3,340 | 3.86 |
| DF | 2,128 | 4.07 |
| _… | _… | _…_ |

#### Q5. On-time vs late delivery by state (top 5)

*Chart 4* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT c.customer_state AS state,
       COUNT(DISTINCT o.order_id) AS delivered,
       SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                THEN 1 ELSE 0 END) AS late,
       ROUND(100.0*SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
                             THEN 1 ELSE 0 END)/COUNT(*),1) AS late_pct
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
  AND (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
GROUP BY state ORDER BY delivered DESC LIMIT 5
```

**Verified result** (5 rows):

| State | Delivered | Late | Late Pct |
|---|---|---|---|
| SP | 40,501 | 2,387 | 5.90 |
| RJ | 12,350 | 1,664 | 13.50 |
| MG | 11,354 | 637 | 5.60 |
| RS | 5,345 | 382 | 7.10 |
| PR | 4,923 | 246 | 5.00 |

#### Q6. Delivery punctuality vs satisfaction

*Advanced feature* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
            THEN 'On Time' ELSE 'Late' END AS delivery_status,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(AVG(CAST(r.review_score AS REAL)),3) AS avg_score,
       ROUND(AVG(julianday(o.order_delivered_customer_date)
               - julianday(o.order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN reviews r  ON o.order_id  = r.order_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
  AND (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
GROUP BY 1 ORDER BY avg_score DESC
```

**Verified result** (2 rows):

| Delivery Status | Orders | Avg Score | Avg Delivery Days |
|---|---|---|---|
| On Time | 88,171 | 4.29 | 10.88 |
| Late | 7,661 | 2.57 | 31.39 |

#### Q7. Average days late when late

*Diagnostic* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT COUNT(*) AS late_orders,
       ROUND(AVG(julianday(order_delivered_customer_date)
               - julianday(order_estimated_delivery_date)),2) AS avg_days_late,
       ROUND(MAX(julianday(order_delivered_customer_date)
               - julianday(order_estimated_delivery_date)),0) AS worst_days_late
FROM orders
WHERE order_status='delivered'
  AND order_delivered_customer_date > order_estimated_delivery_date
```

**Verified result** (1 row):

| Late Orders | Avg Days Late | Worst Days Late |
|---|---|---|
| 7,826 | 9.55 | 189.00 |

#### Q8. Review volume by month

*Chart support* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       COUNT(*) AS reviews
FROM orders o JOIN reviews r ON o.order_id = r.order_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY year ORDER BY year
```

**Verified result** (3 rows):

| Year | Reviews |
|---|---|
| 2,016 | 326 |
| 2,017 | 45,044 |
| 2,018 | 53,854 |

#### Q9. Satisfaction by delivery-time bucket

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT CASE
         WHEN julianday(o.order_delivered_customer_date)-julianday(o.order_purchase_timestamp) <= 5  THEN '0-5 days'
         WHEN julianday(o.order_delivered_customer_date)-julianday(o.order_purchase_timestamp) <= 10 THEN '6-10 days'
         WHEN julianday(o.order_delivered_customer_date)-julianday(o.order_purchase_timestamp) <= 20 THEN '11-20 days'
         WHEN julianday(o.order_delivered_customer_date)-julianday(o.order_purchase_timestamp) <= 30 THEN '21-30 days'
         ELSE '30+ days' END AS delivery_bucket,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(AVG(CAST(r.review_score AS REAL)),3) AS avg_score
FROM orders o JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
  AND (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY 1 ORDER BY 1
```

**Verified result** (5 rows):

| Delivery Bucket | Orders | Avg Score |
|---|---|---|
| 0-5 days | 13,374 | 4.45 |
| 11-20 days | 35,547 | 4.22 |
| 21-30 days | 9,588 | 3.69 |
| 30+ days | 4,438 | 2.26 |
| 6-10 days | 32,885 | 4.36 |

#### Q10. Reviews fan-out diagnostic

*Data quality* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT COUNT(*) AS review_rows, COUNT(DISTINCT order_id) AS distinct_orders,
       COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_rows
FROM reviews
```

**Verified result** (1 row):

| Review Rows | Distinct Orders | Duplicate Rows |
|---|---|---|
| 99,224 | 98,673 | 551 |

#### Q11. Distinct customers vs customer rows

*Data quality* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT (SELECT COUNT(*) FROM customers) AS customer_rows,
       (SELECT COUNT(DISTINCT customer_unique_id) FROM customers) AS unique_customers
```

**Verified result** (1 row):

| Customer Rows | Unique Customers |
|---|---|
| 99,441 | 96,096 |

#### Q12. Lowest-scoring states (min 2,000 orders)

*Insight* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT c.customer_state AS state,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(AVG(CAST(r.review_score AS REAL)),3) AS avg_score
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN reviews r  ON o.order_id  = r.order_id
WHERE (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
GROUP BY state HAVING orders >= 2000
ORDER BY avg_score ASC LIMIT 10
```

**Verified result** (10 rows):

| State | Orders | Avg Score |
|---|---|---|
| BA | 3,340 | 3.86 |
| RJ | 12,687 | 3.88 |
| ES | 2,006 | 4.04 |
| GO | 2,007 | 4.04 |
| DF | 2,128 | 4.07 |
| SC | 3,609 | 4.07 |
| RS | 5,443 | 4.13 |
| MG | 11,554 | 4.14 |
| _… | _… | _…_ |

---

## Before You Present

- [ ] Every KPI on the dashboard reconciles to the table above with filters set to `All`
- [ ] 5 charts — the 4 required **and** your advanced feature — all filter-driven
- [ ] App deployed, public URL loads with data, three tabs present
- [ ] Filters update every chart, not just some
- [ ] Every chart is a function; every query is parameterised
- [ ] `@st.cache_resource` on the connection (not `@st.cache_data` — it cannot hold a
      `sqlite3.Connection`)
- [ ] Report states which GMV definition you used, and why
- [ ] Presentation names one real limitation, not a generic apology
