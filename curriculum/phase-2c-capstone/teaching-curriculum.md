# Phase 2c — Capstone Project
## PORA Academy Cohort 7

**Duration:** 4 weeks (8 facilitated sessions: Wed + Thu × 4 weeks)
**Dataset:** Olist Brazilian E-Commerce (same as Phase 2a Python + Phase 2b SQL)
**Format:** All groups share the same facilitated sessions for core skills; group-specific analytical work happens in breakouts and between sessions
**Groups:** Same 4 project teams of 30 from Phase 1 (3 sub-groups of 10 each)
**Deliverable:** Deployed Streamlit dashboard (Streamlit Community Cloud) + written report (2–3 pages) + 10-minute group presentation

> **Curriculum principle:** Students arrive with 8 weeks of Python (Phase 2a) and 8 weeks of SQL (Phase 2b) — 16 weeks in total — on this exact dataset. Phase 2c consolidates those skills into a single production-grade deliverable. The technical bar is intentionally higher: the dashboard must be deployed, not just demonstrated in Colab.

---

## The Four Groups and Their Analytical Focus

Each group builds a Streamlit dashboard on the Olist dataset, focused on an analytical angle that connects back to their Phase 1 Excel project:

| Group | Phase 1 Theme | Phase 2c Dashboard Focus |
|---|---|---|
| **Group 1** | Customer Satisfaction (Amazon Reviews) | Order reviews, delivery performance, satisfaction drivers |
| **Group 2** | Product Category Performance (Superstore) | Category revenue rankings, product-level GMV analysis |
| **Group 3** | Publishing Intelligence → Seller Performance | Seller tiers, top performers, geographic distribution |
| **Group 4** | UK Retail Revenue | GMV trends, state-level revenue, payment behaviour |

All four dashboards draw from the same 11 Olist tables. The distinction is analytical focus and which joins/queries are most important.

---

## Verified Dataset Facts (Olist — from Phase 2a/2b)

All KPIs embedded in this curriculum were verified by running code against the actual dataset.

| Metric | Value |
|---|---|
| Total orders | **99,441** |
| Delivered orders | **96,478 (97.0%)** |
| Canceled orders | **625 (0.6%)** |
| Total GMV (all orders, price + freight) | **R$15,843,553.24** |
| Avg payment value | **R$154.10** |
| Credit card payments | **73.9%** |
| Avg review score | **4.09** |
| 5-star reviews | **57,328** |
| Top state by orders | **SP — 41,746** |
| Avg delivery time | **12.6 days** |
| Late deliveries | **7,826 (8.1%)** |
| Peak month (orders) | **Nov 2017 — 7,544** |
| Top revenue category | **health_beauty — R$1,258,681.34** |
| Top seller revenue | **R$229,472.63** |
| Total sellers | **3,095** |

> **GMV definition — read this before any group writes a GMV query.**
> GMV is `SUM(order_items.price + order_items.freight_value)` across **all** order items,
> with **no** `order_status` filter. This is the same definition Phase 2b Week 8 verified
> (product revenue 13,591,643.70 + freight 2,251,909.54 = **15,843,553.24**).
>
> A group that adds `WHERE order_status = 'delivered'` gets **R$15,419,773.75** instead.
> Both numbers are correct answers to different questions, and groups that
> present the delivered-only figure must say so explicitly. Use the all-orders
> figure for the headline KPI so it reconciles with Phase 2b and the README.

---

## Technical Stack

| Component | Tool |
|---|---|
| Language | Python 3 |
| Data loading | pandas |
| Database | SQLite in-memory via `sqlite3` — a plain Python script, so no `%%sql` magic |
| Dashboard framework | Streamlit |
| Visualisation | matplotlib / seaborn / plotly (group choice) |
| Development environment | Google Colab (pyngrok tunnel) |
| Production deployment | Streamlit Community Cloud (GitHub) |

**Data architecture pattern** (same as Phase 2b Colab setup):

```python
import sqlite3, pandas as pd, os

DATA_DIR = "/content/drive/MyDrive/olist/"

tables = {
    "orders":        "olist_orders_dataset.csv",
    "customers":     "olist_customers_dataset.csv",
    "order_items":   "olist_order_items_dataset.csv",
    "products":      "olist_products_dataset.csv",
    "sellers":       "olist_sellers_dataset.csv",
    "payments":      "olist_order_payments_dataset.csv",
    "reviews":       "olist_order_reviews_dataset.csv",
    "categories":    "product_category_name_translation.csv",
}

conn = sqlite3.connect(":memory:")
for name, file in tables.items():
    pd.read_csv(os.path.join(DATA_DIR, file)).to_sql(name, conn, if_exists="replace", index=False)
```

