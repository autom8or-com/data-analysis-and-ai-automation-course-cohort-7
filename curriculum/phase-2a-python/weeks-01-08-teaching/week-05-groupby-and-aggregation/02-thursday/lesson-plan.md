# Week 5 — GroupBy & Aggregation: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week05_thu_demo.ipynb`
- [ ] Student exercise link ready to share: `week05_thu_exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Parse datetime columns with pd.to_datetime()
2. Extract year, month, day of week from datetime
3. GroupBy with datetime components
4. GroupBy with two keys (cross-tabulation)

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, load data |
| 0:10–0:40 | Datetime Parsing | Convert string → datetime, extract .dt components |
| 0:40–1:10 | Multi-Key GroupBy | Cross-tabulation with .unstack(), day-of-week analysis |
| 1:10–1:15 | Mini Challenge | 2018 truncated months puzzle |
| 1:15–1:55 | Group Exercise | 4 tasks incl. DeepSeek validation |
| 1:55–2:00 | Debrief & assignment intro | Preview Week 6: Data Cleaning |

---

## Key Concepts

### Datetime Parsing
Pandas loads all date columns as `object` (string). Use `pd.to_datetime()` to convert, then the `.dt` accessor to extract components.

**Expected outputs:**
- `orders['order_purchase_timestamp'].dtype` before → `object`
- After `pd.to_datetime()` → `datetime64[ns]`
- Orders by year: 2016=329 | 2017=45,101 | 2018=54,011
- Monthly 2017: November = 7,544 orders (Black Friday peak!)
- Monthly 2017 full: Jan=800, Feb=1,780, Mar=2,682, Apr=2,404, May=3,700, Jun=3,245, Jul=4,026, Aug=4,331, Sep=4,285, Oct=4,631, Nov=7,544, Dec=5,673

**Common mistake to watch for:** trying to groupby the raw string timestamp column without parsing first. Always parse first, then extract components.

---

### Multi-Key GroupBy
Group by two columns simultaneously to create a cross-tabulation. Use `.unstack()` to pivot the inner key into columns for a cleaner view.

**Expected outputs:**
- State × year cross-tab shows SP/RJ/MG growth from 2016 → 2018
- Day-of-week counts must sum to 99,441

---

## Group Exercise

**Tasks (40 min):**

1. Parse order_purchase_timestamp. Verify year distribution: 2016=329, 2017=45,101, 2018=54,011
2. Monthly order count for 2017. Which month had most? Expected: November (7,544) — Black Friday!
3. Average order price per month for 2017 (merge orders + items, groupby month, mean of price)
4. DeepSeek task: ask DeepSeek to write code showing the number of orders per day_of_week. Which day sees the most orders? Validate the total sums to 99,441.

All expected outputs verified against the actual Olist dataset.

---

## Weekly Assignment

Submit `week5_assignment.ipynb`:

1. Load `olist_orders_dataset.csv`. Parse `order_purchase_timestamp` to datetime. Add columns: `year`, `month`, `day_of_week`.

2. Monthly order trend for **2018** (use only 2018 data):
   - Note: Sep 2018 has only 16 orders, Oct 2018 has 4. Why? *(The dataset ends Oct 17, 2018 — incomplete months)*

3. Load `olist_order_items_dataset.csv`. Merge with orders. Build a grouped table:
   - Rows: customer_state (from customers dataset — requires another merge)
   - Values: total revenue, avg price, order count
   - Sort by total revenue descending. Print top 5.
   - Verify SP = R$5,202,955.05

4. **DeepSeek challenge:** Ask DeepSeek to group orders by `order_status` and `year` (multi-key groupby) and show the count for each combination. Paste the DeepSeek prompt you used, the code it returned, and your output. Does delivered + 2018 = 54,011? *(Note: actual answer requires counting only delivered in 2018 — explore this)*
