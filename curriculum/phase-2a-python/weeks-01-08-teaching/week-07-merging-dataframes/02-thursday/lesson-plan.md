# Week 7 — Merging DataFrames: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-07-thu-demo.ipynb`
- [ ] Student exercise link ready to share: `week-07-thu-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek access confirmed for all students (Week 4+ requirement)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Chain multiple merges cleanly
2. Use `pd.concat()` to stack DataFrames
3. Handle mismatched columns after concat
4. Build a complete multi-table analysis

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:40 | Full Pipeline | Chain orders → customers → items → products → translation, then merge in reviews for category analysis |
| 0:40–1:05 | Payment Analysis | Groupby `payment_type`: count, total value, avg installments, pct share |
| 1:05–1:45 | Group Exercise | Complete multi-table analysis by state, plus DeepSeek task |
| 1:45–2:00 | Debrief & assignment brief | Share expected answers, introduce Weekly Assignment 7 |

---

## Key Concepts

### Full pipeline — chained merges
Chain merges of orders, customers, items, products, and translation into one full analysis table, then bring in reviews for category-level analysis.

Expected outputs:
- `full.shape` → (112650, 20)

Common mistake to watch for: chaining merges with mismatched key names (`_x`/`_y` suffixes appear silently) — always check `.columns` after each merge step to confirm nothing collided.

### Payment analysis
Group payments by `payment_type` to see count, total value, average installments, and percentage share.

Expected outputs:
- credit_card: 76,795 orders, ~R$12.3M, 73.9%, avg 3.0 installments
- boleto: 19,784 orders, 19.0%
- voucher: 5,775 orders, 5.6%
- debit_card: 1,529 orders, 1.5%

Common mistake to watch for: forgetting `.reset_index()` after a `groupby().agg()` chain, which leaves `payment_type` as an index rather than a column — breaks later merges or plotting.

---

## Group Exercise

Build the complete multi-table analysis:
1. Merge: orders + customers + items + products + translation + reviews
2. GroupBy `customer_state`, calculate:
   - `total_revenue` (sum of price)
   - `avg_review_score` (mean of review_score)
   - `order_count` (nunique of order_id)
3. Which state has the highest avg review score among those with >500 orders?
4. **DeepSeek task**: Ask DeepSeek to add the payments table to the analysis and show avg `payment_installments` by state. Validate: Brazil avg installments = 2.85

**Expected outputs**: Brazil avg payment installments = 2.85 (validation check for the DeepSeek output).

---

## Weekly Assignment

**Weekly Assignment 7:**

Submit `week7_assignment.ipynb`:

1. Build the full merged table (orders + customers + items + products + translation).
   Verify final shape = **(112650, 20)**

2. From the full merged table, answer:
   - Which state has the highest average price per item? *(Groupby state, mean of price)*
   - What is the total revenue from "health_beauty" category? *(Expected: R$1,258,681.34)*

3. Merge in reviews. Find the 5 **worst-rated** product categories (min 100 orders).
   *(Expected bottom 5 include security_and_services at 2.50 avg)*

4. **DeepSeek challenge:** Ask DeepSeek to merge orders + payments and calculate total payment value per order status. What is the total payment value for 'delivered' orders? Paste your prompt and verify the output is internally consistent.

---
