# Group 4 — Revenue & Growth

**Focus:** GMV trends, state-level revenue, payment behaviour
**Carries forward from:** Phase 1 Excel — UCI Online Retail — 541,909 transactions, full teaching dataset

> **12 starter queries below, every one pre-validated against this dataset.** The result
> shown is what you will get. Use them as your floor — if you write your own, it must
> still return these numbers unless you can justify the difference.

---

## Your Five Required Charts

1. Monthly GMV trend — line, annotate the Nov 2017 peak
2. Revenue by state — horizontal bar, top 10 states
3. Payment method breakdown — pie
4. Year-over-year GMV comparison — grouped bar, with the partial-year caveat visible
5. **Credit-card instalment analysis** (Q6) — the advanced feature, required

Charts 1–4 are the common core. **Chart 5 is your advanced feature and it is required** —
its SQL is already written and verified below as Q6, so it is one hour of work, not a
redesign. The query number in brackets is the one to use.

**Four is a floor, not a target.** Add a 6th and 7th chart if you have insight worth
showing and can make them filter-driven and SQL-correct. Extra charts that are wrong cost
you marks.

**Sub-group ownership:** Q2, Q3, Q4, Q5 feed the four required charts. Q6 is your advanced feature. Q7 must be read before you chart Q6.

---

## The Shape of Your App

One file, one URL, three tabs:

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "Revenue & Growth", "Detail & Method"])

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

| Total Gmv | Peak Month | Peak Month Gmv | Avg Payment Value | Credit Card Pct |
|---|---|---|---|---|
| 15,843,553.24 | 2017-11 | 1,179,143.77 | 154.10 | 73.90 |

Your dashboard will also show **filtered** values as users change the sidebar, with the
active filter visible on screen. A `Total Orders` metric reading 45,101 when the year
filter is on 2017 is correct behaviour, not a bug — but a team that can toggle back to
`All` and reproduce the table above is demonstrating they understand their own dashboard.

---


## Your Headline Story

November 2017 is the peak at **R$1,179,143.77** — almost certainly Black Friday, and
naming that is worth marks. Total GMV is **R$15,843,553.24** across all orders.

Three supporting facts:

- Credit card is **73.9%** of transactions at R$154.10 average payment value.
- SP alone is **37.38%** of all GMV (R$5,921,678.12) — the top 3 states clear 70%.
- Your Q7 is a trap worth reading twice: `payment_installments` is **text**, its real
  maximum is **24** (not 12), and **2 rows have 0 instalments**. A chart capped at 12 or
  sorted as text is wrong in a way nobody notices unless you check.

2016 (329 orders) and 2018 (ends 17 Oct) are both partial. Your year-over-year chart needs
a visible caveat or it misleads. And your Q2 and Q5 will disagree on order counts — Q2
counts line items, the `orders` table gives 329 for 2016. Label which grain you are using.

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
WITH m AS (
    SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
           SUM(i.price + i.freight_value) AS gmv
    FROM order_items i JOIN orders o ON i.order_id = o.order_id
    WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
    GROUP BY month
)
SELECT ROUND(SUM(gmv),2)                              AS total_gmv,
       (SELECT month FROM m ORDER BY gmv DESC LIMIT 1) AS peak_month,
       (SELECT ROUND(gmv,2) FROM m ORDER BY gmv DESC LIMIT 1) AS peak_month_gmv,
       (SELECT ROUND(AVG(payment_value),2) FROM payments) AS avg_payment_value,
       (SELECT ROUND(100.0*SUM(CASE WHEN payment_type='credit_card' THEN 1 ELSE 0 END)
                           /COUNT(*),1) FROM payments) AS credit_card_pct
FROM m
```

**Verified result** (1 row):

| Total Gmv | Peak Month | Peak Month Gmv | Avg Payment Value | Credit Card Pct |
|---|---|---|---|---|
| 15,843,553.24 | 2017-11 | 1,179,143.77 | 154.10 | 73.90 |

#### Q2. Monthly GMV trend

*Chart 1* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       ROUND(SUM(i.price + i.freight_value),2) AS gmv,
       COUNT(DISTINCT i.order_id) AS orders
FROM orders o JOIN order_items i ON o.order_id = i.order_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY month ORDER BY month
```

**Verified result** (24 rows):

| Month | Gmv | Orders |
|---|---|---|
| 2016-09 | 354.75 | 3 |
| 2016-10 | 56,808.84 | 308 |
| 2016-12 | 19.62 | 1 |
| 2017-01 | 137,188.49 | 789 |
| 2017-02 | 286,280.62 | 1,733 |
| 2017-03 | 432,048.59 | 2,641 |
| 2017-04 | 412,422.24 | 2,391 |
| 2017-05 | 586,190.95 | 3,660 |
| _… | _… | _…_ |

#### Q3. Revenue by state (top 10)

