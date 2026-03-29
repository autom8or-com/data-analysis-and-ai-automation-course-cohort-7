# Week 03 — Thursday: TRIM, Data Cleaning & Text Functions
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 03 of 6
**Session:** Thursday
**Topic:** TRIM, Data Cleaning & Text Functions

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-03-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-03-thu-exercises.xlsx`
- [ ] Weekly assignment distributed or screen-shared at end of session
- [ ] Projector / screen sharing ready

---

## Learning Objectives

By the end of this session, students will be able to:

1. Use TRIM to remove extra spaces from text data and explain why this matters for lookups
2. Apply PROPER, UPPER, LOWER, LEN, and SUBSTITUTE for text standardisation
3. Remove duplicates correctly (always on a copy, never on raw data)

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap Wednesday: SUMIFS, AVERAGEIF, IF | Quick-fire Q&A |
| 0:10 – 0:25 | Part 1 — Why text cleaning matters (COUNTIF demo) | Invisible space gotcha |
| 0:25 – 0:55 | Part 2 — TRIM, PROPER, UPPER, LOWER, LEN | Build Cleaned Data sheet |
| 0:55 – 1:20 | Part 3 — LEN and SUBSTITUTE | Character counts + text replacement |
| 1:20 – 1:40 | Part 4 — Removing Duplicates | Unique InvoiceNo / CustomerID |
| 1:40 – 2:00 | Group Exercise + debrief + assignment intro | |

---

## Concepts & Verified Outputs

### Concept 1 — Why Text Cleaning Matters

Live demo — run these two formulas and compare results:
```
=COUNTIF(C:C,"WHITE HANGING HEART T-LIGHT HOLDER")    → gets a count
=COUNTIF(C:C," WHITE HANGING HEART T-LIGHT HOLDER")   → returns 0
```
*"Same product name, different results — because of one invisible space."*

**Full dataset fact:** 113,452 Description values have leading or trailing spaces.

---

### Concept 2 — TRIM

**Syntax:** `=TRIM(text)` — removes leading, trailing, and excess internal spaces.

Create a new sheet `Cleaned Data`. In column A:
```
=TRIM('Raw Data'!C2)
```

**LEN comparison (demonstrate in a blank cell):**
```
=LEN("  WHITE METAL LANTERN  ")         → 23
=LEN(TRIM("  WHITE METAL LANTERN  "))   → 19
```

**Other text case functions (add as extra columns):**
```
=PROPER('Raw Data'!C2)   → "White Metal Lantern"
=UPPER('Raw Data'!C2)    → "WHITE METAL LANTERN"
=LOWER('Raw Data'!C2)    → "white metal lantern"
```

---

### Concept 3 — LEN and SUBSTITUTE

**LEN:** Count characters — useful for finding unusually short/long product names.
```
=LEN([@Description])
```

**SUBSTITUTE:** Replace specific text within a string.
```
=SUBSTITUTE([@Description],"HEART","❤")        ← fun demo
=SUBSTITUTE([@StockCode]," ","")               ← practical: clean spaces from codes
=SUBSTITUTE([@Description],"HOLDER","STAND")   ← rename product line
```

Teaching point: SUBSTITUTE is **case-sensitive**. "HOLDER" ≠ "holder".

---

### Concept 4 — Removing Duplicates

**Important rule: NEVER remove duplicates on the raw data sheet. Always copy first.**

Demo steps:
1. Copy the InvoiceNo column (A) to a blank area
2. `Data → Remove Duplicates`
3. Count remaining rows

**Full dataset verified:**
- Unique InvoiceNo values: **25,900**
- Unique CustomerID values: **4,372**

*"541,909 rows but only 25,900 invoices — confirms many invoices contain multiple line items."*

---

## Group Exercise

**Questions (20 min):**

1. Apply TRIM to the Description column in a helper column. Use LEN to compare original and trimmed lengths for 5 rows. Find at least 3 rows where TRIM makes a difference.

2. Using SUBSTITUTE, replace all occurrences of "HOLDER" with "STAND" in the Description column. How many descriptions contain the word "HOLDER"?
   *(Hint: `=COUNTIF(C:C,"*HOLDER*")`)*

3. How many unique `StockCode` values exist in the 1,000-row sample?
   *(Full dataset: 4,070 unique StockCodes)*

4. Apply PROPER to the Country column. Does it change anything for "EIRE" vs "United Kingdom"?

**Debrief points:**
- EIRE → "Eire" (changed), United Kingdom → "United Kingdom" (unchanged — already title case)
- SUBSTITUTE is case-sensitive; COUNTIF wildcards are not
- Always work on a copy before removing duplicates

---

## Weekly Assignment

*Set at the end of this session — students complete before next Wednesday.*

1. Create a column `CleanDescription` that applies both TRIM and PROPER to the Description column. Write the combined formula.
   *(Formula: `=PROPER(TRIM([@Description]))`)*

2. Using SUMIFS, calculate total revenue for transactions where the Description contains "CANDLE" (use wildcard: `"*CANDLE*"`). Write the formula and result.

3. Create an `OrderType` column using `IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")`. Then use COUNTIFS to count how many **UK** transactions are Cancellations.
   *(Formula: `=COUNTIFS(H:H,"United Kingdom",J:J,"Cancellation")`)*

4. What is the average UnitPrice for transactions where the Description contains "CHRISTMAS"? Use AVERAGEIF with a wildcard.
   *(Formula: `=AVERAGEIF(C:C,"*CHRISTMAS*",F:F)`)*

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-03-thu-demo.xlsx` | Instructor demo workbook — end-state Cleaned Data sheet with all text formulas |
| `exercises/week-03-thu-exercises.xlsx` | Distributed to students — blank answer cells in Formula Workspace |
| `solutions/week-03-thu-solutions.xlsx` | Instructor reference — all formulas filled including assignment answers |

---

## Instructor Notes

- **TRIM doesn't touch single internal spaces:** `"WHITE METAL LANTERN"` has single spaces between words — TRIM leaves those. It only removes leading, trailing, and consecutive internal spaces.
- **Always work on a copy:** Stress this every time before Remove Duplicates. Students who delete from raw data will lose data they can't recover easily.
- **SUBSTITUTE is case-sensitive:** Test with "HOLDER" vs "holder" live — show the difference.
- **COUNTIF wildcards are NOT case-sensitive:** `"*HOLDER*"` matches "holder", "HOLDER", "Holder" — good contrast to teach alongside SUBSTITUTE.
- **Assignment Q2 wildcard in SUMIFS:** `=SUMIFS(I:I,C:C,"*CANDLE*")` — remind students that criteria range C and sum range I must cover the same rows.
