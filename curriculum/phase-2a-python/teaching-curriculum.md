# Phase 2a — Python Teaching Curriculum
## PORA Academy Cohort 7

**Duration:** 8 weeks (16 sessions)
**Format:** Wednesday & Thursday, 2 hours each session — both days Python-focused
**Class size:** 120 students in 12 groups of 10
**Platform:** Google Colab (shared cloud)
**Dataset:** Brazilian Olist E-commerce Platform (2016–2018)
**AI assistance:** None in Weeks 1–3. DeepSeek introduced from Week 4.
**Assessment:** Weekly assignments (no tests)

> **Curriculum principle:** Every code snippet, every expected output, and every exercise in this document was executed against the actual dataset before being written. No output is assumed.

---

## Dataset Reference Card
*(Uploaded to shared Google Drive at program start — students mount in every Colab notebook)*

| File | Rows | Key Columns | Used From |
|---|---|---|---|
| `olist_orders_dataset.csv` | 99,441 | order_id, customer_id, order_status, order_purchase_timestamp | Week 3 |
| `olist_customers_dataset.csv` | 99,441 | customer_id, customer_unique_id, customer_city, customer_state | Week 5 |
| `olist_order_items_dataset.csv` | 112,650 | order_id, product_id, seller_id, price, freight_value | Week 5 |
| `olist_products_dataset.csv` | 32,951 | product_id, product_category_name (has nulls + typo in column name) | Week 6 |
| `olist_order_reviews_dataset.csv` | 99,224 | order_id, review_score, review_comment_message | Week 7 |
| `olist_order_payments_dataset.csv` | 103,886 | order_id, payment_type, payment_installments, payment_value | Week 7 |
| `olist_sellers_dataset.csv` | 3,095 | seller_id, seller_city, seller_state | Week 7 |
| `product_category_name_translation.csv` | 71 | product_category_name, product_category_name_english | Week 7 |

**Business context to introduce at start of program:**
> *"Olist is a Brazilian e-commerce marketplace — similar to Jumia or Konga but in Brazil. It connects small and medium merchants to major marketplace platforms. This dataset contains 100,000 real orders placed between 2016 and 2018. We will use it to analyse order performance, customer behaviour, product categories, and delivery times — exactly what a data analyst at this company would do."*

---

## AI Assistance Protocol (Weeks 4–8)

From Week 4, students use **DeepSeek** to help write and debug code. The protocol:

1. **Understand first:** Before prompting, students must describe in plain English what they want to achieve
2. **Prompt with context:** Provide DeepSeek with the DataFrame name, relevant column names, and the specific question
3. **Validate the output:** Every output from DeepSeek must be verified against expected values. If the answer does not match the verified value in this curriculum, the code is wrong — not the curriculum.
4. **Never copy blindly:** Students must be able to explain every line of generated code

**Sample prompt template (teach students this):**
> *"I have a pandas DataFrame called `orders` with columns: order_id, customer_id, order_status, order_purchase_timestamp. How do I count the number of orders for each order_status and sort the result from highest to lowest?"*

---

## WEEK 1 — Python Fundamentals: Variables, Types & Strings
*(No AI assistance)*

### Wednesday: Variables, Data Types & Basic Operations

**Learning objectives:**
- Set up and navigate Google Colab
- Create variables and understand Python data types
- Perform arithmetic operations and understand type behaviour
- Use print() and f-strings for output

**Session outline (2 hours)**

**Part 1 — Colab Setup (20 min)**

Walk through:
1. Opening Google Colab at colab.research.google.com
2. Creating a new notebook
3. Renaming the notebook: `week1_wednesday.ipynb`
4. Understanding: Code cells vs Text cells
5. Running a cell: `Shift + Enter`
6. Adding cells: `+Code` button or `B` key

First cell every student runs:
```python
print("Hello, I am a data analyst!")
print("Welcome to PORA Academy Cohort 7")
```

**Part 2 — Variables & Data Types (40 min)**

Introduce with Olist business context — these are real values from the dataset:

