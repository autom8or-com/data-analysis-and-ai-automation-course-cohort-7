## WEEK 6 — Data Cleaning
*(DeepSeek assisted)*

### Wednesday: Handling Nulls & Data Types

**Learning objectives:**
- Identify and count null values
- Use fillna(), dropna(), and conditional replacement
- Convert data types correctly
- Recognise the typo in the products dataset

**Session outline (2 hours)**

**Part 1 — Products Dataset — A Real Cleaning Challenge (30 min)**

```python
import pandas as pd

products = pd.read_csv('olist_products_dataset.csv')
print(products.shape)          # (32951, 9)
print(products.isnull().sum())
# product_category_name         610
# product_name_lenght           610   ← NOTE THE TYPO
# product_description_lenght    610   ← TYPO HERE TOO
# product_photos_qty            610
# product_weight_g                2
# product_length_cm               2
# product_height_cm               2
# product_width_cm                2

# Fix the column name typo
products = products.rename(columns={
    'product_name_lenght': 'product_name_length',
    'product_description_lenght': 'product_description_length'
})
print(products.columns.tolist())
# ['product_id', 'product_category_name', 'product_name_length',
#  'product_description_length', 'product_photos_qty',
#  'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
```

**Part 2 — fillna & dropna (35 min)**

```python
# Option 1: fillna — replace nulls with a value
products_filled = products.copy()
products_filled['product_category_name'] = products_filled['product_category_name'].fillna('unknown')

# Verify
print(products_filled['product_category_name'].isnull().sum())   # 0
print((products_filled['product_category_name'] == 'unknown').sum())  # 610

# Option 2: dropna — remove rows with nulls
products_dropped = products.dropna(subset=['product_category_name'])
print(products_dropped.shape)    # (32341, 9) — 610 rows removed

# Option 3: dropna on ALL columns (removes rows where ANY column is null)
products_all_clean = products.dropna()
print(products_all_clean.shape)  # (32341, 9) — same result here

# When to use which:
# fillna → when null means "category not set yet" and you want to keep the row
# dropna → when null means the row is too incomplete to use
```

**Part 3 — Datetime Conversion & Delivery Time Calculation (30 min)**

```python
orders = pd.read_csv('olist_orders_dataset.csv')

# Convert all date columns at once
date_cols = ['order_purchase_timestamp', 'order_approved_at',
             'order_delivered_carrier_date', 'order_delivered_customer_date',
             'order_estimated_delivery_date']

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')

# errors='coerce' → turns unparseable values into NaT (not-a-time) instead of error

# Calculate delivery days
orders['delivery_days'] = (
    orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
).dt.days

# Stats on delivery time (delivered orders only)
delivered = orders[orders['order_status'] == 'delivered']
print(delivered['delivery_days'].describe().round(1))
# count    96470.0
# mean        12.1
# std          9.6
# min          0.0
# 25%          6.0
# 50%         10.0
# 75%         15.0
# max        209.0
```

**Part 4 — Group Exercise (20 min)**

```python
# Tasks:
# 1. Load products. Print null counts. Fix the column name typos.
#    Verify: renamed columns show 'product_name_length' (not 'lenght')

# 2. Fill null product_category_name with 'unknown'
#    Verify: 0 nulls remain, 610 rows have value 'unknown'

# 3. Load orders. Convert all 5 date columns using pd.to_datetime(errors='coerce')
#    Calculate delivery_days. Verify: mean ≈ 12.1 days

# 4. What % of orders have a delivery_days value > 30 (slow)?
#    Hint: delivered['delivery_days'].gt(30).mean() * 100
```

---

### Thursday: String Cleaning in Pandas

**Learning objectives:**
- Use the .str accessor for vectorised string operations
- Apply .str.strip(), .str.title(), .str.upper(), .str.contains(), .str.replace()
- Split strings in pandas
- Combine string cleaning with filtering

**Session outline (2 hours)**

**Part 1 — The .str Accessor (30 min)**

```python
customers = pd.read_csv('olist_customers_dataset.csv')

# Cities come in lowercase and may have spaces
print(customers['customer_city'].head(5).tolist())
# ['franca', 'sao bernardo do campo', 'sao paulo', 'mogi das cruzes', 'campinas']

# Standardise
customers['customer_city_clean'] = customers['customer_city'].str.strip().str.title()
print(customers['customer_city_clean'].head(5).tolist())
# ['Franca', 'Sao Bernardo Do Campo', 'Sao Paulo', 'Mogi Das Cruzes', 'Campinas']

# Count cities containing 'paulo'
paulo_count = customers['customer_city'].str.contains('paulo', case=False).sum()
print(paulo_count)    # 15,606

# Replace _ with space in categories
translation = pd.read_csv('product_category_name_translation.csv')
translation['category_clean'] = translation['product_category_name_english'].str.replace('_', ' ').str.title()
print(translation[['product_category_name_english', 'category_clean']].head(5))
# health_beauty → Health Beauty
# computers_accessories → Computers Accessories
```

**Part 2 — Splitting & Extracting (30 min)**

```python
orders = pd.read_csv('olist_orders_dataset.csv')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Extract date-only string
orders['purchase_date'] = orders['order_purchase_timestamp'].dt.strftime('%Y-%m-%d')
print(orders['purchase_date'].head(3).tolist())
# ['2017-10-02', '2018-07-24', '2018-08-08']

# Extract month-year label
orders['month_year'] = orders['order_purchase_timestamp'].dt.strftime('%b %Y')
print(orders['month_year'].value_counts().head(5))
# Aug 2018    10843 → wait, check this
# Most likely Nov 2017 or similar as peak

# String length analysis on reviews
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
reviews['comment_length'] = reviews['review_comment_message'].str.len()
print(reviews['comment_length'].describe().round(1))
# count    40977.0 (only non-null messages)
# mean       103.9
```

**Part 3 — Group Exercise (35 min)**

```python
# 1. Load customers. Clean customer_city: strip + title case.
#    How many unique cities after cleaning?
#    (May differ from before cleaning due to space normalisation)

# 2. Load reviews. Add 'has_comment' = True/False based on whether
#    review_comment_message is not null.
#    What % of reviews have a comment?
#    Expected: (99224 - 58247) / 99224 = 41.3%

# 3. Load translation. Add 'category_display' column:
#    product_category_name_english with _ replaced by space, in Title Case.
#    Print all 71 category display names.

# 4. DeepSeek challenge: Ask DeepSeek to find the top 5 cities by number of orders.
#    Use orders + customers merge, groupby customer_city (cleaned), count.
#    Verify: Sao Paulo is #1 with 15,540+ orders.
```

**Weekly Assignment 6:**

Submit `week6_assignment.ipynb`:

1. Load `olist_products_dataset.csv`. Fix the two column name typos. Fill null `product_category_name` with `'unknown'`. Confirm 0 nulls remain.

2. Load `olist_orders_dataset.csv`. Convert all 5 date columns. Calculate `delivery_days`. Answer:
   - What is the median delivery time? *(Expected: 10.0 days)*
   - What % of delivered orders took more than 30 days?
   - What is the longest delivery in days? *(Expected: 209 days)*

3. Load `olist_customers_dataset.csv`. Clean `customer_city` (strip + title case). Find the top 10 cities by customer count. *(Expected: Sao Paulo = 15,540)*

4. Load `olist_order_reviews_dataset.csv`. Add `has_comment` column. What % of reviews include a comment message? For those that do, what is the average comment length in characters?

---
