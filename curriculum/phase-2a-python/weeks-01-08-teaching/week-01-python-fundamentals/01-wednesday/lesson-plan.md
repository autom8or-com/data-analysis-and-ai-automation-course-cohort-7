# Week 1 — Python Fundamentals
## Phase 2a Python | PORA Academy Cohort 7

**Day:** Wednesday  
**Duration:** 2 hours  
**Week:** 1 of 8  
**AI assistance:** None this week

---

## Learning Objectives

- Set up and navigate Google Colab
- Create variables and understand Python data types (str, int, float, bool, NoneType)
- Perform arithmetic operations and understand type behaviour
- Use print() and f-strings for output

---

## Session Outline

| Time | Activity |
|------|----------|
| 0:00–0:20 | Part 1 — Colab Setup |
| 0:20–1:00 | Part 2 — Variables & Data Types |
| 1:00–1:30 | Part 3 — Strings |
| 1:30–2:00 | Part 4 — Group Exercise |

---

## Materials

- **Demo notebook:** `lecture-materials/week-01-wed-demo.ipynb`
- **Exercise notebook:** `exercises/week-01-wed-exercises.ipynb`
- **Solutions:** `solutions/week-01-wed-solutions.ipynb` *(instructor only)*

---

## Key Concepts

**Variables and types:**
- `str`, `int`, `float`, `bool`, `NoneType`
- Use `type()` to inspect
- Anchor with real Olist values (order_id, item_price, is_delivered)

**Arithmetic:**
- `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Integer division vs float division
- Profit margin formula: `(revenue - cost) / revenue * 100`

**Strings:**
- `.upper()`, `.title()`, `.lower()`, `.replace()`, `.strip()`, `len()`
- Indexing: `s[0]`, `s[-1]`, slicing: `s[:8]`
- f-strings: `f"State {state} has {orders:,} orders"`

---

## Group Exercise

Students work in groups of 10 on a shared Colab notebook using verified Olist values.  
See `exercises/week-01-wed-exercises.ipynb` for questions.

**Expected outputs:**
1. Total order value: `72.19`
2. SP state percentage: `41.98%`
3. seller_city in title case: `Campinas`
4. First 8 chars of product_id: `'4244733e'`
5. f-string: `"This order costs R$72.19 including R$13.29 freight"`

---

## Notes

- First session — expect Colab setup to take the full 20 minutes
- Emphasise: every variable, every expected output is from real Olist data
- No pandas yet — pure Python only
- Assignment assigned at end of Thursday session