```python
# A real order from the Olist dataset
order_id = "e481f51cbdc54678b7cc49136f2d6af7"
order_status = "delivered"
item_price = 58.90
freight_value = 13.29
is_delivered = True
cancelled_orders = None

# Check types
print(type(order_id))       # <class 'str'>
print(type(item_price))     # <class 'float'>
print(type(is_delivered))   # <class 'bool'>
print(type(cancelled_orders))  # <class 'NoneType'>
```

**Arithmetic operations:**
```python
# Calculate total order cost
total_cost = item_price + freight_value
print(total_cost)          # 72.19

# Profit margin calculation
revenue = 58.90
cost = 40.00
margin = (revenue - cost) / revenue * 100
print(f"Profit margin: {margin:.1f}%")   # Profit margin: 32.1%

# Integer vs float division
print(10 / 3)    # 3.3333333333333335
print(10 // 3)   # 3  (floor division)
print(10 % 3)    # 1  (remainder)
```

**Part 3 — Strings (30 min)**

```python
city = "sao paulo"

# String methods
print(city.upper())           # SAO PAULO
print(city.title())           # Sao Paulo
print(city.replace("sao", "rio"))  # rio paulo
print(len(city))              # 9
print(city.strip())           # removes leading/trailing spaces

# Indexing and slicing
order_id = "e481f51cbdc54678b7cc49136f2d6af7"
print(order_id[0])            # e
print(order_id[-1])           # 7
print(order_id[:8])           # e481f51c
print(order_id[8:16])         # bdc54678

# f-strings
state = "SP"
orders = 41746
print(f"State {state} has {orders:,} orders")
# State SP has 41,746 orders
```

**Part 4 — Group Exercise (30 min)**

Each group completes this in one shared Colab notebook:

```python
# Given these verified values from the Olist dataset:
product_id = "4244733e06e7ecb4970a6e2683c13e61"
seller_city = "campinas"
price = 58.90
freight = 13.29
review_score = 4
total_orders_brazil = 99441

# Tasks:
# 1. Calculate the total order value (price + freight)
# Expected: 72.19

# 2. What percentage of Brazil's total orders are from SP state (41,746)?
# Expected: 41.98%

# 3. Print seller_city in title case
# Expected: Campinas

# 4. Extract the first 8 characters of product_id
# Expected: '4244733e'

# 5. Create an f-string: "This order costs R$XX.XX including R$XX.XX freight"
# Expected: "This order costs R$72.19 including R$13.29 freight"
```

**Weekly Assignment (partial — completed after Thursday):**
Assigned Thursday end of session.

---

### Thursday: String Operations & Type Conversion

**Learning objectives:**
- Apply string methods to clean and format data
- Understand and perform type conversion
- Use string checking methods (startswith, endswith, in, contains)

**Session outline (2 hours)**

**Part 1 — More String Methods (30 min)**

```python
# Real data patterns from Olist
order_id = "e481f51cbdc54678b7cc49136f2d6af7"
category = "  cama_mesa_banho  "  # has extra spaces

# Cleaning
print(category.strip())           # 'cama_mesa_banho'
print(category.strip().replace("_", " "))  # 'cama mesa banho'

# split() — splitting strings into lists
date_str = "2017-10-02 10:56:33"
parts = date_str.split(" ")
print(parts)            # ['2017-10-02', '10:56:33']
date_only = parts[0]
print(date_only)        # '2017-10-02'
year = date_only.split("-")[0]
print(year)             # '2017'

# Checking content
status = "delivered"
print(status.startswith("d"))          # True
print("cancel" in status)              # False
print(status.endswith("ed"))           # True

# The C-prefix pattern (same logic as our Excel cancellation detection)
invoice_normal = "536365"
invoice_cancel = "C536379"
print(invoice_cancel.startswith("C"))   # True
print(invoice_normal.startswith("C"))   # False
```

**Part 2 — Type Conversion (30 min)**

