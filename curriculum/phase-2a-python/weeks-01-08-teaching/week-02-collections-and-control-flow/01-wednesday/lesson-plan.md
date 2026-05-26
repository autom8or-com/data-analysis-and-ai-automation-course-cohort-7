# Week 2 — Collections & Control Flow
## Wednesday | Phase 2a Python | PORA Academy Cohort 7

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
payment_counts = 

[Full curriculum in teaching-curriculum.md]
