## WEEK 3 — Functions & First Contact with Data
*(No AI assistance)*

### Wednesday: Functions Deep Dive

**Learning objectives:**
- Write well-structured functions with parameters, defaults, and return values
- Use docstrings for documentation
- Handle edge cases with try/except
- Chain functions together

**Session outline (2 hours)**

**Part 1 — Function Fundamentals (30 min)**

```python
# Basic function anatomy
def calculate_total_cost(price, freight):
    """
    Calculate the total order cost.

    Args:
        price: item price in R$
        freight: shipping cost in R$
    Returns:
        float: total cost
    """
    return price + freight

# Test with verified Olist values
print(calculate_total_cost(58.90, 13.29))   # 72.19
print(calculate_total_cost(239.90, 19.93))  # 259.83
print(calculate_total_cost(199.00, 17.87))  # 216.87

# Default parameters
def classify_review(score, positive_threshold=4, negative_threshold=2):
    """Classify review score as Positive, Neutral, or Negative."""
    if score >= positive_threshold:
        return "Positive"
    elif score <= negative_threshold:
        return "Negative"
    else:
        return "Neutral"

# Standard thresholds
for s in [1, 2, 3, 4, 5]:
    print(f"Score {s} → {classify_review(s)}")
# Score 1 → Negative
# Score 2 → Negative
# Score 3 → Neutral
# Score 4 → Positive
# Score 5 → Positive
```

**Part 2 — Functions Returning Multiple Values (25 min)**

```python
def delivery_analysis(purchase_date_str, delivery_date_str):
    """
    Calculate delivery time and classify it.
    Returns (days, classification) tuple.
    """
    from datetime import datetime
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        purchase = datetime.strptime(purchase_date_str, fmt)
        delivery = datetime.strptime(delivery_date_str, fmt)
        days = (delivery - purchase).days
        if days <= 7:
            status = "Fast"
        elif days <= 14:
            status = "Normal"
        else:
            status = "Slow"
        return days, status
    except:
        return None, "Unknown"

# Verified from actual Olist rows
days, status = delivery_analysis("2017-10-02 10:56:33", "2017-10-10 21:25:13")
print(f"Days: {days}, Status: {status}")    # Days: 8, Status: Normal

days, status = delivery_analysis("2018-07-24 20:41:37", "2018-08-07 15:27:45")
print(f"Days: {days}, Status: {status}")    # Days: 13, Status: Normal
```

**Part 3 — Group Exercise (40 min)**

```python
# Write these 4 functions using what you have learned:

# Function 1: summarise_orders(status_list, count_list)
# Takes two lists, returns a dict: {status: count}
# Test with the 8 Olist statuses and counts

# Function 2: top_n_items(data_dict, n=5)
# Takes a dict {key: numeric_value}, returns list of top n (key, value) tuples
# Test: top_n_items({"SP":41746,"RJ":12852,"MG":11635,"RS":5466,"PR":5045}, 3)
# Expected: [("SP",41746), ("RJ",12852), ("MG",11635)]

# Function 3: format_currency(amount, currency="R$")
# Returns formatted string: "R$1,234.56"
# Test: format_currency(5202955.05) → "R$5,202,955.05"

# Function 4: safe_divide(numerator, denominator, default=0.0)
# Returns numerator/denominator, returns default if denominator is 0
# Test: safe_divide(96478, 99441) → 0.9702...
# Test: safe_divide(100, 0) → 0.0
```

---

### Thursday: Reading Real Data with Python

**Learning objectives:**
- Open and read CSV files using `open()` and the `csv` module
- Build a list of dicts from a CSV file
- Apply functions to CSV data
- Understand why pandas will make all of this easier

**Session outline (2 hours)**

**Part 1 — Reading CSV with open() (30 min)**

```python
import csv

# Mount Google Drive first (instructor demonstrates once)
# from google.colab import drive
# drive.mount('/content/drive')

# Reading the orders file
filepath = 'olist_orders_dataset.csv'  # adjust path to where it's stored

row_count = 0
with open(filepath, 'r') as f:
    reader = csv.DictReader(f)
    print("Headers:", reader.fieldnames)
    # Headers: ['order_id', 'customer_id', 'order_status',
    #           'order_purchase_timestamp', 'order_approved_at',
    #           'order_delivered_carrier_date', 'order_delivered_customer_date',
    #           'order_estimated_delivery_date']
    for row in reader:
        row_count += 1

print(f"Total rows: {row_count:,}")   # Total rows: 99,441
```