*Chart 2* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT c.customer_state AS state,
       ROUND(SUM(i.price + i.freight_value),2) AS gmv,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN orders o    ON i.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY state ORDER BY gmv DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Gmv | Orders |
|---|---|---|
| SP | 5,921,678.12 | 41,375 |
| RJ | 2,129,681.98 | 12,762 |
| MG | 1,856,161.49 | 11,544 |
| RS | 885,826.76 | 5,432 |
| PR | 800,935.44 | 4,998 |
| BA | 611,506.67 | 3,358 |
| SC | 610,213.60 | 3,612 |
| DF | 353,229.44 | 2,125 |
| _… | _… | _…_ |

#### Q4. Payment method breakdown

*Chart 3* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT p.payment_type,
       COUNT(*) AS transactions,
       ROUND(SUM(p.payment_value),2) AS total_value,
       ROUND(AVG(p.payment_value),2) AS avg_value,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM payments),1) AS pct_of_all_transactions
FROM payments p
WHERE (? = '[]' OR p.payment_type IN (SELECT value FROM json_each(?)))
GROUP BY p.payment_type ORDER BY transactions DESC
```

**Verified result** (5 rows):

| Payment Type | Transactions | Total Value | Avg Value | Pct Of All Transactions |
|---|---|---|---|---|
| credit_card | 76,795 | 12,542,084.19 | 163.32 | 73.90 |
| boleto | 19,784 | 2,869,361.27 | 145.03 | 19.00 |
| voucher | 5,775 | 379,436.87 | 65.70 | 5.60 |
| debit_card | 1,529 | 217,989.79 | 142.57 | 1.50 |
| not_defined | 3 | 0.00 | 0.00 | 0.00 |

#### Q5. Year-over-year GMV comparison

*Chart 4* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       (SELECT COUNT(*) FROM orders o2
         WHERE strftime('%Y', o2.order_purchase_timestamp) = strftime('%Y', o.order_purchase_timestamp))
         AS orders_placed,
       COUNT(DISTINCT i.order_id) AS orders_with_items,
       COUNT(*) AS line_items,
       ROUND(SUM(i.price + i.freight_value),2) AS gmv
FROM order_items i JOIN orders o ON i.order_id = o.order_id
GROUP BY year ORDER BY year
```

**Verified result** (3 rows):

| Year | Orders Placed | Orders With Items | Line Items | Gmv |
|---|---|---|---|---|
| 2,016 | 329 | 312 | 370 | 57,183.21 |
| 2,017 | 45,101 | 44,579 | 50,864 | 7,142,672.43 |
| 2,018 | 54,011 | 53,775 | 61,416 | 8,643,697.60 |

#### Q6. Credit-card instalment analysis

*Advanced feature* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT CAST(p.payment_installments AS INTEGER) AS instalments,
       COUNT(*) AS transactions,
       ROUND(AVG(p.payment_value),2) AS avg_value
FROM payments p WHERE p.payment_type='credit_card'
  AND (? = '[]' OR p.payment_type IN (SELECT value FROM json_each(?)))
GROUP BY instalments ORDER BY CAST(p.payment_installments AS INTEGER)
```

**Verified result** (24 rows):

| Instalments | Transactions | Avg Value |
|---|---|---|
| 0 | 2 | 94.31 |
| 1 | 25,455 | 95.87 |
| 2 | 12,413 | 127.23 |
| 3 | 10,461 | 142.54 |
| 4 | 7,098 | 163.98 |
| 5 | 5,239 | 183.47 |
| 6 | 3,920 | 209.85 |
| 7 | 1,626 | 187.67 |
| _… | _… | _…_ |

#### Q7. Instalment data-quality check

*Data quality* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT (SELECT COUNT(*) FROM payments WHERE payment_installments='0') AS zero_instalment_rows,
       (SELECT MIN(CAST(payment_installments AS INTEGER)) FROM payments
         WHERE payment_type='credit_card') AS min_instalments,
       (SELECT MAX(CAST(payment_installments AS INTEGER)) FROM payments
         WHERE payment_type='credit_card') AS max_instalments,
       (SELECT COUNT(*) FROM payments) AS payment_rows,
       (SELECT COUNT(DISTINCT order_id) FROM payments) AS distinct_orders
```

**Verified result** (1 row):

| Zero Instalment Rows | Min Instalments | Max Instalments | Payment Rows | Distinct Orders |
|---|---|---|---|---|
| 2 | 0 | 24 | 103,886 | 99,440 |

#### Q8. Average payment value by instalment band

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT CASE WHEN CAST(p.payment_installments AS INTEGER) = 1  THEN '1 (paid in full)'
            WHEN CAST(p.payment_installments AS INTEGER) <= 3  THEN '2-3'
            WHEN CAST(p.payment_installments AS INTEGER) <= 6  THEN '4-6'
            WHEN CAST(p.payment_installments AS INTEGER) <= 12 THEN '7-12'
            ELSE '13+' END AS band,
       COUNT(*) AS transactions,
       ROUND(AVG(p.payment_value),2) AS avg_value,
       ROUND(SUM(p.payment_value),2) AS total_value
