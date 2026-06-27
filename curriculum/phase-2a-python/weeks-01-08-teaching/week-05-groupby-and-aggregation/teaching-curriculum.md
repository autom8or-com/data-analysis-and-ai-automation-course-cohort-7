## WEEK 5 — GroupBy & Aggregation
*(DeepSeek assisted)*

### Wednesday: GroupBy Fundamentals

**Learning objectives:**
- Use .groupby() with single and multiple keys
- Apply aggregation functions: sum, mean, count, nunique, min, max
- Use .agg() for multiple aggregations at once
- Reset index after groupby

**Session outline (2 hours)**

**Part 1 — Single-Key GroupBy (35 min)**

```python
import pandas as pd

orders = pd.read_csv('olist_orders_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')
items = pd.read_csv('olist_order_items_dataset.csv')

# Orders per status
status_counts = orders.groupby('order_status')['order_id'].count()
print(status_counts.sort_values(ascending=False))
# delivered      96478
# shipped         1107
# ...

# Merge to get state info
orders_customers = orders.merge(customers, on='customer_id')

# Orders per state
state_orders = orders_customers.groupby('customer_state')['order_id'].count()
print(state_orders.sort_values(ascending=False).head(5))
# SP    41746
# RJ    12852
# MG    11635
# RS     5466
# PR     5045

# Revenue per state
orders_items = orders_customers.merge(items, on='order_id')
state_revenue = orders_items.groupby('customer_state')['price'].sum()
print(state_revenue.sort_values(ascending=False).head(5))
# SP    5202955.05
# RJ    1824092.67
# MG    1585308.03
# RS     750304.02
# PR     683083.76
```

**Part 2 — .agg() for Multiple Metrics (35 min)**

```python
# Multiple aggregations in one call
seller_stats = items.groupby('seller_id').agg(
    total_revenue=('price', 'sum'),
    avg_price=('price', 'mean'),
    total_items=('order_item_id', 'count'),
    unique_orders=('order_id', 'nunique')
).reset_index()

print(seller_stats.nlargest(5, 'total_revenue'))
# seller_id | total_revenue | avg_price | total_items | unique_orders

# Order-level summary
order_summary = items.groupby('order_id').agg(
    total_price=('price', 'sum'),
    total_freight=('freight_value', 'sum'),
    item_count=('order_item_id', 'count')
).reset_index()

print(f"Orders with >1 item: {(order_summary['item_count'] > 1).sum():,}")
# Expected: 9,803
print(f"Max items in one order: {order_summary['item_count'].max()}")
# Expected: 21
print(f"Avg items per order: {order_summary['item_count'].mean():.2f}")
# Expected: 1.14
```

**Part 3 — Group Exercise (40 min)**

```python
# Tasks — verified expected values:

# 1. Using orders + customers merged:
#    How many orders came from each state?
#    Print top 5. SP Expected: 41,746

# 2. Using items:
#    Total revenue + avg price by seller (top 5 by revenue)
#    Top seller revenue Expected: R$229,472.63

# 3. Build order_summary (group by order_id):
#    - total_price (sum), total_freight (sum), item_count (count)
#    - How many orders have exactly 1 item? Expected: ~90,000+
#    - What is max item count in a single order? Expected: 21

# 4. DeepSeek task: Ask DeepSeek to write code that groups orders
#    by order_status and calculates:
#    - count of orders, percentage of total, and avg approved_at delay
#    Validate the counts against the verified values above.
```

---

### Thursday: Time Series & Multi-Key GroupBy

**Learning objectives:**
- Parse datetime columns with pd.to_datetime()
- Extract year, month, day of week from datetime
- GroupBy with datetime components
- GroupBy with two keys (cross-tabulation)

**Session outline (2 hours)**

**Part 1 — Datetime Parsing (30 min)**

```python
orders = pd.read_csv('olist_orders_dataset.csv')

# All date columns load as 'object' (string)
print(orders['order_purchase_timestamp'].dtype)   # object

# Convert to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
print(orders['order_purchase_timestamp'].dtype)   # datetime64[ns]

# Extract components
orders['year'] = orders['order_purchase_timestamp'].dt.year
orders['month'] = orders['order_purchase_timestamp'].dt.month
orders['month_name'] = orders['order_purchase_timestamp'].dt.month_name()
orders['day_of_week'] = orders['order_purchase_timestamp'].dt.day_name()

# Orders by year
print(orders.groupby('year')['order_id'].count())
# 2016      329
# 2017    45101
# 2018    54011

# Monthly orders — 2017 only (full year)
orders_2017 = orders[orders['year'] == 2017]
monthly_2017 = orders_2017.groupby('month')['order_id'].count()
print(monthly_2017)
# 1      800
# 2     1780
# 3     2682
# 4     2404
# 5     3700
# 6     3245
# 7     4026
# 8     4331
# 9     4285
# 10    4631
# 11    7544  ← Black Friday peak
# 12    5673
```

**Part 2 — Multi-Key GroupBy (30 min)**

```python
# Orders per state per year
state_year = orders.merge(
    pd.read_csv('olist_customers_dataset.csv'), on='customer_id'
).groupby(['customer_state', 'year'])['order_id'].count().unstack(fill_value=0)

print(state_year.loc[['SP', 'RJ', 'MG']])
# Shows SP/RJ/MG orders split across 2016, 2017, 2018

# Day of week orders
dow_counts = orders.groupby('day_of_week')['order_id'].count()
print(dow_counts.sort_values(ascending=False))
# Which day has the most orders? (should be weekdays > weekends)
```

**Part 3 — Group Exercise (40 min)**

```python
# Tasks — verified expected values:

# 1. Parse order_purchase_timestamp. Verify year distribution:
#    2016: 329, 2017: 45,101, 2018: 54,011

# 2. Monthly order count for 2017.
#    Which month had most orders? Expected: November (7,544) — Black Friday!

# 3. Average order value (from items) per month for 2017
#    Merge orders + items, then groupby month and take mean of price

# 4. DeepSeek task: Ask DeepSeek to write code showing
#    "the number of orders per day of week"
#    Which day of the week sees the most orders?
#    Validate the total sums to 99,441.
```

**Weekly Assignment 5:**

Submit `week5_assignment.ipynb`:

1. Load `olist_orders_dataset.csv`. Parse `order_purchase_timestamp` to datetime. Add columns: `year`, `month`, `day_of_week`.

2. Monthly order trend for **2018** (use only 2018 data):
   - Note: Sep 2018 has only 16 orders, Oct 2018 has 4. Why? *(The dataset ends Oct 17, 2018 — incomplete months)*

3. Load `olist_order_items_dataset.csv`. Merge with orders. Build a grouped table:
   - Rows: customer_state (from customers dataset — requires another merge)
   - Values: total revenue, avg price, order count
   - Sort by total revenue descending. Print top 5.
   - Verify SP = R$5,202,955.05

4. **DeepSeek challenge:** Ask DeepSeek to group orders by `order_status` and `year` (multi-key groupby) and show the count for each combination. Paste the DeepSeek prompt you used, the code it returned, and your output. Does delivered + 2018 = 54,011? *(Note: actual answer requires counting only delivered in 2018 — explore this)*

---
