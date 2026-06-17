## WEEK 4 — Pandas Introduction
*(DeepSeek assistance begins)*

**Transition briefing — start of Wednesday session (10 min):**

> *"From today, you have a new tool: DeepSeek. But tools are only as good as the person using them. You have spent 3 weeks understanding Python from first principles. You know variables, loops, functions, and how to read a CSV by hand. Now when DeepSeek writes pandas code for you, you will understand every line — because you have built the foundation. Someone who skipped Weeks 1–3 would copy code they don't understand. You won't."*

**How to use DeepSeek this session:**
After the instructor demo, groups attempt each task themselves first (5 minutes), then may use DeepSeek if stuck. All outputs must be verified against the expected values in this document.

---

### Wednesday: DataFrames — Loading, Inspecting & Selecting

**Learning objectives:**
- Import pandas and load a CSV into a DataFrame
- Use .shape, .columns, .dtypes, .head(), .tail(), .info(), .describe()
- Select columns and filter rows
- Use .value_counts() and .nunique()

**Session outline (2 hours)**

**Part 1 — Loading Data (25 min)**

```python
import pandas as pd

# Load the orders dataset
orders = pd.read_csv('olist_orders_dataset.csv')

# Inspect
print(type(orders))           # <class 'pandas.core.frame.DataFrame'>
print(orders.shape)           # (99441, 8)
print(orders.columns.tolist())
# ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
#  'order_approved_at', 'order_delivered_carrier_date',
#  'order_delivered_customer_date', 'order_estimated_delivery_date']

print(orders.dtypes)
# All columns show 'object' (string) — dates haven't been parsed yet

orders.head(3)
# Returns first 3 rows — shows real data
```

**Part 2 — Exploration Methods (35 min)**

```python
# .info() — column types and null counts in one view
orders.info()
# Shows: 99441 entries, 8 columns
# order_approved_at: 99281 non-null (160 nulls)
# order_delivered_carrier_date: 97658 non-null (1783 nulls)
# order_delivered_customer_date: 96476 non-null (2965 nulls)

# .describe() — numeric summary (only works on numeric columns)
# Since all columns are 'object', describe on a specific column:
print(orders['order_status'].describe())
# count: 99441, unique: 8, top: delivered, freq: 96478

# .isnull().sum() — null count per column
print(orders.isnull().sum())
# order_approved_at               160
# order_delivered_carrier_date   1783
# order_delivered_customer_date  2965

# .value_counts()
print(orders['order_status'].value_counts())
# delivered      96478
# shipped         1107
# canceled         625
# unavailable      609
# invoiced         314
# processing       301
# created            5
# approved           2

# .nunique()
print(orders['order_status'].nunique())    # 8
print(orders['order_id'].nunique())        # 99441 (all unique)
print(orders['customer_id'].nunique())     # 99441 (each order = unique customer_id)
```

**Part 3 — Selecting & Filtering (30 min)**

```python
# Select a single column → Series
status_col = orders['order_status']
print(type(status_col))    # <class 'pandas.core.series.Series'>

# Select multiple columns → DataFrame
subset = orders[['order_id', 'order_status', 'order_purchase_timestamp']]
print(subset.shape)        # (99441, 3)

# Filter rows — boolean indexing
delivered = orders[orders['order_status'] == 'delivered']
print(len(delivered))      # 96478

canceled = orders[orders['order_status'] == 'canceled']
print(len(canceled))       # 625

# Multiple conditions
not_delivered = orders[
    (orders['order_status'] != 'delivered') &
    (orders['order_status'] != 'shipped')
]
print(len(not_delivered))  # 1756  (625+609+314+301+5+2)

# Filter + select columns together
canceled_ids = orders[orders['order_status'] == 'canceled']['order_id']
print(canceled_ids.head())
```

**Part 4 — Group Exercise (30 min)**