> **`olist_geolocation_dataset.csv` is deliberately excluded.** It is 1,000,163 rows /
> ~58 MB — over half the size of everything else combined — and **no group brief in this
> curriculum uses it.** Loading it costs every group a slow cold start on Streamlit
> Community Cloud for a table nothing queries. Groups that want a map can add it, but
> they should expect the deploy to take noticeably longer and say so in their
> limitations slide.

> **Why `pd.read_sql()` and not `%%sql`.** Phase 2b used the `%%sql` cell magic
> (jupysql), which only works inside a notebook. A Streamlit app is an ordinary Python
> script, so the capstone uses `sqlite3.connect()` + `pd.read_sql()` throughout.
> The SQL itself is identical — students are changing the *transport*, not the language.
> Call this out in Week 1; it is the single biggest conceptual jump from Phase 2b.

> **Table naming.** Olist's files are `olist_*_dataset.csv`; the short names above
> (`orders`, `order_items`, …) are what the SQL in the group briefs uses. Keep the mapping
> consistent — `payment_installments` is in `olist_order_payments_dataset.csv`, and the
> briefs refer to it as `payments`.

---

## Session Plan

### Week 1 — Foundation & Architecture

#### Wednesday (All Groups): Project Kickoff + Pipeline Setup

**Objective:** Reconstruct the Phase 2b data pipeline inside a Streamlit app skeleton. Every group leaves with a running app.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:20 | Capstone overview: what we're building, assessment criteria, deployment goal |
| 0:20–0:45 | Live demo: Streamlit skeleton + SQLite pipeline in Colab (pyngrok tunnel) |
| 0:45–1:15 | All groups: implement the skeleton in their own Colab notebooks |
| 1:15–1:45 | Groups read their group-specific brief (see below); identify 3 KPIs they will show |
| 1:45–2:00 | Each group states their 3 KPIs to the class — instructor validates |

**Streamlit skeleton to implement:**

```python
# app.py (written via %%writefile app.py in Colab)
import os
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Olist Dashboard", layout="wide")

# Switch to "data/" once deployed to Streamlit Community Cloud.
DATA_DIR = "/content/drive/MyDrive/olist/"

TABLES = {
    "orders":      "olist_orders_dataset.csv",
    "customers":   "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products":    "olist_products_dataset.csv",
    "sellers":     "olist_sellers_dataset.csv",
    "payments":    "olist_order_payments_dataset.csv",
    "reviews":     "olist_order_reviews_dataset.csv",
    "categories":  "product_category_name_translation.csv",
}

@st.cache_resource
def get_conn():
    """One shared in-memory SQLite connection for the whole app.

    @st.cache_resource, NOT @st.cache_data — cache_data requires the return value
    to be serialisable, and a live sqlite3.Connection is not. cache_resource is for
    exactly this: non-serialisable objects shared across reruns.
    """
    conn = sqlite3.connect(":memory:")
    for name, fname in TABLES.items():
        pd.read_csv(os.path.join(DATA_DIR, fname)).to_sql(name, conn, if_exists="replace", index=False)
    return conn

conn = get_conn()

st.title("Olist Dashboard — [Group Name]")
st.markdown("Data: Brazilian E-Commerce (Olist, 2016–2018)")

# --- KPI placeholders — hardcoded for now, replaced with live SQL on Thursday ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", "99,441")
col2.metric("Total GMV", "R$15.8M")
col3.metric("Avg Review Score", "4.09")
```

> **The skeleton must be copied exactly, including `DATA_DIR` and `TABLES`.** A truncated
> copy that omits them fails with `NameError: name 'TABLES' is not defined`, and every
> group hits this in the first ten minutes. If a group is stuck, check they pasted the
> whole block before debugging anything else.

**Assignment (between Wed and Thu):**
Each group writes 3 SQL queries (verified to run) that will power their 3 KPIs. Queries committed to a shared group notebook.

---

#### Thursday (Group Breakouts): KPI Queries + Wireframe

**Objective:** Replace hardcoded metric values with live SQL queries; sketch the full dashboard layout.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:15 | Quick share: each group shows their 3 queries — peer check for correctness |
| 0:15–1:00 | Groups implement `st.metric()` values from live SQL results |
| 1:00–1:30 | Paper wireframe: sketch 4-chart dashboard layout (where does each chart go?) |
| 1:30–2:00 | Instructor review: wireframe sign-off per group |

**Pattern: query → metric**

```python
total_orders = pd.read_sql("SELECT COUNT(*) as n FROM orders", conn).iloc[0]["n"]
col1.metric("Total Orders", f"{total_orders:,}")
```

