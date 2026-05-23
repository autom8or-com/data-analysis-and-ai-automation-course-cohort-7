# Week 2 — Collections & Control Flow
## Phase 2a Python | PORA Academy Cohort 7

**Day:** Thursday
**Duration:** 2 hours
**Week:** 2 of 8
**Topic:** Collections & Control Flow — Dictionaries & Conditionals

---

## Learning Objectives

- Create and manipulate dictionaries
- Use if/elif/else for business logic
- Combine loops with conditionals
- Nest dictionaries for structured data

---

## Session Plan

### Part 1 — Dictionaries (35 min)


### Part 2 — Conditionals (35 min)


### Part 3 — Group Exercise (40 min)


---

## Instructor Notes

[See teaching-curriculum.md for detailed notes and verified outputs]

---

## Group Exercise

Duration: See teaching-curriculum.md

Tasks:
- # Task 1: Create a dict mapping status → count
- # Task 2: Using a loop, print only statuses where count > 500
- # Task 3: Write a function classify_status(status) that returns:
- # Task 4: Create a dict comprehension: {status: count for ...}

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

---

## Assignment

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
