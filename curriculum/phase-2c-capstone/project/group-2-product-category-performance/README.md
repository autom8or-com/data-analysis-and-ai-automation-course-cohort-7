# Group 2 — Product Category Performance

**Focus:** Category revenue rankings, product-level GMV analysis
**Carries forward from:** Phase 1 Excel — Superstore — 9,994 transactions, 3 categories, 4 regions

> **12 starter queries below, every one pre-validated against this dataset.** The result
> shown is what you will get. Use them as your floor — if you write your own, it must
> still return these numbers unless you can justify the difference.

---

## Your Five Required Charts

1. Top 10 categories by revenue — horizontal bar, English names via the translation join
2. Category revenue over time — stacked or grouped bar by quarter, top 5 categories
3. Price distribution by category — box plot or average-price bar, top 10
4. Order volume vs revenue per category — scatter, to spot over/underperformers
5. **Market share of the top 10** (Q6) — the advanced feature, required

Charts 1–4 are the common core. **Chart 5 is your advanced feature and it is required** —
its SQL is already written and verified below as Q6, so it is one hour of work, not a
redesign. The query number in brackets is the one to use.

**Four is a floor, not a target.** Add a 6th and 7th chart if you have insight worth
showing and can make them filter-driven and SQL-correct. Extra charts that are wrong cost
you marks.

**Sub-group ownership:** Q2, Q3, Q4, Q5 feed the four required charts. Q6 is your advanced feature (market share). Q7 is not optional reading — your denominator depends on it.

---

## The Shape of Your App

One file, one URL, three tabs:

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "Category Performance", "Detail & Method"])

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

| Total Gmv | Top Category Revenue | Translated Categories | Avg Item Price | Total Items |
|---|---|---|---|---|
| 15,843,553.24 | 1,258,681.34 | 71 | 120.65 | 112,650 |

Your dashboard will also show **filtered** values as users change the sidebar, with the
active filter visible on screen. A `Total Orders` metric reading 45,101 when the year
filter is on 2017 is correct behaviour, not a bug — but a team that can toggle back to
`All` and reproduce the table above is demonstrating they understand their own dashboard.

---


## Your Headline Story

**No category dominates.** `health_beauty` leads at **9.39%** of translated item revenue,
and the top 10 categories together reach only **63.22%**. The long tail is the story.

Three supporting facts:

- `health_beauty` is R$1,258,681.34 across 8,836 orders.
- Average item price across the whole dataset is **R$120.65** — most categories cluster
  near it, so price is a poor differentiator between them.
- Your Q7 exists because the category join is lossy: **623 products** and R$185,049.76 of
  revenue disappear the moment you join `categories`. Your denominator is a choice, and
  you must state which one you used (9.39% translated vs 9.26% of all item revenue).

If someone tells you to "filter out null categories", they are solving a problem that does
not exist — there are zero nulls. The real loss is at the join.

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
SELECT (SELECT ROUND(SUM(i.price + i.freight_value),2) FROM order_items i
          JOIN orders o ON i.order_id=o.order_id)                    AS total_gmv,
       (SELECT ROUND(SUM(i.price),2) FROM order_items i
          JOIN orders o ON i.order_id=o.order_id
          JOIN products p ON i.product_id=p.product_id
          JOIN categories t ON p.product_category_name=t.product_category_name
          WHERE t.product_category_name_english='health_beauty')    AS top_category_revenue,
       (SELECT COUNT(*) FROM categories)                            AS translated_categories,
       (SELECT ROUND(AVG(price),2) FROM order_items)               AS avg_item_price,
       (SELECT COUNT(*) FROM order_items)                          AS total_items