```python
# Tasks — all expected answers verified:

# 1. Load olist_orders_dataset.csv. Verify: orders.shape == (99441, 8)

# 2. How many orders have NO delivery date (order_delivered_customer_date is null)?
#    orders['order_delivered_customer_date'].isnull().sum()
#    Expected: 2,965

# 3. Filter to orders where status is 'canceled' OR 'unavailable'
#    How many rows? Expected: 625 + 609 = 1,234

# 4. What % of all orders are 'delivered'?
#    Expected: 96478 / 99441 * 100 = 97.01%

# 5. Filter the DataFrame to only the 3 most common statuses.
#    Hint: use isin(['delivered', 'shipped', 'invoiced'])
#    How many rows? Expected: 96478 + 1107 + 314 = 97,899
```

---

### Thursday: Sorting, Calculating & value_counts Deep Dive

**Learning objectives:**
- Sort DataFrames with .sort_values()
- Add calculated columns
- Use .nlargest() / .nsmallest()
- Chain pandas operations

**Session outline (2 hours)**

**Part 1 — Load Items & Calculate Revenue (30 min)**

```python
import pandas as pd

items = pd.read_csv('olist_order_items_dataset.csv')
print(items.shape)          # (112650, 7)
print(items.columns.tolist())
# ['order_id', 'order_item_id', 'product_id', 'seller_id',
#  'shipping_limit_date', 'price', 'freight_value']

print(items.describe())
# price:  mean=120.65, max=6735.00, min=0.85
# freight_value: mean=19.99, max=409.68

# Add calculated column
items['total_cost'] = items['price'] + items['freight_value']
print(items['total_cost'].mean().round(2))   # 140.64
print(items['total_cost'].sum())             # R$15,843,553.24

# Add value tier
items['price_tier'] = items['price'].apply(
    lambda x: "Premium" if x >= 500 else "Standard" if x >= 100 else "Economy"
)
print(items['price_tier'].value_counts())
# Economy     73397
# Standard    30760
# Premium      8493
```

**Part 2 — Sorting & nlargest (30 min)**

```python
# Sort by price descending
expensive = items.sort_values('price', ascending=False)
print(expensive[['order_id', 'price', 'freight_value']].head(5))
# Top price: R$6,735.00

# nlargest/nsmallest
print(items.nlargest(5, 'price')[['product_id', 'price']])
print(items.nsmallest(5, 'price')[['product_id', 'price']])

# Revenue by seller
seller_revenue = items.groupby('seller_id')['price'].sum()
print(seller_revenue.nlargest(5))
# Top seller: R$229,472.63
# 2nd seller: R$222,776.05
```

**Part 3 — Group Exercise (40 min)**

```python
# Using olist_order_items_dataset.csv:

# 1. Total revenue (sum of price column)
#    Expected: R$13,591,643.70

# 2. Total freight collected
#    Expected: R$2,251,909.54

# 3. Add a column 'revenue_share' = price / total revenue * 100
#    (each item's % contribution to total revenue)

# 4. How many items are in the "Premium" tier (price >= R$500)?
#    Expected: 8,493 items

# 5. Which order has the most items?
#    Hint: groupby order_id, count order_item_id, nlargest(1)
#    Expected: max items in one order = 21

# 6. What is the average freight as a % of price?
#    Expected: items['freight_value'] / items['price'] → mean → ~20%
```

**Weekly Assignment 4:**

Submit `week4_assignment.ipynb`:

1. Load both `olist_orders_dataset.csv` and `olist_order_items_dataset.csv`.
   Print `.shape` and `.isnull().sum()` for each.

2. From the orders DataFrame:
   - How many unique order statuses exist? *(Expected: 8)*
   - What % of orders are NOT yet delivered (status ≠ 'delivered')? *(Expected: 3.0%)*
   - Filter to only orders with status 'canceled' or 'unavailable'. How many rows? *(Expected: 1,234)*

3. From the items DataFrame:
   - Add a `total_cost` column (price + freight_value)
   - Add a `price_tier` column: Premium (≥500), Standard (≥100), Economy (<100)
   - What is the count of each tier? *(Expected: Economy=73,397 / Standard=30,760 / Premium=8,493)*

4. Find the top 5 sellers by total revenue (sum of price, grouped by seller_id).
   What is the revenue of the #1 seller? *(Expected: R$229,472.63)*

---
