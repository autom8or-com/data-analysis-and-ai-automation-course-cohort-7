# Week 7 — Merging DataFrames: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-07-wed-demo.ipynb`
- [ ] Student exercise link ready to share: `week-07-wed-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek access confirmed for all students (Week 4+ requirement)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Understand inner, left, right, and outer joins
2. Use `pd.merge()` correctly
3. Detect and handle unmatched rows after a join
4. Merge on different key column names

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:20 | Join Types Explained | Visual analogy: inner = intersection, left = all-left-plus-matched, right = reverse of left, outer = union with NaN gaps |
| 0:20–0:55 | Orders + Customers merge | Inner merge on `customer_id`, inspect new columns, groupby state |
| 0:55–1:30 | Items + Products + Translation merge | Two chained left joins, detect unmatched rows via `.isnull().sum()` |
| 1:30–1:55 | Group Exercise | Build the full merged table step by step |
| 1:55–2:00 | Debrief & preview | Share expected answers, preview Thursday's multi-table analysis |

---

## Key Concepts

### Join Types
Inner join keeps only rows matching in both tables; left join keeps all left rows plus matched right rows (unmatched = NaN); right join is the reverse of left; outer join keeps all rows from both tables (unmatched = NaN on either side).

Common mistake to watch for: students default to inner join without realizing they may silently drop unmatched rows — always ask "should unmatched rows survive?" before choosing `how=`.

### Orders + Customers merge
Inner merge of orders and customers on `customer_id`; both tables have matching row counts so no rows are lost.

Expected outputs:
- `orders.shape` → (99441, 8)
- `customers.shape` → (99441, 5)
- merged shape → (99441, 12)
- new columns added: `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`
- top 5 states by order count: SP 41,746 | RJ 12,852 | MG 11,635 | RS 5,466 | PR 5,045

Common mistake to watch for: forgetting that `merge()` returns a new DataFrame — students sometimes call `orders.merge(customers, on='customer_id')` and then reference `orders` expecting it to be merged.

### Items + Products + Translation merge (left joins)
Left join items to products (keeping unmatched items) then to the category name translation table; reveals unmatched product rows.

Expected outputs:
- `items_products.shape` → (112650, 8)
- unmatched `product_category_name` after left join → 1,603
- `items_cat.shape` → (112650, 9)
- top 5 categories by revenue: health_beauty R$1,258,681.34 | watches_gifts R$1,205,005.68 | bed_bath_table R$1,036,988.68 | sports_leisure R$988,048.97 | computers_accessories R$911,954.32

Common mistake to watch for: using `how='inner'` here would silently drop the 1,603 items with unmatched categories — stress why `how='left'` is the right choice when you want to keep every item row.

---

## Group Exercise

Build the full merged table step by step:
- orders → merge customers (on `customer_id`)
- → merge items (on `order_id`)
- → merge products[['product_id','product_category_name']] (on `product_id`, `how='left'`)
- → merge translation (on `product_category_name`, `how='left'`)

Final shape should be: (112650, 20). Verify: `full.shape == (112650, 20)`.

Then answer:
- What is the total revenue from SP state? Expected: R$5,202,955.05
- What is the top category by revenue in RJ state?

**Expected outputs**: full merged shape (112650, 20); SP state total revenue R$5,202,955.05.

---