```python
# Type conversion — common in data work
price_str = "58.90"          # came in as string from CSV
price_num = float(price_str)
print(price_num + 10)        # 68.9

qty_str = "6"
qty_num = int(qty_str)
print(qty_num * 3)           # 18

# What happens with bad conversion?
bad_value = "N/A"
# float(bad_value)  # This would raise ValueError — introduce try/except concept

# Safe conversion with default
def safe_float(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default

print(safe_float("58.90"))   # 58.9
print(safe_float("N/A"))     # 0.0

# Converting numbers to strings
score = 4
label = "Score: " + str(score)
print(label)                  # Score: 4
```

**Part 3 — Group Exercise (40 min)**

```python
# Olist data cleaning scenarios — all values verified from actual data

# 1. The city "sao paulo" needs to be "Sao Paulo"
city = "sao paulo"
# Expected: "Sao Paulo"

# 2. Category "cama_mesa_banho" needs to become "Cama Mesa Banho"
category = "cama_mesa_banho"
# Expected: "Cama Mesa Banho"

# 3. Order timestamp "2017-10-02 10:56:33" — extract just the date part
timestamp = "2017-10-02 10:56:33"
# Expected: "2017-10-02"

# 4. Extract the year from "2017-10-02"
# Expected: "2017" (as string) or 2017 (as int)

# 5. Given price_str = "120.65", convert to float and add 19.99 freight
price_str = "120.65"
# Expected: 140.64

# 6. Check if "C536379" is a cancellation (starts with "C")
invoice = "C536379"
# Expected: True
```

**Weekly Assignment 1:**

Submit a Colab notebook (`week1_assignment.ipynb`) with:

1. Create variables for a fictional Olist order: `order_id`, `customer_city`, `item_price`, `freight_value`, `review_score`, `order_status`. Use realistic values.

2. Calculate:
   - `total_cost = item_price + freight_value`
   - `is_expensive = total_cost > 200` (boolean)

3. Using string methods on your `customer_city`:
   - Print it in UPPER CASE
   - Print it in Title Case
   - Print its length
   - Check if it contains "paulo"

4. Write a safe conversion function `safe_int(value, default=0)` that converts a string to int and returns `default` if conversion fails. Test with `"42"`, `"hello"`, and `"3.5"`.

5. Write an f-string that outputs:
   `"Order [order_id first 8 chars]... from [city title case] — Status: [status] — Total: R$[total_cost]"`

---

## WEEK 2 — Collections & Control Flow
*(No AI assistance)*

### Wednesday: Lists, Tuples & Loops

**Learning objectives:**
- Create and manipulate lists
- Use for loops and range()
- Apply list comprehensions for simple transformations
- Understand tuples and when to use them

**Session outline (2 hours)**

**Part 1 — Lists (35 min)**

```python
# Real data from Olist — 8 order statuses and their counts
statuses = ["delivered", "shipped", "canceled", "unavailable",
            "invoiced", "processing", "created", "approved"]
counts   = [96478, 1107, 625, 609, 314, 301, 5, 2]

print(len(statuses))        # 8
print(statuses[0])          # delivered
print(statuses[-1])         # approved
print(statuses[:3])         # ['delivered', 'shipped', 'canceled']
print(sorted(statuses))     # alphabetical order

# Modifying lists
top_states = ["SP", "RJ", "MG"]
top_states.append("RS")
print(top_states)           # ['SP', 'RJ', 'MG', 'RS']
top_states.insert(0, "BA")
print(top_states)           # ['BA', 'SP', 'RJ', 'MG', 'RS']
top_states.remove("BA")
print(top_states)           # ['SP', 'RJ', 'MG', 'RS']

# Useful list operations
scores = [5, 4, 1, 5, 3, 2, 5, 4, 5, 1]
print(max(scores))          # 5
print(min(scores))          # 1
print(sum(scores))          # 35
print(sum(scores)/len(scores))  # 3.5
print(scores.count(5))      # 4
```

**Part 2 — For Loops (35 min)**

