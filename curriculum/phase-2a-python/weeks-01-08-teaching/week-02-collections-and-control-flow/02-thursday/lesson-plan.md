# Week 2 — Collections & Control Flow
## Thursday | Phase 2a Python | PORA Academy Cohort 7

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
# "Activ

[Full curriculum in teaching-curriculum.md]