**Part 2 — Building Data Structures from CSV (35 min)**

```python
import csv

def load_orders(filepath, limit=None):
    """
    Load orders CSV into a list of dicts.

    Args:
        filepath: path to CSV file
        limit: max rows to load (None = all rows)
    Returns:
        list of dicts
    """
    orders = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit and i >= limit:
                break
            orders.append(row)
    return orders

# Load first 1000 rows for exploration
orders_sample = load_orders('olist_orders_dataset.csv', limit=1000)

print(f"Loaded: {len(orders_sample)} orders")    # Loaded: 1000 orders
print(f"First order: {orders_sample[0]}")
print(f"Status of first order: {orders_sample[0]['order_status']}")  # delivered

# Count statuses manually
from collections import Counter
status_counts = Counter(o['order_status'] for o in orders_sample)
print(f"\nStatus counts (sample of 1000):")
for status, count in status_counts.most_common():
    print(f"  {status}: {count}")
```

**Part 3 — Applying Functions to CSV Data (30 min)**

```python
# Load all orders
orders = load_orders('olist_orders_dataset.csv')
print(f"Total: {len(orders):,}")   # 99,441

# Apply our classify_review logic to a different column
def classify_delivery_days_str(purchase_str, delivery_str):
    """Works directly on the raw string values from CSV."""
    if not delivery_str:
        return "Not Delivered"
    from datetime import datetime
    try:
        p = datetime.strptime(purchase_str[:19], "%Y-%m-%d %H:%M:%S")
        d = datetime.strptime(delivery_str[:19], "%Y-%m-%d %H:%M:%S")
        days = (d - p).days
        if days <= 7: return "Fast"
        elif days <= 14: return "Normal"
        else: return "Slow"
    except:
        return "Unknown"

# Count delivery speed across all orders
delivery_counts = Counter()
for order in orders:
    speed = classify_delivery_days_str(
        order['order_purchase_timestamp'],
        order['order_delivered_customer_date']
    )
    delivery_counts[speed] += 1

print("Delivery speed distribution:")
for speed, count in delivery_counts.most_common():
    pct = count / len(orders) * 100
    print(f"  {speed}: {count:,} ({pct:.1f}%)")
```

**Key teaching moment — end of Part 3:**

> *"We just did something real: we read 99,441 rows, applied a classification function to every row, and counted the results. But notice how much code that took — 25+ lines. Next week, we'll do the same thing in 3 lines using pandas. That's why pandas exists."*

**Part 4 — Group Exercise (20 min)**

```python
# Tasks using the loaded orders list:

# 1. Count how many orders have a blank order_delivered_customer_date
#    (Hint: check if the value is an empty string "")
#    Expected: ~2,965 rows have no delivery date

# 2. Write a function count_by_status(orders_list) that returns a dict
#    of {status: count} for all statuses in the list
#    Verify: delivered should be 96,478

# 3. Using a list comprehension, create a list of all unique customer states
#    (Hint: you'll need to load customers file too, or just use orders for now)

# 4. From the orders list, filter to only "canceled" orders
#    How many are there? Expected: 625
```

**Weekly Assignment 3:**

Submit `week3_assignment.ipynb`:

1. Write a function `load_csv(filepath, limit=None)` that loads any CSV file into a list of dicts. Test it on `olist_orders_dataset.csv`. Verify row count = **99,441**.

2. Using the loaded orders, write a function `status_report(orders_list)` that:
   - Counts each status
   - Calculates each status as a % of total
   - Returns a list of dicts: `[{"status": "delivered", "count": 96478, "pct": 97.0}, ...]`
   - Print each item as: `"delivered: 96,478 orders (97.0%)"`

3. Write a function `find_orders_by_status(orders_list, status)` that filters and returns only orders matching a given status. Test: `find_orders_by_status(orders, "canceled")` should return a list of **625** orders.

4. **Reflection question** (1 paragraph in a text cell): You just processed 99,441 rows using pure Python. What were the most tedious parts of this work? What would you want a tool to do automatically?

---