```python
# Loop through statuses with counts
statuses = ["delivered", "shipped", "canceled", "unavailable", "invoiced"]
counts   = [96478, 1107, 625, 609, 314]
total = sum(counts)

for status, count in zip(statuses, counts):
    pct = count / total * 100
    print(f"{status}: {count:,} orders ({pct:.1f}%)")

# Expected output:
# delivered: 96,478 orders (97.0%)
# shipped: 1,107 orders (1.1%)
# canceled: 625 orders (0.6%)
# unavailable: 609 orders (0.6%)
# invoiced: 314 orders (0.3%)

# range() loops
print("\nOrder scores 1-5:")
for score in range(1, 6):
    print(f"  Score {score}")

# Loop with index
cities = ["sao paulo", "rio de janeiro", "belo horizonte"]
for i, city in enumerate(cities):
    print(f"{i+1}. {city.title()}")
# 1. Sao Paulo
# 2. Rio De Janeiro
# 3. Belo Horizonte
```

**Part 3 — List Comprehensions (20 min)**

```python
# Transform a list in one line
scores = [5, 4, 1, 5, 3, 2, 5, 4, 5, 1]

# Standard loop version
positives = []
for s in scores:
    if s >= 4:
        positives.append(s)
print(positives)   # [5, 4, 5, 5, 4, 5]

# List comprehension version (same result)
positives = [s for s in scores if s >= 4]
print(positives)   # [5, 4, 5, 5, 4, 5]

# Transform values
labels = ["Positive" if s >= 4 else "Neutral" if s == 3 else "Negative"
          for s in scores]
print(labels)
# ['Positive', 'Positive', 'Negative', 'Positive', 'Neutral',
#  'Negative', 'Positive', 'Positive', 'Positive', 'Negative']

# Verified count
print(labels.count("Positive"))   # 6
```

**Part 4 — Group Exercise (30 min)**

```python
# Verified data from Olist
payment_types = ["credit_card", "boleto", "voucher", "debit_card", "not_defined"]
payment_counts = [76795, 19784, 5775, 1529, 3]

# Tasks:
# 1. Print total payments: sum(payment_counts) → Expected: 103,886
# 2. Using a for loop with zip(), print each type and its % of total
#    Expected: credit_card = 73.9%, boleto = 19.0%, etc.
# 3. Using a list comprehension, create a list of only types with count > 1000
#    Expected: ['credit_card', 'boleto', 'voucher', 'debit_card']
# 4. Create a list comprehension that converts all type names to UPPER CASE
# 5. What is the average payment count per type?
#    Expected: 103886 / 5 = 20,777.2
```

---

### Thursday: Dictionaries & Conditionals

**Learning objectives:**
- Create and manipulate dictionaries
- Use if/elif/else for business logic
- Combine loops with conditionals
- Nest dictionaries for structured data

**Session outline (2 hours)**

**Part 1 — Dictionaries (35 min)**

```python
# Represent an Olist order as a dictionary
order = {
    "order_id": "e481f51cbdc54678b7cc49136f2d6af7",
    "status": "delivered",
    "price": 58.90,
    "freight": 13.29,
    "state": "SP",
    "review_score": 4
}

# Access values
print(order["status"])               # delivered
print(order.get("review_score"))     # 4
print(order.get("seller", "unknown"))  # unknown (key doesn't exist → default)

# Modify
order["total"] = order["price"] + order["freight"]
print(order["total"])                # 72.19

# Loop through dict
for key, value in order.items():
    print(f"{key}: {value}")

# Keys and values as lists
print(list(order.keys()))
print(list(order.values()))

# Dict of dicts — state order summary (verified counts)
state_summary = {
    "SP": {"orders": 41746, "revenue": 5202955.05},
    "RJ": {"orders": 12852, "revenue": 1824092.67},
    "MG": {"orders": 11635, "revenue": 1585308.03}
}
print(state_summary["SP"]["revenue"])      # 5202955.05
print(state_summary["RJ"]["orders"])       # 12852
```

**Part 2 — Conditionals (35 min)**

