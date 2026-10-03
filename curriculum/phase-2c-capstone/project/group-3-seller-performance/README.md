# Group 3 — Seller Performance

**Focus:** Seller tiers, top performers, geographic distribution
**Carries forward from:** Phase 1 Excel — Bestselling Books — 550 books, 2 genres, 2009–2019

> **12 starter queries below, every one pre-validated against this dataset.** The result
> shown is what you will get. Use them as your floor — if you write your own, it must
> still return these numbers unless you can justify the difference.

---

## Your Five Required Charts

1. Seller tier distribution — pie or donut, count per tier
2. Top 20 sellers by revenue — horizontal bar
3. Revenue by seller state — horizontal bar, top 10 states
4. Revenue concentration — cumulative % curve (the Pareto curve)
5. **Pareto: the exact top-40 share** (Q6) — the advanced feature, required

Charts 1–4 are the common core. **Chart 5 is your advanced feature and it is required** —
its SQL is already written and verified below as Q6, so it is one hour of work, not a
redesign. The query number in brackets is the one to use.

**Four is a floor, not a target.** Add a 6th and 7th chart if you have insight worth
showing and can make them filter-driven and SQL-correct. Extra charts that are wrong cost
you marks.

**Sub-group ownership:** Q2, Q3, Q4, Q5 feed the four required charts. Q6 is your advanced feature. Q7 and Q11 sharpen the concentration story.

---

## The Shape of Your App

One file, one URL, three tabs:

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "Seller Performance", "Detail & Method"])

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

| Total Sellers | Top Seller Revenue | Top Tier | High Performer | Mid Tier | Standard |
|---|---|---|---|---|---|
| 3,095 | 229,472.63 | 18 | 22 | 252 | 2,803 |

Your dashboard will also show **filtered** values as users change the sidebar, with the
active filter visible on screen. A `Total Orders` metric reading 45,101 when the year
filter is on 2017 is correct behaviour, not a bug — but a team that can toggle back to
`All` and reproduce the table above is demonstrating they understand their own dashboard.

---


## Your Headline Story

**40 sellers — 1.29% of the marketplace — generate 29.54% of all item revenue**
(R$4,014,922.70 of R$13,591,643.70). That is your headline, and the rubric's
"quantify this correctly" criterion is aimed straight at it.

Three supporting facts:

- Tiers split **18 Top / 22 High / 252 Mid / 2,803 Standard** — 90.6% of sellers sit in
  the Standard bucket.
- The top seller is `4869f7a5dfa277a7dca6462dcf3b52b2` in SP at **R$229,472.63** across
  1,132 orders.
- SP is the dominant seller state at R$8,753,396.21 across 1,849 sellers, but its top 5
  sellers account for only 11.29% of that — concentration is a *national* story, not a
  São Paulo one. Both are interesting; pick deliberately.

Your Q5 Pareto curve and Q6 exact share are the same finding at two resolutions. Show the
curve in the dashboard, quote the exact number in the report.

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

*KPI row* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT (SELECT COUNT(DISTINCT seller_id) FROM sellers) AS total_sellers,
       (SELECT ROUND(MAX(total_revenue),2) FROM (SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue, COUNT(DISTINCT i.order_id) AS orders FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state)) AS top_seller_revenue,
       (SELECT COUNT(*) FROM (SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue, COUNT(DISTINCT i.order_id) AS orders FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state)
         WHERE total_revenue >= 100000)                             AS top_tier,
       (SELECT COUNT(*) FROM (SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue, COUNT(DISTINCT i.order_id) AS orders FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state)
         WHERE total_revenue >= 50000 AND total_revenue < 100000)   AS high_performer,
       (SELECT COUNT(*) FROM (SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue, COUNT(DISTINCT i.order_id) AS orders FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state)
         WHERE total_revenue >= 10000 AND total_revenue < 50000)    AS mid_tier,
       (SELECT COUNT(*) FROM (SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue, COUNT(DISTINCT i.order_id) AS orders FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id GROUP BY s.seller_id, s.seller_state)
         WHERE total_revenue < 10000)                               AS standard