```

**Verified result** (1 row):

| Total Gmv | Top Category Revenue | Translated Categories | Avg Item Price | Total Items |
|---|---|---|---|---|
| 15,843,553.24 | 1,258,681.34 | 71 | 120.65 | 112,650 |

#### Q2. Top 10 categories by revenue

*Chart 1* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       ROUND(SUM(i.price),2) AS revenue,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY revenue DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Revenue | Orders |
|---|---|---|
| health_beauty | 1,258,681.34 | 8,836 |
| watches_gifts | 1,205,005.68 | 5,624 |
| bed_bath_table | 1,036,988.68 | 9,417 |
| sports_leisure | 988,048.97 | 7,720 |
| computers_accessories | 911,954.32 | 6,689 |
| furniture_decor | 729,762.49 | 6,449 |
| cool_stuff | 635,290.85 | 3,632 |
| housewares | 632,248.66 | 5,884 |
| _… | _… | _…_ |

#### Q3. Category revenue by quarter (top 5)

*Chart 2* · **filterable** — call with `year_params(...)`; the table below is the `All` result

```sql
SELECT strftime('%Y', o.order_purchase_timestamp) AS year,
       (strftime('%m', o.order_purchase_timestamp) - 1) / 3 + 1 AS quarter,
       SUM(CASE WHEN t.product_category_name_english IN
                   ('health_beauty','watches_gifts','bed_bath_table',
                    'sports_leisure','computers_accessories')
                THEN i.price ELSE 0 END) AS top5_revenue
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
GROUP BY year, quarter ORDER BY year, quarter
```

**Verified result** (9 rows):

| Year | Quarter | Top5 Revenue |
|---|---|---|
| 2,016 | 3 | 134.97 |
| 2,016 | 4 | 13,124.70 |
| 2,017 | 1 | 251,637.08 |
| 2,017 | 2 | 482,229.50 |
| 2,017 | 3 | 663,545.80 |
| 2,017 | 4 | 932,805.79 |
| 2,018 | 1 | 1,215,287.18 |
| 2,018 | 2 | 1,141,699.09 |
| _… | _… | _…_ |

#### Q4. Average item price by category (top 10)

*Chart 3* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       ROUND(AVG(i.price),2) AS avg_price,
       ROUND(MIN(i.price),2) AS min_price,
       ROUND(MAX(i.price),2) AS max_price
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY avg_price DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Avg Price | Min Price | Max Price |
|---|---|---|---|
| computers | 1,098.34 | 1,100.00 | 899.00 |
| small_appliances_home_oven_and_coffee | 624.29 | 10.19 | 98.00 |
| home_appliances_2 | 476.12 | 100.00 | 99.89 |
| agro_industry_and_commerce | 342.12 | 109.90 | 99.00 |
| musical_instruments | 281.62 | 100.60 | 999.87 |
| small_appliances | 280.78 | 10.00 | 999.99 |
| fixed_telephony | 225.69 | 10.00 | 99.90 |
| construction_tools_safety | 208.99 | 100.90 | 99.90 |
| _… | _… | _… | _…_ |

#### Q5. Order volume vs revenue per category

*Chart 4* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       COUNT(DISTINCT i.order_id) AS orders,
       ROUND(SUM(i.price),2) AS revenue,
       ROUND(SUM(i.price)/COUNT(DISTINCT i.order_id),2) AS revenue_per_order
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY revenue DESC LIMIT 15
```

**Verified result** (15 rows):

| Category | Orders | Revenue | Revenue Per Order |
|---|---|---|---|
| health_beauty | 8,836 | 1,258,681.34 | 142.45 |
| watches_gifts | 5,624 | 1,205,005.68 | 214.26 |
| bed_bath_table | 9,417 | 1,036,988.68 | 110.12 |
| sports_leisure | 7,720 | 988,048.97 | 127.99 |
| computers_accessories | 6,689 | 911,954.32 | 136.34 |
| furniture_decor | 6,449 | 729,762.49 | 113.16 |
| cool_stuff | 3,632 | 635,290.85 | 174.91 |
| housewares | 5,884 | 632,248.66 | 107.45 |
| _… | _… | _… | _…_ |

#### Q6. Market share of top 10 categories

*Advanced feature* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
WITH filtered AS (
    SELECT t.product_category_name_english AS category, SUM(i.price) AS revenue
    FROM order_items i
    JOIN orders o      ON i.order_id = o.order_id
    JOIN products p    ON i.product_id = p.product_id
    JOIN categories t  ON p.product_category_name = t.product_category_name
    WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
    GROUP BY category
)
SELECT category, ROUND(revenue,2) AS revenue,
       ROUND(100.0*revenue/(SELECT SUM(revenue) FROM filtered),2) AS pct_share
FROM filtered ORDER BY revenue DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Revenue | Pct Share |
|---|---|---|
| health_beauty | 1,258,681.34 | 9.39 |
| watches_gifts | 1,205,005.68 | 8.99 |
| bed_bath_table | 1,036,988.68 | 7.73 |
| sports_leisure | 988,048.97 | 7.37 |
| computers_accessories | 911,954.32 | 6.80 |
| furniture_decor | 729,762.49 | 5.44 |
| cool_stuff | 635,290.85 | 4.74 |
| housewares | 632,248.66 | 4.72 |
| _… | _… | _…_ |

#### Q7. Category translation join loss

*Data quality* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT (SELECT COUNT(DISTINCT product_category_name) FROM products
         WHERE product_category_name IS NOT NULL)                        AS distinct_cats_in_products,
       (SELECT COUNT(*) FROM categories)                                 AS translation_rows,
       (SELECT COUNT(*) FROM products p LEFT JOIN categories t
          ON p.product_category_name=t.product_category_name
         WHERE t.product_category_name IS NULL)                         AS products_dropped,
       (SELECT COUNT(*) FROM products WHERE product_category_name IS NULL) AS null_category_names