```python
# Business classification logic — same patterns we'll use in pandas later

def classify_delivery(days):
    """Classify delivery speed based on number of days."""
    if days is None:
        return "Unknown"
    elif days <= 7:
        return "Fast"
    elif days <= 14:
        return "Normal"
    elif days <= 30:
        return "Slow"
    else:
        return "Very Slow"

# Test with real delivery time stats from the dataset
# Min: 0 days, Median: 10 days, Mean: 12.1 days, Max: 209 days
for days in [0, 5, 10, 20, 50, None]:
    print(f"{days} days → {classify_delivery(days)}")

# 0 days → Fast
# 5 days → Fast
# 10 days → Normal
# 20 days → Slow
# 50 days → Very Slow
# None days → Unknown

def classify_order_value(price):
    """Classify order by price tier."""
    if price >= 500:
        return "Premium"
    elif price >= 100:
        return "Standard"
    else:
        return "Economy"

# Verified: Avg price = R$120.65, Max = R$6,735.00
for p in [58.90, 120.65, 500.00, 6735.00]:
    print(f"R${p:.2f} → {classify_order_value(p)}")
```

**Part 3 — Group Exercise (40 min)**

```python
# Build a status summary dict from scratch

statuses = ["delivered", "shipped", "canceled", "unavailable",
            "invoiced", "processing", "created", "approved"]
counts = [96478, 1107, 625, 609, 314, 301, 5, 2]

# Task 1: Create a dict mapping status → count
# Expected: {"delivered": 96478, "shipped": 1107, ...}

# Task 2: Using a loop, print only statuses where count > 500
# Expected: delivered (96478), shipped (1107), canceled (625), unavailable (609)

# Task 3: Write a function classify_status(status) that returns:
# "Active" if status in ["delivered", "shipped", "invoiced", "processing"]
# "Problem" if status in ["canceled", "unavailable"]
# "Other" otherwise
# Test with all 8 statuses

# Task 4: Create a dict comprehension: {status: count for ...}
# Then add a "pct" to each — build a nested dict:
# {"delivered": {"count": 96478, "pct": 97.0}, ...}
```

**Weekly Assignment 2:**

Submit `week2_assignment.ipynb`:

1. Create a dictionary representing 3 Olist orders (make up order_ids but use realistic prices from R$20–R$500). Include: order_id, city, state, price, freight, review_score.

2. Write a function `order_report(order_dict)` that:
   - Calculates total cost (price + freight)
   - Returns a formatted string: `"Order from [city]: R$[total] — [Fast/Normal/Slow delivery classification based on review score proxy]"`

3. Using a list of 10 review scores `[5, 4, 1, 5, 3, 2, 5, 4, 5, 1]`:
   - Count positives (≥4), neutrals (=3), negatives (≤2) using a loop
   - Then do the same with a list comprehension + `.count()`
   - Verify both methods give the same answer *(Expected: positive=6, neutral=1, negative=3)*

4. Write a function `top_states(state_dict, n)` that takes a dict of `{state: order_count}` and returns the top `n` states sorted by count descending. Test with:
   ```python
   data = {"SP": 41746, "RJ": 12852, "MG": 11635, "RS": 5466, "PR": 5045}
   ```
   `top_states(data, 3)` should return `[("SP", 41746), ("RJ", 12852), ("MG", 11635)]`

---

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

## WEEK 8 — Visualisation & Putting It Together
*(DeepSeek assisted)*

### Wednesday: matplotlib & seaborn Basics

**Learning objectives:**
- Create bar charts, line charts, and histograms with matplotlib
- Format charts (title, labels, figsize, colours)
- Use seaborn for cleaner charts
- Save charts to file

> **Note:** Every chart built today will be embedded inside a Streamlit dashboard on Thursday. matplotlib figures are passed directly to `st.pyplot()` — so the skills are directly connected.

**Session outline (2 hours)**

**Part 1 — matplotlib Foundations (30 min)**

