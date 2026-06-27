# Week 4 — Pandas Introduction: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week04_wed_demo.ipynb`
- [ ] Student exercise link ready to share: `week04_wed_exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Import pandas and load a CSV into a DataFrame
2. Use `.shape`, `.columns`, `.dtypes`, `.head()`, `.tail()`, `.info()`, `.describe()`
3. Select columns and filter rows
4. Use `.value_counts()` and `.nunique()`

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | DeepSeek transition briefing | Introduce AI tool — see briefing text below |
| 0:10–0:35 | Loading DataFrames | `pd.read_csv()`, `.shape`, `.columns`, `.dtypes`, `.head()` |
| 0:35–1:10 | Exploration Methods | `.info()`, `.isnull().sum()`, `.value_counts()`, `.nunique()` |
| 1:10–1:40 | Selecting & Filtering | Boolean indexing, `.isin()`, multiple conditions |
| 1:40–2:00 | Group Exercise | Hands-on with `olist_orders_dataset.csv` |

---

## DeepSeek Transition Briefing (read verbatim at session start)

> "From today, you have a new tool: DeepSeek. But tools are only as good as the person using them. You have spent 3 weeks understanding Python from first principles. You know variables, loops, functions, and how to read a CSV by hand. Now when DeepSeek writes pandas code for you, you will understand every line — because you have built the foundation. Someone who skipped Weeks 1–3 would copy code they don't understand. You won't."

**Protocol**: After the instructor demo, groups attempt each task themselves first (5 minutes), then may use DeepSeek if stuck. All outputs must be verified against the expected values in this document.

---

## Key Concepts

### Loading DataFrames
Use `pd.read_csv()` to load CSV files; inspect with `.shape`, `.columns`, `.dtypes`, `.head()`

**Expected outputs:**
- `orders.shape` → `(99441, 8)`
- Columns: `order_id`, `customer_id`, `order_status`, `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`
- All dtypes show `object` (string) — dates not yet parsed

**Common mistake:** forgetting to import pandas first (`import pandas as pd`)

---

### Exploration Methods
Use `.info()`, `.isnull().sum()`, `.value_counts()`, `.nunique()` to understand the data

**Expected outputs:**
- `order_approved_at` nulls: 160
- `order_delivered_carrier_date` nulls: 1,783
- `order_delivered_customer_date` nulls: 2,965
- `.value_counts()`: delivered=96,478 | shipped=1,107 | canceled=625 | unavailable=609 | invoiced=314 | processing=301 | created=5 | approved=2
- `nunique(order_status)` = 8 | `nunique(order_id)` = 99,441

---

### Selecting & Filtering
Select columns (single → Series, multiple → DataFrame); filter rows using boolean indexing

**Expected outputs:**
- Subset with 3 columns: shape `(99441, 3)`
- Delivered orders: 96,478
- Canceled orders: 625
- Not delivered and not shipped: 1,756

**Common mistake:** forgetting double brackets `[[...]]` for multi-column selection; missing parentheses around conditions when using `&` or `|`

---

## Group Exercise

Using `olist_orders_dataset.csv` (already loaded as `orders`):

1. Load the file. Verify: `orders.shape == (99441, 8)`
2. How many orders have NO delivery date (`order_delivered_customer_date` is null)? Expected: **2,965**
3. Filter to 'canceled' OR 'unavailable' orders. How many rows? Expected: **1,234**
4. What % of all orders are 'delivered'? Expected: **97.01%**
5. Filter to the 3 most common statuses (delivered, shipped, invoiced) using `.isin()`. How many rows? Expected: **97,899**

All expected outputs verified against the actual Olist dataset.
