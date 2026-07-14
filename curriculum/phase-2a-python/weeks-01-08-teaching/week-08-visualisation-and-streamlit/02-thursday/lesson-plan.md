# Week 8 — Visualisation & Putting It Together: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-08-thu-demo.ipynb`
- [ ] Student exercise link ready to share: `week-08-thu-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek access confirmed for all students (Week 4+ requirement)
- [ ] Students have created a free ngrok.com account and grabbed their auth token in advance (setup takes ~2 minutes)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Understand what Streamlit is and why it matters for data analysts
2. Build a working multi-page dashboard using Streamlit
3. Use core Streamlit components: `st.title`, `st.metric`, `st.selectbox`, `st.columns`, `st.pyplot`, `st.dataframe`, `@st.cache_data`
4. Run a Streamlit app from Google Colab using pyngrok
5. Know the Streamlit Community Cloud deployment workflow (used in Phase 2c Capstone)

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:20 | What is Streamlit? | Execution model: every widget interaction re-runs the whole script top to bottom |
| 0:20–1:00 | Core Components | Build the full dashboard live: `@st.cache_data`, sidebar selectbox, KPI row, `st.pyplot` charts, two-column layout, `st.checkbox` toggle |
| 1:00–1:40 | Group Exercise | Groups A–D each extend the dashboard with one new section |
| 1:40–2:00 | Deployment Demo | Instructor walkthrough of Streamlit Community Cloud deploy (used again in Phase 2c Capstone) |

---

## Key Concepts

### What is Streamlit?
Streamlit turns a plain Python script into an interactive web app with no HTML/CSS/JS required. The core mental model students must internalize: every time a user touches a widget, the *entire* script re-runs from top to bottom — this explains why `@st.cache_data` matters.

### Running Streamlit in Colab via pyngrok
Colab cannot render a Streamlit app directly. The pattern: write the app to `app.py` with `%%writefile`, launch it in the background with `subprocess.Popen`, then tunnel it publicly with `pyngrok`.

Common mistake to watch for: students forget `time.sleep(3)` after starting the server and get a connection error from `ngrok.connect()` because the server hasn't finished booting yet.

### Core Components — Full Dashboard
The full dashboard combines `@st.cache_data` (load once, reuse), `st.sidebar.selectbox` (year filter), `st.columns` + `st.metric` (KPI row), `st.pyplot` (embedded matplotlib figures), a two-column chart layout, and `st.checkbox` + `st.dataframe` (raw data toggle).

Expected outputs (verify when selecting each year):
- 2017 — Total Orders: 45,101 | Delivered: 43,428 | Canceled: 265 | Delivered %: 96.3%
- 2018 — Total Orders: 54,011 | Delivered: 52,783 | Canceled: 334 | Delivered %: 97.7%

Common mistake to watch for: forgetting `plt.close()` after `st.pyplot(fig)` — figures accumulate in memory across re-runs and slow the app down over a session.

---

## Group Exercise

Each group extends the dashboard above by adding one new section:
- **Group A**: Delivery time histogram — expected mean = 12.1 days, median = 10.0 days
- **Group B**: Review score bar chart — expected 5-star = 57,328, 1-star = 11,424
- **Group C**: Top-10 revenue categories chart — expected top category health_beauty = R$1,258,681.34
- **Group D (challenge)**: `st.selectbox` for state, filtering all charts — verify SP total orders (2017) = 17,760

**Expected outputs**: delivery days mean 12.1 / median 10.0; review counts 5-star 57,328 / 1-star 11,424; top revenue category health_beauty R$1,258,681.34; SP 2017 orders = 17,760.

---

## Weekly Assignment

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