**Assignment (Week 1 → Week 2):**
Each group writes all SQL queries needed for their 4 charts. Queries must be tested and returning correct results before Session 3.

---

### Week 2 — Core Dashboard Build

#### Wednesday (All Groups): First Chart + Layout

**Objective:** Build one complete chart (title, axis labels, data from SQL) and wire it into the Streamlit layout.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:20 | Instructor demo: full chart cycle (SQL → DataFrame → matplotlib → st.pyplot) |
| 0:20–1:00 | All groups implement their first chart in Streamlit |
| 1:00–1:30 | Introduce `st.sidebar` + `st.selectbox` — add one filter connected to chart |
| 1:30–2:00 | Groups troubleshoot; instructor reviews each running app |

**Chart pattern — write every chart as a function, from the first one:**

```python
import matplotlib.pyplot as plt

# Defined here so Week 2 charts run standalone. It is the same helper the full
# filter contract in Week 3 introduces alongside multi_params() and year_multi() — put it in a
# shared module (e.g. filters.py) and import it, don't redefine it per chart.
def year_params(year):
    """Query has 2 placeholders (year guard only)."""
    return (year, year)

def chart_monthly_orders(conn, year):
    """year is a single value: "All", "2016", "2017" or "2018".

    The ? guards are already in place, so this function works today with
    filters set to "All" and is unchanged when the sidebar arrives."""
    df = pd.read_sql("""
        SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
               COUNT(DISTINCT o.order_id) AS orders
        FROM orders o
        WHERE o.order_status = 'delivered'
          AND (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
        GROUP BY month ORDER BY month
    """, conn, params=year_params(year))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["month"], df["orders"], marker="o")
    ax.set_title("Monthly Orders (Delivered)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Orders")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    return fig
```

> **Two non-negotiables, decided in Week 2, not retrofitted in Week 3.**
> 1. **Every chart is a function**, not a top-level block. Thirty people appending chart
>    code to the bottom of `app.py` is how you get a 900-line file nobody can change.
> 2. **Every query has the `?` guards from day one**, even with no sidebar wired up yet.
>    Pass `params=("All","All",...)` until Week 3 and the function already works. The
>    alternative — adding filters later — means editing every query by hand, and it is
>    the single most common reason a Week 3 dashboard ends up with filters on some charts
>    and not others.
>
> Chart 1 below is the reference implementation. Every group's four charts follow it.

> **November 2016 has zero orders.** A 2016 monthly chart shows September, October, then a
> gap, then December. That gap is real — November 2016 is empty in this dataset, not a
> plotting failure. Do not "fix" it by interpolating. 2016 covers only 3 months with any
> order activity at all (Sep, Oct, Dec) and 329 orders.

**Assignment (between Wed and Thu):**
Build charts 2 and 3 from their wireframe. Must run without errors before Thursday.

---

#### Thursday (Group Breakouts): Complete Chart Set

**Objective:** All 4 charts implemented as functions, layout matches wireframe, app runs end-to-end.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:30 | Groups integrate charts 2 and 3 reviewed by instructor |
| 0:30–1:15 | Groups build chart 4 (group-specific — see briefs below) |
| 1:15–1:45 | Cross-group peer review: each group demos to one other group |
| 1:45–2:00 | Feedback collected; instructor sets quality bar for Week 3 |

**Instructor check at the 1:45 gate — all four, or the group falls behind in Week 3:**
each chart is a function · each query has `?` guards · each chart has a title, axis labels,
and a formatted axis · `app.py` is under ~200 lines.

**Assignment (Week 2 → Week 3):**
Polish: consistent colour scheme, chart titles, axis labels, formatted numbers (e.g. `f"R${value:,.2f}"`). Write a one-paragraph "key finding" for each chart.

---

### Week 3 — Interactivity, Polish & Peer Review

#### Wednesday (All Groups): Sidebar Filters + Tabs + Caching

**Objective:** Connect sidebar widgets to all charts so filtering by year or state updates the entire dashboard, and split the app into tabs.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:20 | Instructor demo: `st.sidebar.selectbox` → **parameterised** SQL → chart update |
| 0:20–0:50 | Groups add year filter connected to all charts |
| 0:50–1:20 | Add state filter (multiselect) — the `json_each` guard |
| 1:20–1:40 | `st.tabs` — split the app into Overview / Team Theme / Detail & Method |
| 1:40–2:00 | Caching: `@st.cache_resource` for the connection, `@st.cache_data` for DataFrames — cache raw tables, not filtered results |

**The filter contract — use this, do not invent your own.** All four teams share one
convention so that 30 people per team are not each solving string-building differently.
Two guards, both parameterised:

