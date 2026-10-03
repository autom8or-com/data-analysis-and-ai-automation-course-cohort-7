# Phase 2c — Capstone Project
## PORA Academy Cohort 7 · Data Analysis & AI Automation

**Duration:** 4 weeks (8 facilitated sessions, Wed + Thu)
**Dataset:** Olist Brazilian E-Commerce — the same 11 CSVs you used in Phase 2a and 2b
**Deliverable:** A deployed Streamlit dashboard + a written report + a 10-minute group presentation
**Tool:** Streamlit, deployed to Streamlit Community Cloud via GitHub

> You arrive with 8 weeks of Python and 8 weeks of SQL on this exact data. Phase 2c is
> where those become one production artefact. The bar is deliberately higher than anything
> so far: **it must be deployed to a public URL**, not demonstrated from your laptop.

---

## The Four Teams

Your team was assigned in Phase 1 and carries through unchanged. Each team builds a
dashboard with a different analytical focus on the same 11 tables.

| Team | Focus area | Phase 1 dataset you came from |
|---|---|---|
| **Group 1** | [Customer Satisfaction](group-1-customer-satisfaction/README.md) | Amazon Reviews — 50,000 reviews, 20,290 products, 2002–2012 |
| **Group 2** | [Product Category Performance](group-2-product-category-performance/README.md) | Superstore — 9,994 transactions, 3 categories, 4 regions |
| **Group 3** | [Seller Performance](group-3-seller-performance/README.md) | Bestselling Books — 550 books, 2 genres, 2009–2019 |
| **Group 4** | [Revenue & Growth](group-4-revenue-and-growth/README.md) | UCI Online Retail — 541,909 transactions, full teaching dataset |

Open your team's README for its brief, its required charts, and **12 pre-validated SQL
queries with real results**. Those queries are your starting point — every one has been
run against this dataset and the result shown is the result you will get.

---

## How Your Team Is Split

Each team is **30 students, working as 3 sub-groups of 10**. You share one repository and
one deployment. Split the work by layer so nobody is editing the same file:

| Sub-group | Owns | Hands off |
|---|---|---|
| **A — Data** | The SQL queries behind every KPI and chart | A clean query module |
| **B — Visualisation** | The 4 charts and the KPI row | Chart functions that take a filtered frame |
| **C — Interactivity & Deploy** | Sidebar filters, GitHub, Streamlit Cloud | A live public URL |

Agree this split in your first session and write it down. 30 people editing one `app.py`
is how Week 2 goes wrong.

---

## Critical Data Rules — All Teams

These were verified against the dataset. Following them is the difference between a
number that is right and a number that looks right.

### 1. GMV means all orders, not just delivered

```sql
SELECT SUM(price + freight_value) FROM order_items   -- no join to orders, no status filter
-- = 15,843,553.24
```

This is the definition Phase 2b Week 8 verified (13,591,643.70 product + 2,251,909.54
freight). If you add `WHERE order_status = 'delivered'` you get **15,419,773.75** — a
different, also correct, question. Pick one, label it clearly on the dashboard, and say
which you used in your report.

### 2. `reviews` and `payments` are fan-out tables

| Table | Rows | Distinct orders |
|---|---|---|
| `reviews` | 99,224 | 98,673 |
| `payments` | 103,886 | 99,440 |

543 orders carry 2 reviews and 4 carry 3. Some orders have multiple payment rows too.
**Any order count that crosses a join needs `COUNT(DISTINCT order_id)`, never `COUNT(*)`.**
A plain `COUNT(*)` here overstates order volumes by thousands.

### 3. Count customers by `customer_unique_id`, not `customer_id`

`customers` has 99,441 rows but only **96,096** distinct `customer_unique_id` values.
`customer_id` is one row per *order*; `customer_unique_id` is one row per *person*. If you
say "customers", you mean the second one, or you will overstate your customer base by 3,345.

### 4. The category join quietly drops 623 products

Products reference **74** distinct category names, but `product_category_name_translation`
only has **71** rows. A query that joins `categories` therefore loses **623 products** and
their order items — R$185,049.76 of item revenue. There are **zero** null
`product_category_name` values, so "filtering out nulls" is not the fix. State what you did
with the dropped items.

### 5. 2016 and 2018 are both partial years, and November 2016 is empty

| Year | Months with any order | Orders |
|---|---|---|
| 2016 | Sep, Oct, Dec — **November is empty** | 329 |
| 2017 | Full year | 45,101 |
| 2018 | 1 Jan – 17 Oct | 54,011 |

