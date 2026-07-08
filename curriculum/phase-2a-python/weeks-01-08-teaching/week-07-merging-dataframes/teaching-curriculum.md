## WEEK 7 — Merging DataFrames
*(DeepSeek assisted)*

### Wednesday: Joins — Concepts & Practice

**Learning objectives:**
- Understand inner, left, right, and outer joins
- Use pd.merge() correctly
- Detect and handle unmatched rows after a join
- Merge on different key column names

**Session outline (2 hours)**

**Part 1 — Join Types Explained (20 min)**

Use a visual analogy:
- **Inner join:** Only rows that match in BOTH tables (like an intersection)
- **Left join:** All rows from left table + matched rows from right (unmatched right = NaN)
- **Right join:** Reverse of left join
- **Outer join:** All rows from both tables (unmatched = NaN on either side)

**Part 2 — Orders + Customers (35 min)**

```python
import pandas as pd

orders = pd.read_csv('olist_orders_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')

# Both tables have 99,441 rows with customer_id as the join key
print(orders.shape)      # (99441, 8)
print(customers.shape)   # (99441, 5)

# Inner merge (default)
oc = orders.merge(customers, on='customer_id')
print(oc.shape)          # (99441, 12)
# Same row count because every customer_id in orders exists in customers

# What columns were added?
new_cols = [c for c in oc.columns if c not in orders.columns]
print(new_cols)
# ['customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']

# Now we can group by state
state_orders = oc.groupby('customer_state')['order_id'].count().sort_values(ascending=False)
print(state_orders.head(5))
# SP    41746
# RJ    12852
# MG    11635
# RS     5466
# PR     5045
```

**Part 3 — Items + Products + Translation (35 min)**

```python
items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
translation = pd.read_csv('product_category_name_translation.csv')

# Step 1: items + products (left join — keep all items even if product unknown)
items_products = items.merge(
    products[['product_id', 'product_category_name']],
    on='product_id',
    how='left'
)
print(items_products.shape)   # (112650, 8)
print(items_products['product_category_name'].isnull().sum())  # 1,603 unmatched

# Step 2: + translation
items_cat = items_products.merge(
    translation,
    on='product_category_name',
    how='left'
)
print(items_cat.shape)   # (112650, 9)

# Revenue by category
cat_revenue = items_cat.groupby('product_category_name_english')['price'].sum()
print(cat_revenue.nlargest(10).round(2))
# health_beauty            1258681.34
# watches_gifts            1205005.68
# bed_bath_table           1036988.68
# sports_leisure            988048.97
# computers_accessories     911954.32
```

**Part 4 — Group Exercise (25 min)**

```python
# Build the full merged table step by step:
# orders → merge customers (on customer_id)
# → merge items (on order_id)
# → merge products[['product_id','product_category_name']] (on product_id, how='left')
# → merge translation (on product_category_name, how='left')

# Final shape should be: (112650, 20)
# Verify: full.shape == (112650, 20)

# Then answer:
# What is the total revenue from SP state?
# Expected: R$5,202,955.05

# What is the top category by revenue in RJ state?
```

---

### Thursday: Multi-Table Analysis & concat

**Learning objectives:**
- Chain multiple merges cleanly
- Use pd.concat() to stack DataFrames
- Handle mismatched columns after concat
- Build a complete multi-table analysis

**Session outline (2 hours)**

**Part 1 — Full Pipeline (40 min)**

```python
import pandas as pd

path = ''  # adjust to your file path

# Load all needed tables
orders = pd.read_csv(path + 'olist_orders_dataset.csv')
customers = pd.read_csv(path + 'olist_customers_dataset.csv')
items = pd.read_csv(path + 'olist_order_items_dataset.csv')
products = pd.read_csv(path + 'olist_products_dataset.csv')
translation = pd.read_csv(path + 'product_category_name_translation.csv')
payments = pd.read_csv(path + 'olist_order_payments_dataset.csv')
reviews = pd.read_csv(path + 'olist_order_reviews_dataset.csv')

# Full analysis table
full = (
    orders
    .merge(customers, on='customer_id')
    .merge(items, on='order_id')
    .merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
    .merge(translation, on='product_category_name', how='left')
)
print(full.shape)    # (112650, 20)

# Revenue + avg review by category
full_reviews = full.merge(
    reviews[['order_id', 'review_score']],
    on='order_id',
    how='left'
)

cat_analysis = full_reviews.groupby('product_category_name_english').agg(
    total_revenue=('price', 'sum'),
    avg_review=('review_score', 'mean'),
    order_count=('order_id', 'nunique')
).reset_index().sort_values('total_revenue', ascending=False)

print(cat_analysis.head(10).round(2))
```

**Part 2 — Payment Analysis (25 min)**

```python
# Payment types breakdown
pay_summary = payments.groupby('payment_type').agg(
    count=('order_id', 'count'),
    total_value=('payment_value', 'sum'),
    avg_installments=('payment_installments', 'mean')
).reset_index()

pay_summary['pct'] = pay_summary['count'] / pay_summary['count'].sum() * 100
print(pay_summary.round(2))
# credit_card: 76795, R$12.3M, 73.9%, avg 3.0 installments
# boleto: 19784, 19.0%
# voucher: 5775, 5.6%
# debit_card: 1529, 1.5%
```

**Part 3 — Group Exercise (40 min)**

```python
# Build the complete multi-table analysis:
# 1. Merge: orders + customers + items + products + translation + reviews
# 2. GroupBy customer_state, calculate:
#    - total_revenue (sum of price)
#    - avg_review_score (mean of review_score)
#    - order_count (nunique of order_id)
# 3. Which state has the highest avg review score among those with >500 orders?
# 4. DeepSeek task: Ask DeepSeek to add the payments table to the analysis
#    and show avg payment_installments by state.
#    Validate: Brazil avg installments = 2.85
```

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

