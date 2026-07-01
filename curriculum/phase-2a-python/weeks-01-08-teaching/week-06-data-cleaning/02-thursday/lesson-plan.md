# Week 6 — Data Cleaning: Thursday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: TBD | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-06-thu-demo.ipynb`
- [ ] Student exercise link ready to share: `week-06-thu-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek tab open at chat.deepseek.com

---

## Learning Objectives

By the end of this session, students will be able to:
1. Use the .str accessor for vectorised string operations
2. Apply .str.strip(), .str.title(), .str.upper(), .str.contains(), .str.replace()
3. Split strings in pandas
4. Combine string cleaning with filtering

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:05 | Setup & recap | Students open Colab, load customers + orders + reviews + translations |
| 0:05–0:35 | The .str Accessor | Demo strip/title on cities, str.contains for 'paulo' |
| 0:35–1:05 | str.replace() and Category Labels | Demo underscore → space + title case on translations |
| 1:05–1:15 | String Length & Null Detection | Demo str.len() + has_comment flag on reviews |
| 1:15–1:50 | Group Exercise | 4 tasks including DeepSeek challenge |
| 1:50–2:00 | Debrief + Assignment intro | Share expected answers, hand out assignment |

---

## Key Concepts

### The .str Accessor
Vectorised string methods on pandas Series via the .str accessor — strip whitespace, change case, search and replace.

Expected outputs:
- `customers['customer_city_clean'].head(5)`: `['Franca', 'Sao Bernardo Do Campo', 'Sao Paulo', 'Mogi Das Cruzes', 'Campinas']`
- `paulo_count`: `15,606` customers in cities containing 'paulo'

Common mistake to watch for:
- Calling `.strip()` directly on a column without `.str` — raises `AttributeError`

---

### str.replace() and Category Labels
Replace underscores with spaces and apply title case to create human-readable category names.

Expected outputs:
- `translations['category_display'].head(3)`: `['Health Beauty', 'Computers Accessories', 'Auto']`
- Total: 71 categories

Common mistake to watch for:
- Using `.str.replace('_', ' ')` without `regex=False` — the default regex mode can cause unexpected behaviour

---

### String Length and Null Detection
Use str.len() and notna() to detect and measure comment text in reviews.

Expected outputs:
- `reviews_with_comment`: 40,977 rows (41.3% of 99,224 total)
- Average comment length: ~103.9 characters

---

## Group Exercise

1. Load customers. Clean `customer_city`: strip + title case. How many unique cities after cleaning? (May differ from before due to space normalisation)

2. Load reviews. Add `has_comment` = True/False based on whether `review_comment_message` is not null. What % of reviews have a comment? Expected: (99,224 − 58,247) / 99,224 = 41.3%

3. Load translation. Add `category_display` column: `product_category_name_english` with `_` replaced by space, in Title Case. Print all 71 category display names.

4. DeepSeek challenge: Ask DeepSeek to find the top 5 cities by number of orders. Use orders + customers merge, groupby `customer_city` (cleaned), count. Verify: Sao Paulo is #1 with 15,540+ orders.

**Expected outputs:**
- Task 2: 41.3% reviews with comment
- Task 3: 71 category display names
- Task 4: Sao Paulo #1 city

---

## Weekly Assignment

Submit `week6_assignment.ipynb`:

1. Load `olist_products_dataset.csv`. Fix the two column name typos. Fill null `product_category_name` with `'unknown'`. Confirm 0 nulls remain.

2. Load `olist_orders_dataset.csv`. Convert all 5 date columns. Calculate `delivery_days`. Answer:
   - What is the median delivery time? *(Expected: 10.0 days)*
   - What % of delivered orders took more than 30 days?
   - What is the longest delivery in days? *(Expected: 209 days)*

3. Load `olist_customers_dataset.csv`. Clean `customer_city` (strip + title case). Find the top 10 cities by customer count. *(Expected: Sao Paulo = 15,540)*

4. Load `olist_order_reviews_dataset.csv`. Add `has_comment` column. What % of reviews include a comment message? For those that do, what is the average comment length in characters?