A monthly chart across 2016 will show September, October, a gap, then December. **That gap
is real — November 2016 contains zero orders.** It is not a plotting failure and you must
not interpolate across it. 2016 has three active months, not four.

Any year-over-year chart is misleading unless both partial years are flagged. Putting 2016
next to 2017 without the caveat will cost you marks.

**And 775 orders have no line items at all** (99,441 orders, 98,666 with items). So three
different "order count" figures are all defensible, and they are not equal:

| Measure | 2016 | Total |
|---|---|---|
| Orders in the `orders` table | **329** | 99,441 |
| Orders that have ≥1 line item | 312 | 98,666 |
| Rows in `order_items` | 370 | 112,650 |

An order-level chart and an item-level chart will disagree, and that is not a bug. Say
which grain you are counting at. **Never label an `order_items` row count "orders."**

### 6. The filter contract — one convention, all four teams

Your starter queries are given as the **unfiltered reference** — that is the point of the
result tables. When you wire up a chart, add the guards below. Do not build SQL with
f-strings. There is one convention and everyone uses it:

```python
import json

selected_year  = st.sidebar.selectbox("Year", ["All", "2016", "2017", "2018"])
selected_state = st.sidebar.multiselect("State", STATES, default=["All"])

# "All" collapses to an empty JSON array, which the guard reads as "no filter"
state_json = json.dumps([] if "All" in selected_state else list(selected_state))

def year_params(year):                 # year guard only  -> 2 placeholders
    return (year, year)

def multi_params(multi_json):          # multiselect guard only -> 2 placeholders
    return (multi_json, multi_json)

def year_multi(year, multi_json):      # both guards -> 4 placeholders
    return (year, year, multi_json, multi_json)
```

```sql
-- Year guard — 2 placeholders
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
-- Multi-select guard — 2 placeholders (the same JSON string twice)
  AND (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
```

**Match the helper to the query's guards.** sqlite3 raises `Incorrect number of bindings`
when they disagree, and that is the most common filter bug there is:

| Query has | Use | Placeholders |
|---|---|---|
| year guard only | `year_params(year)` | 2 |
| multiselect guard only | `multi_params(multi_json)` | 2 |
| both guards | `year_multi(year, multi_json)` | 4 |

`multi_params` is the same for state, category and payment-type multiselects — the Python
shape is identical, only the column in the SQL differs. Nothing else. Every query in the
team READMEs is labelled with the helper it needs, or marked **not filterable** where the
question is a whole-dataset fact (fan-out counts, join-loss checks, the tier census, a
year-over-year comparison).

**Worked example — Group 4's monthly GMV trend, filterable.** This is the same query as
Q2 in the Group 4 README, with the guards added:

```python
def chart_monthly_gmv(conn, year):
    df = pd.read_sql('''
        SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
               ROUND(SUM(i.price + i.freight_value),2) AS gmv
        FROM orders o JOIN order_items i ON o.order_id = i.order_id
        WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
        GROUP BY month ORDER BY month
    ''', conn, params=year_params(year))
    ...
```

Verified: with `params=("All","All",...)` it returns **15,843,553.24 across 24 months** —
byte-identical to the Q2 table in your README. With `("2017","2017",...)` it returns
7,142,672.43 across 12 months. Add the guards to your own charts the same way; the SELECT,
GROUP BY and ORDER BY never change.

Two consequences worth knowing:
- **With `All` selected, the numbers are identical to the tables in your team README.**
  That is the contract: filters off reproduces your brief exactly.
- **Clearing the state multiselect shows all states, not none** — empty `[]` is read as
  "no filter". If you want empty to mean "no data", handle that in Python before the query.

### 7. Two sets of numbers, on purpose

Your team README's **headline KPI table is the unfiltered reference** and must stay
reproducible. The **dashboard shows filtered values**, with the active filter visible on
screen. They agree exactly when filters are `All`.

So a `Total Orders` metric reading 45,101 is not a bug when the year filter is on 2017. A
team that can toggle back to `All` and reproduce the table is demonstrating they understand
their own dashboard — that is worth marks.

### 8. Olist's `payment_installments` is text, and has two zero rows

`ORDER BY payment_installments` sorts `10` before `2` — cast it. Max instalments is **24**,
not 12. And **2 credit-card rows have `payment_installments = 0`**, which is not a real
instalment count; decide how to handle them and say so.

### 9. Delivery days are fractional