FROM payments p WHERE p.payment_type='credit_card'
  AND (? = '[]' OR p.payment_type IN (SELECT value FROM json_each(?)))
GROUP BY band ORDER BY band
```

**Verified result** (5 rows):

| Band | Transactions | Avg Value | Total Value |
|---|---|---|---|
| 1 (paid in full) | 25,455 | 95.87 | 2,440,445.43 |
| 13+ | 185 | 413.72 | 76,538.91 |
| 2-3 | 22,876 | 134.23 | 3,070,575.46 |
| 4-6 | 16,257 | 181.32 | 2,947,693.72 |
| 7-12 | 12,022 | 333.29 | 4,006,830.67 |

#### Q9. Cumulative GMV share by month

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
WITH m AS (
    SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
           SUM(i.price + i.freight_value) AS gmv
    FROM order_items i JOIN orders o ON i.order_id = o.order_id
    WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
    GROUP BY month
)
SELECT month, ROUND(gmv,2) AS gmv,
       ROUND(100.0*SUM(gmv) OVER (ORDER BY month)/SUM(gmv) OVER (),2) AS cumulative_pct
FROM m ORDER BY month
```

**Verified result** (24 rows):

| Month | Gmv | Cumulative Pct |
|---|---|---|
| 2016-09 | 354.75 | 0.00 |
| 2016-10 | 56,808.84 | 0.36 |
| 2016-12 | 19.62 | 0.36 |
| 2017-01 | 137,188.49 | 1.23 |
| 2017-02 | 286,280.62 | 3.03 |
| 2017-03 | 432,048.59 | 5.76 |
| 2017-04 | 412,422.24 | 8.36 |
| 2017-05 | 586,190.95 | 12.06 |
| _… | _… | _…_ |

#### Q10. Payment type by year

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       p.payment_type,
       COUNT(*) AS transactions,
       ROUND(SUM(p.payment_value),2) AS total_value
FROM payments p JOIN orders o ON p.order_id = o.order_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY year, p.payment_type ORDER BY year, total_value DESC
```

**Verified result** (13 rows):

| Year | Payment Type | Transactions | Total Value |
|---|---|---|---|
| 2,016 | credit_card | 258 | 48,562.48 |
| 2,016 | boleto | 63 | 9,679.06 |
| 2,016 | voucher | 23 | 879.07 |
| 2,016 | debit_card | 2 | 241.73 |
| 2,017 | credit_card | 34,568 | 5,637,373.94 |
| 2,017 | boleto | 9,508 | 1,396,063.37 |
| 2,017 | voucher | 3,027 | 172,982.95 |
| 2,017 | debit_card | 422 | 43,326.47 |
| _… | _… | _… | _…_ |

#### Q11. Revenue concentration: top 3 states

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
WITH s AS (
    SELECT c.customer_state AS state,
           SUM(i.price + i.freight_value) AS gmv
    FROM order_items i
    JOIN orders o    ON i.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
    GROUP BY state
)
SELECT state, ROUND(gmv,2) AS gmv,
       ROUND(100.0*gmv/SUM(gmv) OVER (),2) AS pct_of_total,
       ROUND(100.0*SUM(gmv) OVER (ORDER BY gmv DESC)/SUM(gmv) OVER (),2) AS cumulative_pct
FROM s ORDER BY gmv DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Gmv | Pct Of Total | Cumulative Pct |
|---|---|---|---|
| SP | 5,921,678.12 | 37.38 | 37.38 |
| RJ | 2,129,681.98 | 13.44 | 50.82 |
| MG | 1,856,161.49 | 11.72 | 62.53 |
| RS | 885,826.76 | 5.59 | 68.12 |
| PR | 800,935.44 | 5.06 | 73.18 |
| BA | 611,506.67 | 3.86 | 77.04 |
| SC | 610,213.60 | 3.85 | 80.89 |
| DF | 353,229.44 | 2.23 | 83.12 |
| _… | _… | _… | _…_ |

#### Q12. Monthly order counts (partial-year context)

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       MIN(o.order_purchase_timestamp) AS first_order,
       MAX(o.order_purchase_timestamp) AS last_order,
       COUNT(*) AS orders
FROM orders o WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY year ORDER BY year
```

**Verified result** (3 rows):

| Year | First Order | Last Order | Orders |
|---|---|---|---|
| 2,016 | 2016-09-04 21:15:19 | 2016-12-23 23:16:47 | 329 |
| 2,017 | 2017-01-05 11:56:06 | 2017-12-31 23:29:31 | 45,101 |
| 2,018 | 2018-01-01 02:48:41 | 2018-10-17 17:30:18 | 54,011 |

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
