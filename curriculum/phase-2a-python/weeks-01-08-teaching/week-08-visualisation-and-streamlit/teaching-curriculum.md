## WEEK 8 — Visualisation & Putting It Together
*(DeepSeek assisted)*

### Wednesday: matplotlib & seaborn Basics

**Learning objectives:**
- Create bar charts, line charts, and histograms with matplotlib
- Format charts (title, labels, figsize, colours)
- Use seaborn for cleaner charts
- Save charts to file

> **Note:** Every chart built today will be embedded inside a Streamlit dashboard on Thursday. matplotlib figures are passed directly to `st.pyplot()` — so the skills are directly connected.

**Session outline (2 hours)**

**Part 1 — matplotlib Foundations (30 min)**

```python
import pandas as pd
import matplotlib.pyplot as plt

orders = pd.read_csv('olist_orders_dataset.csv')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')

# Monthly orders 2017 (verified)
orders_2017 = orders[orders['order_purchase_timestamp'].dt.year == 2017]
monthly = orders_2017.groupby('month')['order_id'].count()

# Line chart
plt.figure(figsize=(12, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2, color='steelblue')
plt.title('Monthly Orders — Olist 2017', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# November 2017 spike to 7,544 should be visually prominent (Black Friday)

# Bar chart — order status
status = orders['order_status'].value_counts().head(5)
plt.figure(figsize=(8, 4))
plt.bar(status.index, status.values, color=['#2ecc71','#3498db','#e74c3c','#f39c12','#9b59b6'])
plt.title('Order Status Distribution')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
```

**Part 2 — seaborn (30 min)**

```python
import seaborn as sns

# Review score distribution
reviews = pd.read_csv('olist_order_reviews_dataset.csv')

plt.figure(figsize=(8, 4))
sns.countplot(data=reviews, x='review_score', palette='RdYlGn')
plt.title('Review Score Distribution — Olist')
plt.xlabel('Review Score')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
# Expected visual: 5-star dominates (57,328), 1-star is second (11,424)

# Payment type pie chart
payments = pd.read_csv('olist_order_payments_dataset.csv')
pay_counts = payments['payment_type'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(pay_counts.values, labels=pay_counts.index, autopct='%1.1f%%',
        colors=['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6'])
plt.title('Payment Method Distribution')
plt.show()
# credit_card: 73.9%, boleto: 19.0%, voucher: 5.6%, debit_card: 1.5%
```

**Part 3 — Group Exercise (40 min)**

```python
# Each group builds 3 charts using verified data:

# Chart 1: Monthly order volume for 2017 (line chart)
# Peak should show: November 2017 = 7,544 orders

# Chart 2: Top 10 states by total orders (horizontal bar chart)
# SP should be far ahead at 41,746

# Chart 3: Review score distribution (bar chart)
# Scores 1-5, count for each
# Expected: [11424, 3151, 8179, 19142, 57328]
```

---

### Thursday: Introduction to Streamlit

**Learning objectives:**
- Understand what Streamlit is and why it matters for data analysts
- Build a working multi-page dashboard using Streamlit
- Use core Streamlit components: `st.title`, `st.metric`, `st.selectbox`, `st.columns`, `st.pyplot`, `st.dataframe`, `@st.cache_data`
- Run a Streamlit app from Google Colab using pyngrok
- Know the Streamlit Community Cloud deployment workflow (used in Phase 2c Capstone)

> **Why Streamlit now:** The Phase 2c Capstone project requires each group to build and deploy a Streamlit dashboard combining Python + SQL. This session is your introduction. By end of Capstone, you will build the full version.

---

**Session outline (2 hours)**

**Part 1 — What is Streamlit? (20 min)**

Streamlit turns a Python script into an interactive web app. You do not need to know HTML, CSS, or JavaScript. You write Python; Streamlit handles the browser.

Core concept: every time a user interacts with a widget (selectbox, slider, button), the entire Python script re-runs from top to bottom. This is the Streamlit execution model — understand it before writing your first app.

**Install in Colab:**
```python
!pip install streamlit pyngrok -q
```

**How Streamlit apps work in Colab:**
Streamlit apps cannot be viewed directly inside a Colab notebook. You need to:
1. Write the app code to a `.py` file using `%%writefile`
2. Start the Streamlit server in the background
3. Use `pyngrok` to create a public URL that tunnels to the running server

```python
# Step 1: Write app to file
%%writefile app.py
import streamlit as st
st.title("Hello from Streamlit!")
st.write("This is my first app.")
```

```python
# Step 2: Start Streamlit in background + create tunnel
import subprocess
import time
from pyngrok import ngrok

# You need a free account at ngrok.com to get an auth token
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Start streamlit in background
process = subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])
time.sleep(3)

# Create public URL
public_url = ngrok.connect(8501)
print(f"App is live at: {public_url}")
```

> **Instructor note:** Have students create a free ngrok account before this session. The auth token setup takes 2 minutes. Alternatively, students can run the app locally on their laptop if Python is installed: `streamlit run app.py` opens it at `http://localhost:8501` automatically.

---

**Part 2 — Core Components (40 min)**

Build each component live, run and observe:

```python
%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_DIR = "/content/drive/MyDrive/cohort7/datasets/olist"

st.set_page_config(page_title="Olist Dashboard", layout="wide")

# --- Title and description ---
st.title("Olist E-Commerce Dashboard")
st.markdown("**Brazilian marketplace orders — 2016 to 2018**")
st.divider()

# --- @st.cache_data: load once, reuse ---
# Without caching, the CSV loads every time a widget changes (slow).
# With @st.cache_data, it loads once and stays in memory.
@st.cache_data
def load_data():
    orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))
    payments = pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders["year"] = orders["order_purchase_timestamp"].dt.year
    orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return orders, customers, payments

orders, customers, payments = load_data()

# --- Sidebar: selectbox filter ---
st.sidebar.header("Filters")
year_options = sorted(orders["year"].dropna().unique().astype(int).tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options, index=1)

# Filter data based on selection
filtered = orders[orders["year"] == selected_year]

# --- KPI Row: st.metric in st.columns ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{len(filtered):,}")
col2.metric("Delivered", f"{(filtered['order_status'] == 'delivered').sum():,}")
col3.metric("Canceled", f"{(filtered['order_status'] == 'canceled').sum():,}")
col4.metric("Delivered %", f"{(filtered['order_status'] == 'delivered').mean()*100:.1f}%")

# --- Chart 1: Monthly orders (st.pyplot) ---
st.subheader(f"Monthly Orders — {selected_year}")

monthly = filtered.groupby("month")["order_id"].count().reset_index()
monthly.columns = ["month", "orders"]

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly["month"], monthly["orders"], marker="o", color="steelblue", linewidth=2)
ax1.set_xlabel("Month")
ax1.set_ylabel("Orders")
ax1.tick_params(axis="x", rotation=45)
plt.tight_layout()
st.pyplot(fig1)
plt.close()

# --- Two-column layout: state chart + payment chart ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 States by Orders")
    merged = filtered.merge(customers[["customer_id", "customer_state"]], on="customer_id")
    state_counts = merged["customer_state"].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.barh(state_counts.index[::-1], state_counts.values[::-1], color="coral")
    ax2.set_xlabel("Orders")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

with col_right:
    st.subheader("Payment Method Breakdown")
    pay_counts = payments["payment_type"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
            colors=["#3498db","#e74c3c","#2ecc71","#f39c12","#9b59b6"])
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# --- Raw data toggle: st.dataframe ---
if st.checkbox("Show raw data sample"):
    st.dataframe(filtered.head(20))
```

**Verify these KPIs when selecting 2017:**
| KPI | Expected value |
|---|---|
| Total Orders | 45,101 |
| Delivered | 43,428 |
| Canceled | 265 |
| Delivered % | 96.3% |

**Verify when selecting 2018:**
| KPI | Expected value |
|---|---|
| Total Orders | 54,011 |
| Delivered | 52,783 |
| Canceled | 334 |
| Delivered % | 97.7% |

---

**Part 3 — Group Exercise (40 min)**

Each group extends the app above by adding one new section. Assign sections:

- **Group A:** Add a delivery time histogram. Load `order_delivered_customer_date`, compute `delivery_days`, plot a histogram. Expected: mean = 12.1 days, median = 10.0 days.

- **Group B:** Add a review score bar chart. Load `olist_order_reviews_dataset.csv`, plot `review_score` counts. Expected: 5-star = 57,328, 1-star = 11,424.

- **Group C:** Add a top-10 revenue categories chart. Requires merging order_items + products + translation. Expected: health_beauty = R$1,258,681.34.

- **Group D (challenge):** Add a `st.selectbox` for state selection. Filter all charts by the selected state. Verify SP total orders (2017) = 17,760.

---

**Part 4 — Deployment to Streamlit Community Cloud (20 min — instructor demo)**

> This is what you will use for Phase 2c Capstone deployment. Watch and follow along.

1. Push `app.py` to a public GitHub repository
2. Go to `share.streamlit.io` → Sign in with GitHub
3. Click **New app** → Select repo, branch, and file
4. Click **Deploy** — the app is live at a public URL in ~2 minutes (free)

The Phase 2c Capstone will require each group to deploy their Streamlit dashboard this way. No ngrok needed — the production version runs on Streamlit Community Cloud.

---

**Weekly Assignment 8 (Phase 2a Final — Streamlit App):**

This is the final Python assignment. Build a Streamlit app (`olist_app.py`) that:

1. **Loads and caches** orders, customers, payments, and order_reviews using `@st.cache_data`
2. **Has a sidebar** with a year selector (`st.selectbox`) — 2017 or 2018
3. **Shows 4 KPI metrics** in a row using `st.columns` and `st.metric`:
   - Total Orders, Delivered %, Avg Payment Value, Most Common Payment Type
4. **Shows 3 charts** using `st.pyplot`:
   - Monthly orders line chart (for selected year)
   - Review score bar chart (all years — not filtered)
   - Top 10 states by orders horizontal bar chart (filtered by year)
5. **Has a data table toggle** using `st.checkbox("Show raw orders sample")`

**Verified outputs that must appear in the app:**

| Check | Expected |
|---|---|
| 2017 total orders | 45,101 |
| 2018 total orders | 54,011 |
| 2017 delivered % | 96.3% |
| 2017 peak month | November 2017 = 7,544 orders |
| Review score 5 count | 57,328 |
| Review score 1 count | 11,424 |
| Overall avg payment | R$154.10 |
| Top state (2017) | SP = 17,760 orders |

---