```python
import json

YEAR_OPTIONS = ["All", "2016", "2017", "2018"]

# ── In app.py, once ──────────────────────────────────────────────────────
selected_year  = st.sidebar.selectbox("Year", YEAR_OPTIONS)
selected_state = st.sidebar.multiselect("State", STATES, default=["All"])

# "All" collapses to an empty JSON array, which the guard below treats as no filter
state_json = json.dumps([] if "All" in selected_state else list(selected_state))
```

```sql
-- Year guard — 2 placeholders
WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)

-- Multi-select guard — 2 placeholders (the same JSON string, twice)
  AND (? = '[]' OR c.customer_state IN (SELECT value FROM json_each(?)))
```

**Three named helpers.** A query can carry a year guard, a multiselect guard, or both —
match the helper to the guards actually present, because sqlite3 raises `Incorrect number of
bindings` if the counts disagree, and that error is the single most common filter bug:

```python
def year_params(year):
    """Year guard only — 2 placeholders."""
    return (year, year)


def multi_params(multi_json):
    """Multiselect guard only — 2 placeholders.

    Same Python shape for a state, category or payment-type multiselect;
    only the column in the SQL differs."""
    return (multi_json, multi_json)

def year_multi(year, multi_json):
    """Both guards — 4 placeholders."""
    return (year, year, multi_json, multi_json)
```

| Query has | Use | Placeholders |
|---|---|---|
| year guard only | `year_params(year)` | 2 |
| multiselect guard only | `multi_params(multi_json)` | 2 |
| both guards | `year_multi(year, multi_json)` | 4 |

`multi_params` is the same for state, category and payment-type multiselects — the Python
shape is identical, only the column in the SQL differs.

> **Why three and not one.** A multiselect-only query is common — Group 3's seller-tier
> query filters by state and never mentions a date, so it needs two placeholders, not four.
> Reach for `year_multi` on it and you get `Incorrect number of bindings`; reach for
> `year_params` and you get the same error. Read the guards in the query, then pick.

```python
df = pd.read_sql("""
    SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
           COUNT(DISTINCT o.order_id) AS orders
    FROM orders o
    WHERE (? = 'All' OR strftime('%Y', o.order_purchase_timestamp) = ?)
      AND (? = '[]' OR o.customer_id IN
           (SELECT customer_id FROM customers
            WHERE ? = '[]' OR customer_state IN (SELECT value FROM json_each(?))))
    GROUP BY month ORDER BY month
""", conn, params=year_multi(selected_year, state_json))
```

> **Why not f-strings.** Building SQL with `f"...WHERE year = '{selected_year}'"` teaches a
> habit that breaks the moment a value comes from anywhere but a fixed dropdown — and the
> state filter is exactly that case, because an `IN` list of unknown length forces you to
> hand-build quotes and commas. The guard above is *shorter* than the string it replaces
> and cannot be broken by a quote in the data. Parameterised queries are the habit to keep.

> **`json_each()` is available** in the SQLite build students use (3.38+; Colab ships
> well past this). It reads a JSON array straight into an `IN` list, which is what makes
> the multiselect guard a one-liner.

> **The empty-selection trap.** If a user clears the state multiselect entirely, the value
> is `[]`, which this guard correctly reads as "no filter". So *clearing* the box shows all
> states, not none. Decide deliberately whether that is the behaviour you want, and if not,
> treat an empty selection as "no data" in Python before it reaches SQL.

**Unfiltered vs filtered — settle this before you build.** Your team README's headline KPI
table is the **unfiltered reference** and must stay reproducible. The dashboard shows
**filtered values with the active filter visible on screen**. When filters are `All`, the
two agree exactly. A team that can toggle back to `All` and reproduce the table is
demonstrating they understand their own dashboard.

**Assignment (between Wed and Thu):**
Add a `st.metric` row that recalculates when filters change (not hardcoded). Implement `st.divider()` and section headers with `st.subheader()`.

---

#### Thursday (Group Breakouts): Advanced Feature (Required) + Insight Writing

**Objective:** Each group completes its **required fifth chart** — the advanced feature from
its brief — on the Detail & Method tab, and drafts 3 business insights.

> **The advanced feature is no longer an optional extra.** It is chart 5 of 5, assessed
> under "4 required charts present, labelled, readable" and carried by the Insight
> criterion. The SQL is already written and verified in your team README. It is one hour
> of work, not a redesign — there is no excuse for a team reaching Week 4 without it.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–1:00 | Groups implement the advanced feature as a chart function on the Detail & Method tab (queries pre-validated in your team README) |
| 1:00–1:30 | Write 3 business insights: each backed by a chart/KPI in the dashboard |
| 1:30–2:00 | Full app demo + instructor sign-off — app must run from top to bottom |

