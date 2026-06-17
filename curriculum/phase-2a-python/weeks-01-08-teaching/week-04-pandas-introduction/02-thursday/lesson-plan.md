# Week 4 — Pandas Introduction: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week04_thu_demo.ipynb`
- [ ] Student exercise link ready to share: `week04_thu_exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Sort DataFrames with `.sort_values()`
2. Add calculated columns
3. Use `.nlargest()` / `.nsmallest()`
4. Chain pandas operations

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:30 | Load Items & Calculated Columns | `.shape`, `.describe()`, `total_cost`, `price_tier` |
| 0:30–1:00 | Sorting & nlargest | `.sort_values()`, `.nlargest()`, `.nsmallest()`, groupby revenue |
| 1:00–1:40 | Group Exercise | 6 tasks on `olist_order_items_dataset.csv` |
| 1:40–1:50 | Assignment briefing | Walk through Week 4 assignment requirements |
| 1:50–2:00 | Q&A | Open questions, preview Week 5 |

---

## Key Concepts

### Loading Items & Calculated Columns
Load the order items dataset, use `.describe()` for numeric stats, add calculated columns with arithmetic

**Expected outputs:**
- `items.shape` → `(112650, 7)`
- `price` mean=120.65, max=6,735.00, min=0.85
- `freight_value` mean=19.99, max=409.68
- `total_cost` mean=140.64, sum=R$15,843,553.24
- `price_tier`: Economy=73,397 | Standard=30,760 | Premium=8,493

---

### Sorting & nlargest/nsmallest
Sort with `.sort_values()`; use `.nlargest()` and `.nsmallest()` for top-N analysis; `.groupby()` for aggregation

**Expected outputs:**
- Most expensive item: R$6,735.00
- Top seller by revenue: R$229,472.63
- 2nd seller by revenue: R$222,776.05

**Common mistake:** `.groupby()` without an aggregation (`.sum()`, `.mean()`, etc.) returns a GroupBy object, not numbers; forgetting `ascending=False` when sorting for highest-first

---

## Group Exercise

Using `olist_order_items_dataset.csv` (already loaded as `items`):

1. Total revenue (sum of `price` column). Expected: **R$13,591,643.70**
2. Total freight collected. Expected: **R$2,251,909.54**
3. Add a `revenue_share` column = `price / total_revenue * 100` (each item's % of total)
4. How many items are in the "Premium" tier (`price >= R$500`)? Expected: **8,493**
5. Which order has the most items? Hint: `groupby order_id`, count `order_item_id`, `nlargest(1)`. Expected: **max = 21**
6. Average freight as % of price? Expected: **~20%**

All expected outputs verified against the actual Olist dataset.

---

## Weekly Assignment

Submit `week4_assignment.ipynb` before the next session:

1. Load both `olist_orders_dataset.csv` and `olist_order_items_dataset.csv`. Print `.shape` and `.isnull().sum()` for each.

2. From the orders DataFrame:
   - How many unique order statuses exist? *(Expected: 8)*
   - What % of orders are NOT yet delivered (status ≠ 'delivered')? *(Expected: 3.0%)*
   - Filter to only 'canceled' or 'unavailable' orders. How many rows? *(Expected: 1,234)*

3. From the items DataFrame:
   - Add a `total_cost` column (price + freight_value)
   - Add a `price_tier` column: Premium (≥500), Standard (≥100), Economy (<100)
   - Count each tier *(Expected: Economy=73,397 / Standard=30,760 / Premium=8,493)*

4. Find the top 5 sellers by total revenue (sum of price, grouped by seller_id).
   Revenue of the #1 seller? *(Expected: R$229,472.63)*