```python
import pandas as pd
import matplotlib.pyplot as plt

orders = pd.read_csv('olist_orders_dataset.csv')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')

# Monthly orders 2017 (verified)
orders_2017 = orders[orders['order_purchase_timestamp'].dt.year == 2017]
monthly = orders_2017.groupby('month')['order_id'].count()

# Line chart
plt.figure(figsize=(12, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2, color='steelblue')
plt.title('Monthly Orders — Olist 2017', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# November 2017 spike to 7,544 should be visually prominent (Black Friday)

# Bar chart — order status
status = orders['order_status'].value_counts().head(5)
plt.figure(figsize=(8, 4))
plt.bar(status.index, status.values, color=['#2ecc71','#3498db','#e74c3c','#f39c12','#9b59b6'])
plt.title('Order Status Distribution')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
```

**Part 2 — seaborn (30 min)**

```python
import seaborn as sns

# Review score distribution
reviews = pd.read_csv('olist_order_reviews_dataset.csv')

plt.figure(figsize=(8, 4))
sns.countplot(data=reviews, x='review_score', palette='RdYlGn')
plt.title('Review Score Distribution — Olist')
plt.xlabel('Review Score')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
# Expected visual: 5-star dominates (57,328), 1-star is second (11,424)

# Payment type pie chart
payments = pd.read_csv('olist_order_payments_dataset.csv')
pay_counts = payments['payment_type'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(pay_counts.values, labels=pay_counts.index, autopct='%1.1f%%',
        colors=['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6'])
plt.title('Payment Method Distribution')
plt.show()
# credit_card: 73.9%, boleto: 19.0%, voucher: 5.6%, debit_card: 1.5%
```

**Part 3 — Group Exercise (40 min)**

```python
# Each group builds 3 charts using verified data:

# Chart 1: Monthly order volume for 2017 (line chart)
# Peak should show: November 2017 = 7,544 orders

# Chart 2: Top 10 states by total orders (horizontal bar chart)
# SP should be far ahead at 41,746

# Chart 3: Review score distribution (bar chart)
# Scores 1-5, count for each
# Expected: [11424, 3151, 8179, 19142, 57328]
```

---

### Thursday: Introduction to Streamlit

**Learning objectives:**
- Understand what Streamlit is and why it matters for data analysts
- Build a working multi-page dashboard using Streamlit
- Use core Streamlit components: `st.title`, `st.metric`, `st.selectbox`, `st.columns`, `st.pyplot`, `st.dataframe`, `@st.cache_data`
- Run a Streamlit app from Google Colab using pyngrok
- Know the Streamlit Community Cloud deployment workflow (used in Phase 2c Capstone)

> **Why Streamlit now:** The Phase 2c Capstone project requires each group to build and deploy a Streamlit dashboard combining Python + SQL. This session is your introduction. By end of Capstone, you will build the full version.

---

**Session outline (2 hours)**

**Part 1 — What is Streamlit? (20 min)**

Streamlit turns a Python script into an interactive web app. You do not need to know HTML, CSS, or JavaScript. You write Python; Streamlit handles the browser.

Core concept: every time a user interacts with a widget (selectbox, slider, button), the entire Python script re-runs from top to bottom. This is the Streamlit execution model — understand it before writing your first app.

**Install in Colab:**
```python
!pip install streamlit pyngrok -q
```

**How Streamlit apps work in Colab:**
Streamlit apps cannot be viewed directly inside a Colab notebook. You need to:
1. Write the app code to a `.py` file using `%%writefile`
2. Start the Streamlit server in the background
3. Use `pyngrok` to create a public URL that tunnels to the running server

```python
# Step 1: Write app to file
%%writefile app.py
import streamlit as st
st.title("Hello from Streamlit!")
st.write("This is my first app.")
```

```python
# Step 2: Start Streamlit in background + create tunnel
import subprocess
import time
from pyngrok import ngrok

# You need a free account at ngrok.com to get an auth token
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Start streamlit in background
process = subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])
time.sleep(3)

# Create public URL
public_url = ngrok.connect(8501)
print(f"App is live at: {public_url}")
```

> **Instructor note:** Have students create a free ngrok account before this session. The auth token setup takes 2 minutes. Alternatively, students can run the app locally on their laptop if Python is installed: `streamlit run app.py` opens it at `http://localhost:8501` automatically.

---

**Part 2 — Core Components (40 min)**