Timestamps carry a time component, so `JULIANDAY(delivered) - JULIANDAY(purchased)` returns
fractions (e.g. 12.56, not 13). The headline average is **12.56 days**. If you truncate to
whole dates you get 12.50 — a different number from the same data. Pick one method and be
consistent across your dashboard, report, and presentation.

---

## Weekly Milestones

Each week ends with a gate. You do not advance until the gate is met.

| Week | Focus | Gate — you are not done until |
|---|---|---|
| **1** | Pipeline, app skeleton, 3 KPIs | App runs end to end; 3 SQL queries verified against the numbers in your brief |
| **2** | Core dashboard build | 4 required charts, **each a function with the `?` guards already in place**; one sidebar filter wired to all of them |
| **3** | Tabs, filters, advanced feature | App split into 3 tabs; filters update every chart; **chart 5 (advanced feature) built and working**; one-paragraph finding per chart |
| **4** | Deployment + presentation | **Live public URL**, tested, loading data; 10-minute talk rehearsed |

Deployment is a Week 4 gate, not a Week 3 task. Test your repo in Week 3 — a broken
`requirements.txt` found on Thursday is an unrecoverable Thursday.

**The shape of your app — one file, one URL, three tabs:**

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "<Your Team Theme>", "Detail & Method"])

with tab_overview:
    ...   # 4 KPI metrics + chart 1 (your headline)
with tab_theme:
    ...   # charts 2, 3, 4
with tab_detail:
    ...   # chart 5 — the advanced feature — plus a written data-limitation note
```

`st.tabs` runs every tab's code on each rerun. With eight in-memory SQLite tables that costs
milliseconds — do not try to optimise it away.

---

## Assessment — 70 Marks

The capstone carries **70%** of the Phase 2 grade. The Phase 2b exercise portfolio carries
the remaining **30%**.

### Dashboard — 40 marks

| Criterion | Marks |
|---|---|
| App is deployed and loads from its public URL | 7 |
| KPIs and charts update correctly when filters change (every chart, not some) | 8 |
| 4 required charts **+ the advanced feature**, all labelled and readable; extras earn credit | 10 |
| SQL is correct and matches the verified benchmarks; parameterised, not f-strings | 9 |
| Code quality: every chart a function; `@st.cache_resource` on the connection; no hardcoded values; no `COUNT(*)` across a join | 6 |

**Four required charts is a floor, not a target.** A fifth and sixth chart of your own
choosing, if they are filter-driven and SQL-correct, earn credit. Extra charts that are
wrong lose marks — the bar is quality per chart, not count.

### Presentation — 20 marks

| Criterion | Marks |
|---|---|
| Live demo of the deployed app, not screenshots | 5 |
| Three business insights, each backed by a number on screen | 9 |
| Awareness of a data limitation and what you'd do with more time | 3 |
| Delivery and clarity; every team member speaks | 3 |

### Report — 10 marks

Data cleaning methodology and insight, written up. Not a dashboard description — a record
of what you did to the data and what you concluded.

| Criterion | Marks |
|---|---|
| Cleaning methodology: what you changed, why, and what you chose not to change | 5 |
| Insights written up with supporting figures | 3 |
| Limitations and caveats stated honestly | 2 |

**Suggested structure (2–3 pages is plenty):** data sources and grain → cleaning decisions
and their justification → how you handled the fan-out and join-loss problems → three
findings with figures → limitations and what you would investigate next.

---

## What to Hand In

| # | Artefact | Where |
|---|---|---|
| 1 | Deployed dashboard | Public Streamlit Community Cloud URL |
| 2 | Source repository | GitHub — `app.py`, `requirements.txt`, `data/` |
| 3 | Written report | PDF, 2–3 pages |
| 4 | Presentation | Slides, 10-minute delivery |

Minimum `requirements.txt`:

```
streamlit
pandas
matplotlib
seaborn
```

`sqlite3` is part of the Python standard library — no entry needed.

**Data deployment:** commit the 8 CSVs you actually use to a `data/` folder in your repo
(about 63 MB). Do **not** commit `olist_geolocation_dataset.csv` — it is 58 MB on its own
and no team brief uses it. If you do add it, expect slow cold starts and say so in your
limitations.

---

## Starter Material

Each team folder has a README with:

- your brief and required charts
- **12 pre-validated SQL queries**, each with the real result it produces
- the data rules above, trimmed to the ones that bite your team

You are expected to write your own queries too. These are the floor, not the ceiling —
and if you replace one, it must still return the same numbers unless you can explain why
they legitimately differ.
