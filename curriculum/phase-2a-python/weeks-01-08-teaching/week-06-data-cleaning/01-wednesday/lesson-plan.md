# Week 6 — Data Cleaning: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-06-wed-demo.ipynb`
- [ ] Student exercise link ready to share: `week-06-wed-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek tab open at chat.deepseek.com

---

## Learning Objectives

By the end of this session, students will be able to:
1. Identify and count null values
2. Use fillna(), dropna(), and conditional replacement
3. Convert data types correctly
4. Recognise the typo in the products dataset

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:05 | Setup & recap | Students open Colab, load data (products + orders) |
| 0:05–0:35 | Products Dataset — A Real Cleaning Challenge | Demo null inspection + rename columns |
| 0:35–1:10 | fillna & dropna | Demo three strategies, discuss when to use each |
| 1:10–1:40 | Datetime Conversion & Delivery Time Calculation | Demo pd.to_datetime, errors='coerce', delivery_days |
| 1:40–2:00 | Group Exercise | 4 tasks; see group exercise section below |

---

## Key Concepts

### Products Dataset — A Real Cleaning Challenge
Load olist_products_dataset.csv, inspect shape and null counts, and fix column name typos.

Expected outputs:
- Shape: `(32951, 9)`
- `product_category_name` nulls: `610`
- `product_name_lenght` nulls: `610` (note the typo — this is intentional in the source data)
- After rename: column list includes `product_name_length` and `product_description_length`

Common mistake to watch for:
- Students trying to use `df.column_name_lenght` after rename (old name no longer exists)

---

### fillna & dropna
Three strategies for handling nulls: fill with a value, drop rows with nulls in specific columns, or drop rows with any null.

Expected outputs:
- After `fillna('unknown')`: 0 nulls remain, 610 rows contain 'unknown'
- After `dropna(subset=['product_category_name'])`: shape `(32341, 9)` — 610 rows removed

Common mistake to watch for:
- Using `== None` instead of `.isna()` to check for nulls (always returns False in pandas)

---

### Datetime Conversion & Delivery Time Calculation
Convert string columns to datetime using pd.to_datetime with errors='coerce', then compute delivery duration.

Expected outputs:
- After conversion: all 5 date columns have dtype `datetime64[ns]`
- Delivered order delivery stats: count 96470, mean 12.1 days, median 10.0 days, max 209 days

Common mistake to watch for:
- Forgetting `errors='coerce'` — the notebook will crash on unparseable values without it

---

## Group Exercise

Tasks:
1. Load products. Print null counts. Fix the column name typos. Verify: renamed columns show 'product_name_length' (not 'lenght')
2. Fill null product_category_name with 'unknown'. Verify: 0 nulls remain, 610 rows have value 'unknown'
3. Load orders. Convert all 5 date columns using pd.to_datetime(errors='coerce'). Calculate delivery_days. Verify: mean ≈ 12.1 days
4. What % of orders have a delivery_days value > 30 (slow)? Hint: `delivered['delivery_days'].gt(30).mean() * 100`

**Expected outputs:**
- Task 1: `product_name_length` in columns list
- Task 2: 0 nulls, 610 'unknown' rows
- Task 3: mean ≈ 12.1
- Task 4: a percentage between 5–15%
