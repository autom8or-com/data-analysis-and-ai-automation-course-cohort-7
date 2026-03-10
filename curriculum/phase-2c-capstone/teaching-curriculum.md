# Phase 2c — Capstone Project
## PORA Academy Cohort 7

**Duration:** 4 weeks (8 facilitated sessions: Wed + Thu × 4 weeks)
**Dataset:** Olist Brazilian E-Commerce (same as Phase 2a Python + Phase 2b SQL)
**Format:** All groups share the same facilitated sessions for core skills; group-specific analytical work happens in breakouts and between sessions
**Groups:** Same 4 project teams of 30 from Phase 1 (3 sub-groups of 10 each)
**Deliverable:** Deployed Streamlit dashboard (Streamlit Community Cloud) + 10-minute group presentation

> **Curriculum principle:** Students arrive with 16 weeks of Python (Phase 2a) and SQL (Phase 2b) on this exact dataset. Phase 2c consolidates those skills into a single production-grade deliverable. The technical bar is intentionally higher: the dashboard must be deployed, not just demonstrated in Colab.

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
| Total GMV (delivered orders) | **R$15,843,553.24** |
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

---

## Technical Stack

| Component | Tool |
|---|---|
| Language | Python 3 |
| Data loading | pandas |
| Database | SQLite in-memory (`sqlite3`) — same as Phase 2b |
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
    "geolocation":   "olist_geolocation_dataset.csv",
}

conn = sqlite3.connect(":memory:")
for name, file in tables.items():
    pd.read_csv(os.path.join(DATA_DIR, file)).to_sql(name, conn, if_exists="replace", index=False)
```

For Streamlit Community Cloud deployment, CSVs are committed to the GitHub repo (or loaded from a public URL). The `conn` is wrapped in `@st.cache_data` to avoid reloading on every interaction.

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
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Olist Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect(":memory:")
    # ... load tables as shown above ...
    return conn

conn = load_data()

st.title("Olist Dashboard — [Group Name]")
st.markdown("Data: Brazilian E-Commerce (Olist, 2016–2018)")

# --- KPI placeholders ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", "99,441")
col2.metric("Total GMV", "R$15.8M")
col3.metric("Avg Review Score", "4.09")
```

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

**Chart pattern:**

```python
import matplotlib.pyplot as plt

# SQL → DataFrame
df = pd.read_sql("""
    SELECT strftime('%Y-%m', order_purchase_timestamp) as month,
           COUNT(*) as orders
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY month
    ORDER BY month
""", conn)

# DataFrame → Chart
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["month"], df["orders"], marker="o")
ax.set_title("Monthly Orders (Delivered)")
ax.set_xlabel("Month")
ax.set_ylabel("Orders")
plt.xticks(rotation=45)
st.pyplot(fig)
```

**Assignment (between Wed and Thu):**
Build charts 2 and 3 from their wireframe. Must run without errors before Thursday.

---

#### Thursday (Group Breakouts): Complete Chart Set

**Objective:** All 4 charts implemented; layout matches wireframe; app runs end-to-end.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:30 | Groups integrate charts 2 and 3 reviewed by instructor |
| 0:30–1:15 | Groups build chart 4 (group-specific — see briefs below) |
| 1:15–1:45 | Cross-group peer review: each group demos to one other group |
| 1:45–2:00 | Feedback collected; instructor sets quality bar for Week 3 |

**Assignment (Week 2 → Week 3):**
Polish: consistent colour scheme, chart titles, axis labels, formatted numbers (e.g. `f"R${value:,.2f}"`). Write a one-paragraph "key finding" for each chart.

---

### Week 3 — Interactivity, Polish & Peer Review

#### Wednesday (All Groups): Sidebar Filters + Caching

**Objective:** Connect sidebar widgets to all charts so filtering by year or state updates the entire dashboard.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–0:20 | Instructor demo: `st.sidebar.selectbox` → SQL WHERE clause → chart update |
| 0:20–0:50 | Groups add year filter (2016, 2017, 2018, "All") connected to all charts |
| 0:50–1:20 | Add state filter (top 5 states + "All") — requires `st.sidebar.multiselect` |
| 1:20–1:45 | `@st.cache_data` strategy: cache the raw tables, not the filtered results |
| 1:45–2:00 | Debug session — common issue: cache not invalidating on filter change |

**Filter pattern:**

```python
# Sidebar
year_options = ["All", "2016", "2017", "2018"]
selected_year = st.sidebar.selectbox("Year", year_options)

# Build WHERE clause dynamically
year_filter = "" if selected_year == "All" else f"AND strftime('%Y', order_purchase_timestamp) = '{selected_year}'"

# Use in query
df = pd.read_sql(f"""
    SELECT strftime('%Y-%m', order_purchase_timestamp) as month,
           COUNT(*) as orders
    FROM orders
    WHERE order_status = 'delivered'
    {year_filter}
    GROUP BY month ORDER BY month
""", conn)
```

**Assignment (between Wed and Thu):**
Add a `st.metric` row that recalculates when filters change (not hardcoded). Implement `st.divider()` and section headers with `st.subheader()`.

---

#### Thursday (Group Breakouts): Group-Specific Deep Dive + Insight Writing

**Objective:** Each group completes their group-specific advanced feature (see briefs). Draft 3 business insights for the presentation.

**Session Plan:**