Build each component live, run and observe:

```python
%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_DIR = "/content/drive/MyDrive/cohort7/datasets/olist"

st.set_page_config(page_title="Olist Dashboard", layout="wide")

# --- Title and description ---
st.title("Olist E-Commerce Dashboard")
st.markdown("**Brazilian marketplace orders — 2016 to 2018**")
st.divider()

# --- @st.cache_data: load once, reuse ---
# Without caching, the CSV loads every time a widget changes (slow).
# With @st.cache_data, it loads once and stays in memory.
@st.cache_data
def load_data():
    orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
    customers = pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))
    payments = pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders["year"] = orders["order_purchase_timestamp"].dt.year
    orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return orders, customers, payments

orders, customers, payments = load_data()

# --- Sidebar: selectbox filter ---
st.sidebar.header("Filters")
year_options = sorted(orders["year"].dropna().unique().astype(int).tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options, index=1)

# Filter data based on selection
filtered = orders[orders["year"] == selected_year]

# --- KPI Row: st.metric in st.columns ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{len(filtered):,}")
col2.metric("Delivered", f"{(filtered['order_status'] == 'delivered').sum():,}")
col3.metric("Canceled", f"{(filtered['order_status'] == 'canceled').sum():,}")
col4.metric("Delivered %", f"{(filtered['order_status'] == 'delivered').mean()*100:.1f}%")

# --- Chart 1: Monthly orders (st.pyplot) ---
st.subheader(f"Monthly Orders — {selected_year}")

monthly = filtered.groupby("month")["order_id"].count().reset_index()
monthly.columns = ["month", "orders"]

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly["month"], monthly["orders"], marker="o", color="steelblue", linewidth=2)
ax1.set_xlabel("Month")
ax1.set_ylabel("Orders")
ax1.tick_params(axis="x", rotation=45)
plt.tight_layout()
st.pyplot(fig1)
plt.close()

# --- Two-column layout: state chart + payment chart ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 States by Orders")
    merged = filtered.merge(customers[["customer_id", "customer_state"]], on="customer_id")
    state_counts = merged["customer_state"].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.barh(state_counts.index[::-1], state_counts.values[::-1], color="coral")
    ax2.set_xlabel("Orders")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

with col_right:
    st.subheader("Payment Method Breakdown")
    pay_counts = payments["payment_type"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
            colors=["#3498db","#e74c3c","#2ecc71","#f39c12","#9b59b6"])
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# --- Raw data toggle: st.dataframe ---
if st.checkbox("Show raw data sample"):
    st.dataframe(filtered.head(20))
```

**Verify these KPIs when selecting 2017:**
| KPI | Expected value |
|---|---|
| Total Orders | 45,101 |
| Delivered | 43,428 |
| Canceled | 265 |
| Delivered % | 96.3% |

**Verify when selecting 2018:**
| KPI | Expected value |
|---|---|
| Total Orders | 54,011 |
| Delivered | 52,783 |
| Canceled | 334 |
| Delivered % | 97.7% |

---

**Part 3 — Group Exercise (40 min)**

Each group extends the app above by adding one new section. Assign sections:

- **Group A:** Add a delivery time histogram. Load `order_delivered_customer_date`, compute `delivery_days`, plot a histogram. Expected: mean = 12.1 days, median = 10.0 days.

- **Group B:** Add a review score bar chart. Load `olist_order_reviews_dataset.csv`, plot `review_score` counts. Expected: 5-star = 57,328, 1-star = 11,424.

- **Group C:** Add a top-10 revenue categories chart. Requires merging order_items + products + translation. Expected: health_beauty = R$1,258,681.34.

- **Group D (challenge):** Add a `st.selectbox` for state selection. Filter all charts by the selected state. Verify SP total orders (2017) = 17,760.

---

**Part 4 — Deployment to Streamlit Community Cloud (20 min — instructor demo)**

> This is what you will use for Phase 2c Capstone deployment. Watch and follow along.