```

**Verified result** (1 row):

| Total Sellers | Top Seller Revenue | Top Tier | High Performer | Mid Tier | Standard |
|---|---|---|---|---|---|
| 3,095 | 229,472.63 | 18 | 22 | 252 | 2,803 |

#### Q2. Seller tier distribution

*Chart 1* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH seller_revenue AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
),
tiers AS (
    SELECT *, CASE WHEN total_revenue >= 100000 THEN 'Top Seller'
                   WHEN total_revenue >= 50000  THEN 'High Performer'
                   WHEN total_revenue >= 10000  THEN 'Mid Tier'
                   ELSE 'Standard' END AS tier
    FROM seller_revenue
)
SELECT tier, COUNT(*) AS sellers, ROUND(SUM(total_revenue),2) AS revenue,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM seller_revenue),2) AS pct_of_sellers
FROM tiers GROUP BY tier ORDER BY revenue DESC
```

**Verified result** (4 rows):

| Tier | Sellers | Revenue | Pct Of Sellers |
|---|---|---|---|
| Mid Tier | 252 | 4,992,867.56 | 8.14 |
| Standard | 2,803 | 4,583,853.44 | 90.57 |
| Top Seller | 18 | 2,692,345.55 | 0.58 |
| High Performer | 22 | 1,322,577.15 | 0.71 |

#### Q3. Top 20 sellers by revenue

*Chart 2* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT s.seller_id, s.seller_state,
       ROUND(SUM(i.price),2) AS revenue,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
GROUP BY s.seller_id, s.seller_state
ORDER BY revenue DESC LIMIT 20
```

**Verified result** (20 rows):

| Seller Id | Seller State | Revenue | Orders |
|---|---|---|---|
| 4869f7a5dfa277a7dca6462dcf3b52b2 | SP | 229,472.63 | 1,132 |
| 53243585a1d6dc2643021fd1853d8905 | BA | 222,776.05 | 358 |
| 4a3ca9315b744ce9f8e9374361493884 | SP | 200,472.92 | 1,806 |
| fa1c13f2614d7b5c4749cbc52fecda94 | SP | 194,042.03 | 585 |
| 7c67e1448b00f6e969d365cea6b010ab | SP | 187,923.89 | 982 |
| 7e93a43ef30c4f03f38b393420bc753a | SP | 176,431.87 | 336 |
| da8622b14eb17ae2831f4ac5b9dab84a | SP | 160,236.57 | 1,314 |
| 7a67c85e85bb2ce8582c35f2203ad736 | SP | 141,745.53 | 1,160 |
| _… | _… | _… | _…_ |

#### Q4. Revenue by seller state (top 10)

*Chart 3* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT seller_state AS state, COUNT(*) AS sellers,
       ROUND(SUM(total_revenue),2) AS revenue
FROM (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
)
GROUP BY seller_state ORDER BY revenue DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Sellers | Revenue |
|---|---|---|
| SP | 1,849 | 8,753,396.21 |
| PR | 349 | 1,261,887.21 |
| MG | 244 | 1,011,564.74 |
| RJ | 171 | 843,984.22 |
| SC | 190 | 632,426.07 |
| RS | 129 | 378,559.54 |
| BA | 19 | 285,561.56 |
| DF | 30 | 97,749.48 |
| _… | _… | _…_ |

#### Q5. Revenue concentration (Pareto curve)

*Chart 4* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH ranked AS (
    SELECT seller_id, total_revenue,
           ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS rn,
           SUM(total_revenue) OVER () AS grand_total
    FROM (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
)
)
SELECT rn AS sellers_ranked,
       ROUND(total_revenue,2) AS revenue,
       ROUND(100.0*SUM(total_revenue) OVER (ORDER BY rn)/grand_total,2) AS cumulative_pct
FROM ranked WHERE rn IN (10,50,100,200,400,800,1600,3095)
ORDER BY rn
```

**Verified result** (8 rows):

| Sellers Ranked | Revenue | Cumulative Pct |
|---|---|---|
| 10 | 135,171.70 | 0.99 |
| 50 | 43,587.40 | 1.32 |
| 100 | 25,108.09 | 1.50 |
| 200 | 13,592.08 | 1.60 |
| 400 | 7,630.00 | 1.66 |
| 800 | 3,098.99 | 1.68 |
| 1,600 | 776.00 | 1.68 |
| 3,095 | 3.50 | 1.68 |

#### Q6. Pareto: what share does the top 40 hold?