**Tab structure — the final shape of your app:**

```python
tab_overview, tab_theme, tab_detail = st.tabs(
    ["Overview", "<Your Team Theme>", "Detail & Method"])

with tab_overview:
    # 4 KPI metrics + chart 1 (your headline)
    pass
with tab_theme:
    # charts 2, 3, 4
    pass
with tab_detail:
    # chart 5 — the advanced feature — plus a written data-limitation note
    pass
```

One file, one URL, three tabs. `st.tabs` runs every tab's code on each rerun, so with eight
in-memory SQLite tables the cost is milliseconds — do not try to optimise it away.

**Extras are welcome and rewarded.** Four required charts is a floor, not a ceiling. A
fifth and sixth chart of a group's own choosing, if they are filter-driven and SQL-correct,
earn credit under Dashboard marks. A team that adds charts nobody asked for and gets them
wrong has lost marks, not gained them.

**Assignment (Week 3 → Week 4):**
GitHub repository setup: create repo, commit `app.py`, `requirements.txt`, data files (8 CSVs, no geolocation). Test the full app in the repo before Week 4 — a broken `requirements.txt` found on Thursday is an unrecoverable Thursday.

---

### Week 4 — Deployment & Presentations

#### Wednesday (All Groups): Streamlit Community Cloud Deployment

**Objective:** Every group has a live public URL for their dashboard before the end of the session.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:20 | Instructor demo: GitHub repo → Streamlit Community Cloud → deployed app |
| 0:20–1:15 | Groups deploy (GitHub account required; instructor helps with `requirements.txt`) |
| 1:15–1:45 | Test deployed app: does it load correctly? Does filtering work? |
| 1:45–2:00 | Final presentation structure briefing (10 min per group format) |

**`requirements.txt` template:**
```
streamlit
pandas
matplotlib
seaborn
```

