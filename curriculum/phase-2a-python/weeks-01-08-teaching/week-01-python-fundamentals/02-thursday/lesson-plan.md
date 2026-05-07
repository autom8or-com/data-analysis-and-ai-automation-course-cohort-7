# Week 1 — Python Fundamentals
## Phase 2a Python | PORA Academy Cohort 7

**Day:** Thursday  
**Duration:** 2 hours  
**Week:** 1 of 8  
**AI assistance:** None this week

---

## Learning Objectives

- Apply string methods to clean and format data
- Understand and perform type conversion (str → int, str → float, and back)
- Use string checking methods (startswith, endswith, in)
- Handle conversion errors safely with try/except

---

## Session Outline

| Time | Activity |
|------|----------|
| 0:00–0:30 | Part 1 — More String Methods |
| 0:30–1:00 | Part 2 — Type Conversion |
| 1:00–1:40 | Part 3 — Group Exercise |
| 1:40–2:00 | Weekly Assignment 1 briefing |

---

## Materials

- **Demo notebook:** `lecture-materials/week-01-thu-demo.ipynb`
- **Exercise notebook:** `exercises/week-01-thu-exercises.ipynb`
- **Solutions:** `solutions/week-01-thu-solutions.ipynb` *(instructor only)*

---

## Key Concepts

**More string methods:**
- `.split()` — splits on a character, returns a list
- `.startswith()`, `.endswith()`, `in` operator
- Chaining: `category.strip().replace("_", " ").title()`

**Type conversion:**
- `float("58.90")` → `58.9`
- `int("6")` → `6`
- `str(4)` → `"4"`
- `ValueError` on bad conversion → introduce `try/except`
- `safe_float()` pattern — foundational for data cleaning

---

## Group Exercise

Students work in groups on Olist data cleaning scenarios using verified values.  
See `exercises/week-01-thu-exercises.ipynb` for questions.

**Expected outputs:**
1. `"sao paulo"` → `"Sao Paulo"`
2. `"cama_mesa_banho"` → `"Cama Mesa Banho"`
3. `"2017-10-02 10:56:33"` → `"2017-10-02"`
4. Year extraction → `"2017"` or `2017`
5. `"120.65"` + `19.99` → `140.64`
6. `"C536379".startswith("C")` → `True`

---

## Weekly Assignment 1

Assigned end of session — due before Week 2 Wednesday.

Students submit `week1_assignment.ipynb` with:
1. Variables for a fictional Olist order
2. total_cost and is_expensive calculations
3. String operations on customer_city
4. `safe_int()` function with tests
5. Formatted f-string output

See `teaching-curriculum.md` for full spec.