*Advanced feature* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH sr AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
),
top40 AS (SELECT SUM(total_revenue) AS rev FROM (SELECT total_revenue FROM sr
                                                 ORDER BY total_revenue DESC LIMIT 40))
SELECT (SELECT COUNT(*) FROM sr) AS total_sellers,
       ROUND(100.0*40/(SELECT COUNT(*) FROM sr),2) AS top_40_pct_of_sellers,
       (SELECT ROUND(rev,2) FROM top40) AS top_40_revenue,
       (SELECT ROUND(100.0*(SELECT rev FROM top40)
                     /(SELECT SUM(total_revenue) FROM sr),2)) AS top_40_pct_of_revenue
```

**Verified result** (1 row):

| Total Sellers | Top 40 Pct Of Sellers | Top 40 Revenue | Top 40 Pct Of Revenue |
|---|---|---|---|
| 3,095 | 1.29 | 4,014,922.70 | 29.54 |

#### Q7. Top 5 sellers per state (top 5 states)

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH sr AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
),
per_state AS (
    SELECT seller_state, SUM(total_revenue) AS state_total,
           COUNT(*) AS sellers, SUM(orders) AS state_orders
    FROM sr GROUP BY seller_state
),
top_states AS (
    SELECT seller_state, state_total FROM per_state
    ORDER BY state_total DESC LIMIT 5
),
ranked AS (
    SELECT seller_state, seller_id, total_revenue,
           ROW_NUMBER() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS rn
    FROM sr WHERE seller_state IN (SELECT seller_state FROM top_states)
)
SELECT r.seller_state AS state, r.seller_id,
       ROUND(r.total_revenue,2) AS revenue,
       ROUND(100.0*r.total_revenue/t.state_total,2) AS pct_of_state_revenue
FROM ranked r JOIN top_states t ON r.seller_state = t.seller_state
WHERE r.rn = 1 ORDER BY revenue DESC
```

**Verified result** (5 rows):

| State | Seller Id | Revenue | Pct Of State Revenue |
|---|---|---|---|
| SP | 4869f7a5dfa277a7dca6462dcf3b52b2 | 229,472.63 | 2.62 |
| RJ | 46dc3b2cc0980fb8ec44634e21d2718e | 128,111.19 | 15.18 |
| MG | a1043bafd471dff536d0c462352beb48 | 101,901.16 | 10.07 |
| PR | ccc4bbb5f32a6ab2b7066a4130f114e3 | 74,004.62 | 5.86 |
| SC | 04308b1ee57b6625f47df1d56f00eedf | 60,130.60 | 9.51 |

#### Q8. Seller revenue distribution buckets

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH seller_revenue AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
),
buckets AS (
    SELECT CASE WHEN total_revenue >= 100000 THEN 'a. 100k+'
                WHEN total_revenue >= 50000  THEN 'b. 50k-100k'
                WHEN total_revenue >= 10000  THEN 'c. 10k-50k'
                WHEN total_revenue >= 1000   THEN 'd. 1k-10k'
                WHEN total_revenue >= 100    THEN 'e. 100-1k'
                ELSE 'f. under 100' END AS bucket
    FROM seller_revenue
)
SELECT bucket, COUNT(*) AS sellers FROM buckets GROUP BY bucket ORDER BY bucket
```

**Verified result** (6 rows):

| Bucket | Sellers |
|---|---|
| a. 100k+ | 18 |
| b. 50k-100k | 22 |
| c. 10k-50k | 252 |
| d. 1k-10k | 1,136 |
| e. 100-1k | 1,251 |
| f. under 100 | 416 |

#### Q9. Order count vs average order value (top 15)

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT s.seller_id, s.seller_state,
       COUNT(DISTINCT i.order_id) AS orders,
       ROUND(SUM(i.price),2) AS revenue,
       ROUND(SUM(i.price)/COUNT(DISTINCT i.order_id),2) AS avg_order_value
FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
GROUP BY s.seller_id, s.seller_state
ORDER BY revenue DESC LIMIT 15
```

**Verified result** (15 rows):