*(SQLite3 is part of Python's standard library — no entry needed.)*

**Data note for deployment:** Olist CSVs are committed to the GitHub repo in a `data/` folder. In `app.py`, the data path switches from Google Drive to relative: `DATA_DIR = "data/"`. Excluding `olist_geolocation_dataset.csv` (see the note in Technical Stack) keeps the payload at roughly **63 MB** per group repo — commit 8 files, not 9. If a group adds geolocation, warn them their first cold start will be slow.

**Assignment (Week 4 Wed → Thu):**
Rehearse 10-minute presentation. All group members must speak. Presentation must include: what the dashboard shows, 3 business insights, one limitation of the data.

---

#### Thursday: Final Presentations

**Format:** Each group presents for 10 minutes. Order determined by draw.

**Presentation structure (10 min):**

| Section | Time |
|---|---|
| What the dashboard shows and who it's for | 1 min |
| Live demo of the deployed app (3 charts minimum) | 4 min |
| 3 business insights backed by the data | 3 min |
| One data limitation and what you'd do with more time | 2 min |

---

## Group-Specific Briefs

---

### Group 1 — Customer Satisfaction Dashboard

**Olist focus:** Order reviews, delivery performance, satisfaction drivers

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total reviews | **99,224** |
| Avg review score | **4.09** |
| 5-star reviews | **57,328 (57.8%)** |
| 1-star reviews | **11,424 (11.5%)** |
| Late deliveries | **7,826 (8.1%)** |
| Avg delivery days (on-time) | **10.88 days** (n=88,171 orders, avg score 4.294) |
| Avg delivery days (late) | **31.39 days** (n=7,661 orders, avg score 2.566) |
| Avg days late (when late) | **9.55 days** |

**4 required charts:**

1. **Review score distribution** — bar chart (1 to 5 stars; counts and %)
2. **Monthly avg review score** — line chart (trend over time; look for dip around Nov 2017 peak)
3. **Avg review score by state** — horizontal bar (top 10 states by order volume)
4. **On-time vs late delivery by state** — grouped bar (top 5 states)

**Sidebar filters:** Year, State (top 5 + All), Delivery status (On Time / Late / All)

**Advanced feature (Week 3 Thursday):**
Delivery performance impact on score. Add a chart showing avg review score for on-time vs late deliveries — quantify the satisfaction cost of a late delivery.

```sql
SELECT
    CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
         THEN 'On Time' ELSE 'Late' END AS delivery_status,
    ROUND(AVG(r.review_score), 3) AS avg_score,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status
```

> **`COUNT(DISTINCT o.order_id)`, not `COUNT(*)`.** This joins `orders` to `reviews`, and
> `reviews` is a fan-out table: 99,224 review rows cover only 98,673 distinct orders —
> 543 orders carry 2 reviews and 4 carry 3. A plain `COUNT(*)` counts *review rows*, not
> orders, and overstates the totals by 529 (7,700 instead of 7,661 late; 88,661 instead of
> 88,171 on time). This is the same fan-out trap covered in Phase 2b Week 6; groups that
> already learned it should apply it here unprompted. `AVG(review_score)` is still
> review-weighted, which is the intended reading — "average score given", not
> "average score per order".

**Expected finding (verified):** On-time deliveries average **4.294**; late deliveries average
**2.566** — a gap of **1.73 stars**. Late orders are 7,661 of 95,832 on-time/late delivered
orders with a review (8.0%). Groups must state these exact figures, not a range.

---

### Group 2 — Product Category Performance Dashboard

**Olist focus:** Category revenue rankings, product-level GMV analysis

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total GMV (all orders) | **R$15,843,553.24** |
| Top category (revenue) | **health_beauty — R$1,258,681.34** |
| Total product categories | **71** (translated, after the `categories` join) |
| Distinct categories referenced by products | **74** (3 have no translation row) |
| Avg item price | **R$120.65** (across 112,650 order items) |

**4 required charts:**

1. **Top 10 categories by revenue** — horizontal bar (use `product_category_name_translation` for English names)
2. **Category revenue over time** — stacked or grouped bar by quarter (top 5 categories)
3. **Price distribution by category** — box plot or avg price bar (top 10 categories)
4. **Order volume vs revenue per category** — scatter plot (volume on x, revenue on y — identify over/underperformers)

**Sidebar filters:** Year, Category (selectbox from top 15 + All)

**Key join:**

```sql
SELECT t.product_category_name_english AS category,
       SUM(i.price) AS revenue,
       COUNT(DISTINCT i.order_id) AS orders
FROM order_items i
JOIN products p ON i.product_id = p.product_id
JOIN categories t ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY revenue DESC
```

**Advanced feature (Week 3 Thursday):**
Category market share chart. Show what % of total GMV each of the top 10 categories represents. Add a note on whether any single category dominates.

**Verified market shares** — share of **translated item revenue** (denominator
R$13,406,593.94, i.e. `SUM(price)` over items that survive the `categories` join; freight is
not attributable to a category):

| Category | Revenue | % of translated item revenue |
|---|---|---|
| health_beauty | R$1,258,681.34 | **9.39%** |
| watches_gifts | R$1,205,005.68 | 8.99% |
| bed_bath_table | R$1,036,988.68 | 7.73% |
| sports_leisure | R$988,048.97 | 7.37% |
| computers_accessories | R$911,954.32 | 6.80% |
| **Top 10 combined** | **R$8,475,957.56** | **63.22%** |

**Expected finding:** No single category dominates. `health_beauty` leads at **9.39%**, and
the top 10 categories together reach **63.22%** — a substantial long tail of the remaining
37%. A group claiming one category "dominates" is overstating it.

> **Denominator matters — state which you used.** The two defensible denominators give
> different answers: **9.39%** against translated item revenue (R$13,406,593.94) or
> **9.26%** against *all* item revenue (R$13,591,643.70). The 0.13pp difference is the
> R$185,049.76 of item revenue lost to un-translated categories. Either is defensible;
> the marks are for stating it.

---

### Group 3 — Seller Performance Dashboard

**Olist focus:** Seller tiers, top performers, geographic distribution

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total sellers | **3,095** |
| Top seller revenue | **R$229,472.63** |
| Top Tier sellers (≥ R$100K) | **18** |
| High Performer (R$50K–R$100K) | **22** |
| Mid Tier (R$10K–R$50K) | **252** |
| Standard (< R$10K) | **2,803** |
| Top seller state | **SP** |

**4 required charts:**

1. **Seller tier distribution** — pie or donut (count of sellers per tier)
2. **Top 20 sellers by revenue** — horizontal bar
3. **Revenue by seller state** — horizontal bar (top 10 states)
4. **Revenue concentration** — cumulative % chart: what % of sellers generate 80% of revenue?

**Sidebar filters:** Year, State, Tier

**Seller tier query (from Phase 2b Week 8):**

```sql
WITH seller_revenue AS (
    SELECT s.seller_id, s.seller_state,
           SUM(i.price) AS total_revenue
    FROM order_items i
    JOIN sellers s ON i.seller_id = s.seller_id
    GROUP BY s.seller_id, s.seller_state
),
seller_tiers AS (
    SELECT *,
           CASE WHEN total_revenue >= 100000 THEN 'Top Seller'
                WHEN total_revenue >= 50000  THEN 'High Performer'
                WHEN total_revenue >= 10000  THEN 'Mid Tier'
                ELSE 'Standard' END AS tier
    FROM seller_revenue
)
SELECT tier, COUNT(*) AS sellers, SUM(total_revenue) AS revenue
FROM seller_tiers
GROUP BY tier
ORDER BY revenue DESC
```

**Advanced feature (Week 3 Thursday):**
Pareto analysis. Build a chart showing that the top 40 sellers (Top Tier + High Performer)
generate a disproportionate share of GMV. Calculate and display the exact percentage on the dashboard.

**Verified (computed against the Olist data):** the top 40 sellers — **1.29%** of all 3,095
sellers — account for **29.54%** of total item revenue (R$4,014,922.70 of R$13,591,643.70).
The remaining 2,963 sellers share the other ~70%. That is the headline Group 3 insight, and
it is what justifies the tier structure in the brief above.

---

### Group 4 — Revenue & Growth Dashboard

**Olist focus:** GMV trends, state-level revenue, payment behaviour

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total GMV (all orders) | **R$15,843,553.24** |
| Peak GMV month | **Nov 2017 — R$1,179,143.77** |
| Top state by GMV | **SP — R$5,921,678.12** (41,375 orders) |
| 2nd state | **RJ — R$2,129,681.98** (12,762 orders) |
| 3rd state | **MG — R$1,856,161.49** (11,544 orders) |
| Credit card share | **73.9%** |
| Avg payment value | **R$154.10** |

**4 required charts:**

1. **Monthly GMV trend** — line chart (full timeline; annotate Nov 2017 peak)
2. **Revenue by state** — horizontal bar (top 10 states)
3. **Payment method breakdown** — pie chart (credit card, boleto, voucher, debit card)
4. **Year-over-year GMV comparison** — grouped bar (2016 vs 2017 vs 2018 by month, or by quarter)

**Sidebar filters:** Year, State (top 5 + All), Payment type

**Monthly GMV query:**

```sql
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       SUM(i.price + i.freight_value) AS gmv
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
GROUP BY month
ORDER BY month
```

> **No `WHERE order_status = 'delivered'`.** This query sums to **R$15,843,553.24**,
> matching the headline KPI and Phase 2b Week 8. Adding a delivered filter drops it to
> R$15,419,773.75 and no longer reconciles with the rest of this brief. See the GMV
> definition note near the top of this document.

**Verified year-over-year figures** (for chart 4, same all-orders definition):

| Year | Orders | GMV | Note |
|---|---|---|---|
| 2016 | 370 | R$57,183.21 | **Partial year** — 4 Sep to 23 Dec only |
| 2017 | 50,864 | R$7,142,672.43 | Full year |
| 2018 | 61,416 | R$8,643,697.60 | 1 Jan to 17 Oct only |

**Advanced feature (Week 3 Thursday):**
Payment instalment analysis. Olist payment data includes instalment counts. Show the distribution of instalments (1 instalment, 2, 3, … up to the observed maximum) and calculate: do customers paying in more instalments spend more per order? This connects to creditworthiness and marketing strategy.

```sql
SELECT payment_installments,
       COUNT(*) AS transactions,
       AVG(payment_value) AS avg_value
FROM payments
WHERE payment_type = 'credit_card'
GROUP BY payment_installments
ORDER BY CAST(payment_installments AS INTEGER)
```

> **Two data quirks to expect (both verified).**
> 1. **The maximum is 24 instalments, not 12.** The brief originally said "1 … 12+"; the
>    observed credit-card range is 0–24. A chart capped at 12 silently truncates real
>    transactions. Order by `CAST(payment_installments AS INTEGER)` — the column is text,
>    so a plain `ORDER BY payment_installments` sorts `10` before `2`.
> 2. **Two credit-card rows have `payment_installments = 0`**, which is not a meaningful
>    instalment count. Groups must decide whether to drop them, bucket them as "unknown",
>    or include them — and say which. Silently charting a "0 instalments" bar is a
>    data-quality error, and calling it out earns credit in the limitations section.

---

## Deliverables and Assessment

**The capstone carries 70% of the Phase 2 grade. The Phase 2b exercise portfolio carries
the remaining 30%.** The 70 marks split three ways: Dashboard 40, Presentation 20,
Report 10.

### Dashboard (40 marks)

| Criterion | Marks |
|---|---|
| App is deployed and loads from its public URL | 7 |
| KPIs and charts update correctly when filters change (every chart, not some) | 8 |
| 4 required charts + the advanced feature, all labelled and readable; extras earn credit | 10 |
| SQL is correct and values match the verified benchmarks; parameterised, not f-strings | 9 |
| Code quality: every chart a function; `@st.cache_resource` on the connection; no hardcoded values; no `COUNT(*)` across a join | 6 |

### Presentation (20 marks)

| Criterion | Marks |
|---|---|
| Live demo of deployed app (not screenshots) | 5 |
| 3 business insights, each backed by a number on screen | 9 |
| Awareness of a data limitation and what you'd do with more time | 3 |
| Delivery and clarity; every team member speaks | 3 |

### Report (10 marks)

Data cleaning methodology and insight, written up. **Not a description of the dashboard** —
a record of what was done to the data and what was concluded. 2–3 pages is plenty.

| Criterion | Marks |
|---|---|
| Cleaning methodology: what was changed, why, and what was deliberately left alone | 5 |
| Insights written up with supporting figures | 3 |
| Limitations and caveats stated honestly | 2 |

**Suggested structure:** data sources and grain → cleaning decisions and their
justification → how the fan-out and category join-loss problems were handled → three
findings with figures → limitations and what to investigate next.

The report and the presentation assess different things. The report rewards reasoning
about the data; the presentation rewards knowing it well enough to speak to it without
notes. A team can have one and not the other — mark them separately.

---

## Common Technical Issues and Solutions

| Issue | Solution |
|---|---|
| Colab session times out, SQLite connection lost | Wrap `get_conn()` in `@st.cache_resource` (not `cache_data`) — Streamlit recreates it on next run |
| `st.cache_data` used on a function returning a SQLite connection | `cache_data` needs a serialisable return value. Use `@st.cache_resource` for the connection, or cache the DataFrames instead: `@st.cache_data def load_orders(): return pd.read_sql(...)` |
| Filter changes don't update charts | Every query needs the `?` guards, not just some. If a chart ignores the filter, that query never got a guard — add it in Week 2, not Week 3 |
| Filter state is right but a KPI looks wrong | Decide unfiltered-vs-filtered deliberately. The team README table is the **unfiltered** reference; the dashboard shows **filtered** values with the active filter visible |
| Clearing the state multiselect shows everything, not nothing | Expected: the `? = '[]'` guard reads empty as "no filter". If you want empty to mean "no data", handle it in Python before the query |
| SQL built with f-strings from a dropdown value | Works until a value contains a quote, then breaks or leaks. Use `?` placeholders and `params=` — the `json_each` guard is shorter than the string building it replaces |
| November 2016 missing from a monthly chart | Not a bug — November 2016 has **zero orders** in this dataset. 2016 has only 3 active months (Sep, Oct, Dec) and 329 orders. Do not interpolate |
| Deployment fails: `ModuleNotFoundError` | Check `requirements.txt` — all imports must be listed |
| CSV not found on Streamlit Cloud | Confirm file is committed to the GitHub repo (not `.gitignored`) |
| f-string formatting with R$ | Use `f"R${value:,.2f}"` — comma separator, 2 decimal places |

---

## Instructor Notes

- **Weeks 1–2 are the hardest.** Students will struggle to connect SQL → pandas → Streamlit in one flow. The skeleton in Week 1 Wednesday is critical — do not skip it.
- **Deployment day (Week 4 Wednesday) almost always has problems.** Common: students forget to push data files to GitHub, or `requirements.txt` is missing a package. Budget 45–60 minutes for pure troubleshooting.
- **Group 2 note:** There are **0 products with a null `product_category_name`** — that concern is misplaced. The real loss is at the **translation join**: products reference **74** distinct category names, but `product_category_name_translation` only holds **71**, so **623 products** (and their order items) drop out of any query that joins `categories`. Groups must decide how to handle them — exclude and say so, or label "Unknown" — but must state which, and must not present category revenue as a share of total GMV without disclosing the dropped items.
- **Group 4 note:** 2016 data covers only 4 September – 23 December (329 orders) and 2018 only 1 January – 17 October (54,011). Both partial years must be flagged when comparing year-over-year; an unflagged YoY chart is misleading and should lose marks. Watch the grain: the `orders` table gives 329 orders for 2016, orders with line items give 312, and `order_items` rows give 370. Groups that label an `order_items` row count as "orders" should lose the SQL marks — three defensible counts exist and they must say which grain they used.
- **Group 3 note:** The Pareto finding is the headline insight: **40 sellers (1.29%) account for 29.54% of item revenue.** If a group quantifies this incorrectly, the presentation narrative falls apart — verify their number before sign-off. Watch for the fan-out error: the tier query joins `order_items` to `sellers`, and both are per-item, so `SUM(i.price)` is correct but any order count needs `COUNT(DISTINCT o.order_id)`.
- **All groups:** The Nov 2017 spike in orders is likely related to Black Friday. Groups that identify and name this in their presentation should receive bonus recognition for contextual analysis.