```

**Verified result** (1 row):

| Distinct Cats In Products | Translation Rows | Products Dropped | Null Category Names |
|---|---|---|---|
| 74 | 71 | 623 | 0 |

#### Q8. Long tail: bottom 10 categories by revenue

*Insight* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       ROUND(SUM(i.price),2) AS revenue,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY revenue ASC LIMIT 10
```

**Verified result** (10 rows):

| Category | Revenue | Orders |
|---|---|---|
| security_and_services | 283.29 | 2 |
| fashion_childrens_clothes | 569.85 | 8 |
| cds_dvds_musicals | 730.00 | 12 |
| home_comfort_2 | 760.27 | 24 |
| flowers | 1,110.04 | 29 |
| diapers_and_hygiene | 1,567.59 | 27 |
| arts_and_craftmanship | 1,814.01 | 23 |
| la_cuisine | 2,054.99 | 13 |
| _… | _… | _…_ |

#### Q9. Freight burden by category (top 10)

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       ROUND(SUM(i.freight_value),2) AS freight,
       ROUND(100.0*SUM(i.freight_value)/SUM(i.price),1) AS freight_pct_of_price
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY freight DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Freight | Freight Pct Of Price |
|---|---|---|
| bed_bath_table | 204,693.04 | 19.70 |
| health_beauty | 182,566.73 | 14.50 |
| furniture_decor | 172,749.30 | 23.70 |
| sports_leisure | 168,607.51 | 17.10 |
| computers_accessories | 147,318.08 | 16.20 |
| housewares | 146,149.11 | 23.10 |
| watches_gifts | 100,535.93 | 8.30 |
| garden_tools | 98,962.75 | 20.40 |
| _… | _… | _…_ |

#### Q10. Category growth 2017 vs 2018

*Analysis* · **not filterable** — this is a whole-dataset fact, so it deliberately has no `?` guard

```sql
SELECT t.product_category_name_english AS category,
       ROUND(SUM(CASE WHEN strftime('%Y',o.order_purchase_timestamp)='2017' THEN i.price ELSE 0 END),2) AS gmv_2017,
       ROUND(SUM(CASE WHEN strftime('%Y',o.order_purchase_timestamp)='2018' THEN i.price ELSE 0 END),2) AS gmv_2018
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
GROUP BY category ORDER BY gmv_2018 DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Gmv 2017 | Gmv 2018 |
|---|---|---|
| health_beauty | 481,755.71 | 772,238.15 |
| watches_gifts | 492,794.50 | 708,850.94 |
| bed_bath_table | 498,440.43 | 538,069.26 |
| sports_leisure | 452,148.84 | 532,566.49 |
| computers_accessories | 405,078.69 | 505,476.31 |
| housewares | 231,073.49 | 399,888.10 |
| furniture_decor | 337,213.12 | 386,668.59 |
| auto | 243,255.71 | 347,631.15 |
| _… | _… | _…_ |

#### Q11. Product count per category (top 10)

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT t.product_category_name_english AS category,
       COUNT(DISTINCT p.product_id) AS products,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN orders o      ON i.order_id = o.order_id
JOIN products p    ON i.product_id = p.product_id
JOIN categories t  ON p.product_category_name = t.product_category_name
WHERE (? = '[]' OR t.product_category_name_english IN (SELECT value FROM json_each(?)))
GROUP BY category ORDER BY products DESC LIMIT 10
```

**Verified result** (10 rows):

| Category | Products | Orders |
|---|---|---|
| bed_bath_table | 3,029 | 9,417 |
| sports_leisure | 2,867 | 7,720 |
| furniture_decor | 2,657 | 6,449 |
| health_beauty | 2,444 | 8,836 |
| housewares | 2,335 | 5,884 |
| auto | 1,900 | 3,897 |
| computers_accessories | 1,639 | 6,689 |
| toys | 1,411 | 3,886 |
| _… | _… | _…_ |

#### Q12. Revenue per state, top 10

*Analysis* · **filterable** — call with `multi_params(...)`; the table below is the `All` result

```sql
SELECT c.customer_state AS state,
       ROUND(SUM(i.price),2) AS revenue,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN orders o    ON i.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
GROUP BY state ORDER BY revenue DESC LIMIT 10
```

**Verified result** (10 rows):

| State | Revenue | Orders |
|---|---|---|
| SP | 5,202,955.05 | 41,375 |
| RJ | 1,824,092.67 | 12,762 |
| MG | 1,585,308.03 | 11,544 |
| RS | 750,304.02 | 5,432 |
| PR | 683,083.76 | 4,998 |
| SC | 520,553.34 | 3,612 |
| BA | 511,349.99 | 3,358 |
| DF | 302,603.94 | 2,125 |
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