| Time | Activity |
|---|---|
| 0:00–1:00 | Groups implement their advanced feature (see group briefs) |
| 1:00–1:30 | Write 3 business insights: each backed by a chart/KPI in the dashboard |
| 1:30–2:00 | Full app demo + instructor sign-off — app must run from top to bottom |

**Assignment (Week 3 → Week 4):**
GitHub repository setup: create repo, commit `app.py`, `requirements.txt`, data files (or data loading from URL). Test `streamlit run app.py` locally or confirm pyngrok tunnel works cleanly.

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

**Data note for deployment:** Olist CSVs are committed to the GitHub repo in a `data/` folder. In `app.py`, the data path switches from Google Drive to relative: `DATA_DIR = "data/"`.

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
| Avg delivery days (on-time) | Run & verify |
| Avg delivery days (late) | Run & verify |

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
    CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date
         THEN 'On Time' ELSE 'Late' END AS delivery_status,
    AVG(r.review_score) AS avg_score,
    COUNT(*) AS orders
FROM orders o
JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status
```

**Expected finding:** Late deliveries score approximately 1.5–2 stars lower on average. Groups must state the exact verified values.

---

### Group 2 — Product Category Performance Dashboard

**Olist focus:** Category revenue rankings, product-level GMV analysis

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total GMV | **R$15,843,553.24** |
| Top category (revenue) | **health_beauty — R$1,258,681.34** |
| Total product categories | **74** (after translation join) |
| Avg item price | Run & verify |

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
Category market share chart. Show what % of total GMV each of the top 10 categories represents. Add a note on whether any single category dominates (health_beauty = ~8% of GMV).

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
Pareto analysis. Build a chart showing that ~1% of sellers (Top Tier + High Performer = 40 sellers out of 3,095) generate a disproportionate share of GMV. Calculate and display the exact percentage on the dashboard.

---

### Group 4 — Revenue & Growth Dashboard

**Olist focus:** GMV trends, state-level revenue, payment behaviour

**Verified KPIs:**

| KPI | Verified Value |
|---|---|
| Total GMV | **R$15,843,553.24** |
| Peak month | **Nov 2017 — R$1,230,815** (approx) |
| Top state by GMV | **SP — R$5,770,266.19** |
| 2nd state | **RJ — R$2,055,690.45** |
| 3rd state | **MG — R$1,819,277.61** |
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
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month
```

**Advanced feature (Week 3 Thursday):**
Payment instalment analysis. Olist payment data includes instalment counts. Show the distribution of instalments (1 instalment, 2, 3, … 12+) and calculate: do customers paying in more instalments spend more per order? This connects to creditworthiness and marketing strategy.

```sql
SELECT payment_installments,
       COUNT(*) AS transactions,
       AVG(payment_value) AS avg_value
FROM payments
WHERE payment_type = 'credit_card'
GROUP BY payment_installments
ORDER BY payment_installments
```

---

## Deliverables and Assessment

### Dashboard (60%)

| Criterion | Marks |
|---|---|
| App is deployed and accessible via public URL | 10 |
| 3 KPI metrics update correctly when filters change | 10 |
| 4 charts present, labelled, and readable | 15 |
| SQL queries are correct — values match verified benchmarks | 15 |
| Code quality: `@st.cache_data` used; no hardcoded values | 10 |

### Presentation (40%)

| Criterion | Marks |
|---|---|
| Live demo of deployed app (not screenshots) | 10 |
| 3 business insights backed by specific numbers | 15 |
| Awareness of data limitations | 5 |
| Delivery and clarity | 10 |

---

## Common Technical Issues and Solutions

| Issue | Solution |
|---|---|
| Colab session times out, SQLite connection lost | Wrap `conn = sqlite3.connect(":memory:")` inside `@st.cache_data` — Streamlit recreates it on next run |
| `st.cache_data` doesn't work with SQLite connection objects | Cache the DataFrames, not the connection: `@st.cache_data def load_orders(): return pd.read_sql(...)` |
| Filter changes don't update charts | Ensure queries use the filter variable, not a hardcoded value |
| Deployment fails: `ModuleNotFoundError` | Check `requirements.txt` — all imports must be listed |
| CSV not found on Streamlit Cloud | Confirm file is committed to the GitHub repo (not `.gitignored`) |
| f-string formatting with R$ | Use `f"R${value:,.2f}"` — comma separator, 2 decimal places |

---

## Instructor Notes

- **Weeks 1–2 are the hardest.** Students will struggle to connect SQL → pandas → Streamlit in one flow. The skeleton in Week 1 Wednesday is critical — do not skip it.
- **Deployment day (Week 4 Wednesday) almost always has problems.** Common: students forget to push data files to GitHub, or `requirements.txt` is missing a package. Budget 45–60 minutes for pure troubleshooting.
- **Group 2 note:** The `product_category_name_translation` join drops ~1,400 products with null category names. Groups must decide whether to exclude these or label them "Unknown" — either is acceptable but must be stated.
- **Group 4 note:** 2016 data covers only September–December (partial year). Groups must flag this when comparing across years.
- **Group 3 note:** The Pareto finding (Top 40 sellers = significant share of GMV) is the headline insight. If a group quantifies this incorrectly, the presentation narrative falls apart — verify their number before sign-off.
- **All groups:** The Nov 2017 spike in orders is likely related to Black Friday. Groups that identify and name this in their presentation should receive bonus recognition for contextual analysis.
