# Week 1 — Python Fundamentals
## Phase 2a Python | PORA Academy Cohort 7

**Day:** Thursday
**Duration:** 2 hours
**Week:** 1 of 8
**Topic:** Python Fundamentals — String Operations & Type Conversion

---

## Learning Objectives

- Apply string methods to clean and format data
- Understand and perform type conversion
- Use string checking methods (startswith, endswith, in, contains)

---

## Session Plan

### Part 1 — More String Methods (30 min)


### Part 2 — Type Conversion (30 min)


### Part 3 — Group Exercise (40 min)


---

## Instructor Notes

[See teaching-curriculum.md for detailed notes and verified outputs]

---

## Group Exercise

Duration: See teaching-curriculum.md

Tasks:
- # 1. The city "sao paulo" needs to be "Sao Paulo"
- # 2. Category "cama_mesa_banho" needs to become "Cama Mesa Banho"
- # 3. Order timestamp "2017-10-02 10:56:33" — extract just the date part
- # 4. Extract the year from "2017-10-02"
- # 5. Given price_str = "120.65", convert to float and add 19.99 freight
- # 6. Check if "C536379" is a cancellation (starts with "C")

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

---

## Assignment

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
