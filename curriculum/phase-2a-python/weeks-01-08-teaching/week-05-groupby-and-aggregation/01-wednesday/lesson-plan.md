# Week 5 — GroupBy & Aggregation: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week05_wed_demo.ipynb`
- [ ] Student exercise link ready to share: `week05_wed_exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Use .groupby() with single and multiple keys
2. Apply aggregation functions: sum, mean, count, nunique, min, max
3. Use .agg() for multiple aggregations at once
4. Reset index after groupby

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, load data (orders, customers, items) |
| 0:10–0:45 | Single-Key GroupBy | orders by status, orders/revenue by state |
| 0:45–1:20 | .agg() for Multiple Metrics | seller stats, order-level summary |
| 1:20–2:00 | Group Exercise | 4 tasks incl. DeepSeek validation |

---

## Key Concepts

### Single-Key GroupBy
Use `.groupby('column')['col'].agg()` to count, sum or average rows sharing the same value in one column. Think of it as Excel pivot tables but in one line of code.

**Expected outputs:**
- `orders.groupby('order_status')['order_id'].count()` → delivered: 96,478 at top
- Orders per state (after merging with customers): SP=41,746 | RJ=12,852 | MG=11,635 | RS=5,466 | PR=5,045
- Revenue per state: SP=R$5,202,955.05

**Common mistake to watch for:** forgetting `.reset_index()` after groupby — the result stays as a Series with the groupby key as index rather than a clean DataFrame.

---

### .agg() for Multiple Metrics
Use named aggregations with `.agg()` to compute several metrics simultaneously on grouped data. More efficient and readable than chaining multiple groupby calls.

**Expected outputs:**
- Seller stats: top seller revenue = R$229,472.63
- Order summary: orders with >1 item = 9,803 | max items in one order = 21 | avg = 1.14

**Common mistake to watch for:** confusing `('column', 'function')` tuple order in named aggregations.

---

## Group Exercise

**Tasks (40 min):**

1. Using orders + customers merged: how many orders came from each state? Print top 5. SP Expected: 41,746
2. Using items: total revenue + avg price by seller (top 5 by revenue). Top seller Expected: R$229,472.63
3. Build order_summary (group by order_id): total_price, total_freight, item_count. Verify: orders with >1 item=9,803, max items=21.
4. DeepSeek task: ask DeepSeek to write code grouping orders by order_status with count, %, avg approved_at delay. Validate counts against known values.

All expected outputs verified against the actual Olist dataset.