1. Push `app.py` to a public GitHub repository
2. Go to `share.streamlit.io` → Sign in with GitHub
3. Click **New app** → Select repo, branch, and file
4. Click **Deploy** — the app is live at a public URL in ~2 minutes (free)

The Phase 2c Capstone will require each group to deploy their Streamlit dashboard this way. No ngrok needed — the production version runs on Streamlit Community Cloud.

---

**Weekly Assignment 8 (Phase 2a Final — Streamlit App):**

This is the final Python assignment. Build a Streamlit app (`olist_app.py`) that:

1. **Loads and caches** orders, customers, payments, and order_reviews using `@st.cache_data`
2. **Has a sidebar** with a year selector (`st.selectbox`) — 2017 or 2018
3. **Shows 4 KPI metrics** in a row using `st.columns` and `st.metric`:
   - Total Orders, Delivered %, Avg Payment Value, Most Common Payment Type
4. **Shows 3 charts** using `st.pyplot`:
   - Monthly orders line chart (for selected year)
   - Review score bar chart (all years — not filtered)
   - Top 10 states by orders horizontal bar chart (filtered by year)
5. **Has a data table toggle** using `st.checkbox("Show raw orders sample")`

**Verified outputs that must appear in the app:**

| Check | Expected |
|---|---|
| 2017 total orders | 45,101 |
| 2018 total orders | 54,011 |
| 2017 delivered % | 96.3% |
| 2017 peak month | November 2017 = 7,544 orders |
| Review score 5 count | 57,328 |
| Review score 1 count | 11,424 |
| Overall avg payment | R$154.10 |
| Top state (2017) | SP = 17,760 orders |

---

## Assessment Framework

| Week | Assignment Focus | Key Verified Output |
|---|---|---|
| 1 | Variables, strings, type conversion | calculate_total(58.90, 13.29) = 72.19 |
| 2 | Lists, dicts, loops, conditionals | Status loop outputs match 97.0% delivered |
| 3 | Functions, CSV reading | load_csv returns 99,441 rows |
| 4 | Pandas basics, filtering | items.shape = (112650, 7) |
| 5 | GroupBy, aggregation, datetime | SP state = 41,746 orders |
| 6 | Nulls, datetime, string cleaning | delivery_days mean = 12.1 |
| 7 | Merging, multi-table analysis | Full merge shape = (112650, 20) |
| 8 | Visualisation + Streamlit dashboard | 2017 orders=45,101 | 2017 peak=7,544 | Delivered%=96.3% |

---

## Instructor Notes

### DeepSeek Usage Guidelines (Weeks 4–8)

**Encourage students to:**
- Describe their intent in plain English before prompting
- Include column names and DataFrame names in prompts
- Verify every output against the expected values in this document
- Re-prompt when output doesn't match verified values

**Red flags to watch for:**
- Students who cannot explain the code DeepSeek returned
- Students who skip verification and assume the output is correct
- Groups that stop attempting independently and jump straight to DeepSeek

**The 5-minute rule:** Every exercise must be attempted independently for 5 minutes before DeepSeek is used.

### Common Python Errors to Pre-Empt

1. **KeyError on merge:** Happens when the join key column name doesn't match exactly (e.g., `customer_id` vs `CustomerID`). Always check `.columns` before merging.
2. **TypeError on groupby sum:** If a column contains nulls and non-numeric types mixed, sum will fail. Use `numeric_only=True` or clean first.
3. **datetime parsing fails:** All date columns in Olist load as `object`. Always apply `pd.to_datetime()` with `errors='coerce'`.
4. **SettingWithCopyWarning:** When modifying a filtered subset, always use `.copy()` first.
5. **Product column typo:** `product_name_lenght` (missing 'g') — students who don't notice will get KeyErrors when trying to access `product_name_length`.

### Dataset Notes

- **September & October 2018** have very few orders (16 and 4) — the dataset ends October 17, 2018. Students will notice this in time series and should note it as incomplete data.
- **2016** has only 329 orders — Olist launched late 2016. Always filter to 2017+ for trend analysis.
- **1,603 items** have no matching product in the products table (left join gives nulls) — always use `how='left'` when joining items → products.
