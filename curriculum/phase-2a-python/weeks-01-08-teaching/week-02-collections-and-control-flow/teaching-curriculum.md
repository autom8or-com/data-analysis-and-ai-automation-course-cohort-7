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