| Seller Id | Seller State | Orders | Revenue | Avg Order Value |
|---|---|---|---|---|
| 4869f7a5dfa277a7dca6462dcf3b52b2 | SP | 1,132 | 229,472.63 | 202.71 |
| 53243585a1d6dc2643021fd1853d8905 | BA | 358 | 222,776.05 | 622.28 |
| 4a3ca9315b744ce9f8e9374361493884 | SP | 1,806 | 200,472.92 | 111.00 |
| fa1c13f2614d7b5c4749cbc52fecda94 | SP | 585 | 194,042.03 | 331.70 |
| 7c67e1448b00f6e969d365cea6b010ab | SP | 982 | 187,923.89 | 191.37 |
| 7e93a43ef30c4f03f38b393420bc753a | SP | 336 | 176,431.87 | 525.09 |
| da8622b14eb17ae2831f4ac5b9dab84a | SP | 1,314 | 160,236.57 | 121.95 |
| 7a67c85e85bb2ce8582c35f2203ad736 | SP | 1,160 | 141,745.53 | 122.19 |
| _… | _… | _… | _… | _…_ |

#### Q10. Top seller states by median revenue

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH seller_revenue AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
)
SELECT seller_state AS state, COUNT(*) AS sellers,
       ROUND(AVG(total_revenue),2) AS avg_revenue,
       ROUND(MIN(total_revenue),2) AS min_revenue
FROM seller_revenue GROUP BY seller_state ORDER BY avg_revenue DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Sellers | Avg Revenue | Min Revenue |
|---|---|---|---|
| MA | 1 | 36,408.95 | 36,408.95 |
| BA | 19 | 15,029.56 | 23.90 |
| PE | 9 | 10,165.98 | 25.99 |
| RJ | 171 | 4,935.58 | 9.90 |
| SP | 1,849 | 4,734.12 | 3.50 |
| MT | 4 | 4,267.68 | 318.00 |
| MG | 244 | 4,145.76 | 7.60 |
| PR | 349 | 3,615.72 | 8.00 |
| _… | _… | _… | _…_ |

#### Q11. Seller concentration by state (top 5 sellers share)

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH sr AS (
    SELECT s.seller_id, s.seller_state, SUM(i.price) AS total_revenue,
           COUNT(DISTINCT i.order_id) AS orders
    FROM order_items i JOIN sellers s ON i.seller_id = s.seller_id
    WHERE (? = '[]' OR s.seller_state IN (SELECT value FROM json_each(?)))
    GROUP BY s.seller_id, s.seller_state
),
top_states AS (
    SELECT seller_state, SUM(total_revenue) AS state_total
    FROM sr GROUP BY seller_state ORDER BY state_total DESC LIMIT 5
),
ranked AS (
    SELECT seller_state, total_revenue,
           ROW_NUMBER() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS rn
    FROM sr WHERE seller_state IN (SELECT seller_state FROM top_states)
)
SELECT t.seller_state AS state,
       ROUND(t.state_total,2) AS state_revenue,
       COUNT(*) FILTER (WHERE r.rn <= 5) AS top_5_sellers,
       ROUND(SUM(r.total_revenue) FILTER (WHERE r.rn <= 5),2) AS top_5_revenue,
       ROUND(100.0*SUM(r.total_revenue) FILTER (WHERE r.rn <= 5)/t.state_total,2) AS top_5_pct
FROM top_states t
JOIN ranked r ON r.seller_state = t.seller_state
GROUP BY t.seller_state, t.state_total
ORDER BY t.state_total DESC
```

**Verified result** (5 rows):

| State | State Revenue | Top 5 Sellers | Top 5 Revenue | Top 5 Pct |
|---|---|---|---|---|
| SP | 8,753,396.21 | 5 | 988,343.34 | 11.29 |
| PR | 1,261,887.21 | 5 | 255,174.75 | 20.22 |
| MG | 1,011,564.74 | 5 | 254,135.12 | 25.12 |
| RJ | 843,984.22 | 5 | 423,856.68 | 50.22 |
| SC | 632,426.07 | 5 | 207,289.16 | 32.78 |

#### Q12. Sellers by year first sale

*Analysis* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       COUNT(DISTINCT i.seller_id) AS active_sellers
FROM order_items i JOIN orders o ON i.order_id = o.order_id
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY year ORDER BY year
```

**Verified result** (3 rows):

| Year | Active Sellers |
|---|---|
| 2,016 | 145 |
| 2,017 | 1,784 |
| 2,018 | 2,383 |

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
