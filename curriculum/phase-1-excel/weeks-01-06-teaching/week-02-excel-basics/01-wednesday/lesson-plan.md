# Week 02 — Wednesday: Core Formulas (SUM, AVERAGE, COUNT, MAX, MIN)
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 02 of 6
**Session:** Wednesday
**Topic:** Core Formulas — SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, SUMPRODUCT

---

## Pre-Session Checklist

- [ ] Dataset loaded: `data.csv` from `teaching-data.zip` (UCI Online Retail, 541,909 rows)
- [ ] Students have completed Week 1 — data should already be imported as an Excel file
- [ ] Demo workbook open: `lecture-materials/week-02-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-02-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready

---

## Learning Objectives

By the end of this session, students will be able to:

1. Apply SUM, AVERAGE, COUNT, COUNTA, MAX, and MIN to real business data
2. Understand the difference between COUNT (numeric only) and COUNTA (all non-blank)
3. Use SUMPRODUCT to calculate revenue across two columns
4. Build a business summary statistics table from scratch

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap of Week 1 | Quick recall — what is the dataset, what are the 8 columns? |
| 0:10 – 0:30 | Concept 1 — Formula syntax fundamentals | =FUNCTION(range), column refs, fill handle |
| 0:30 – 1:10 | Concept 2 — Building the Summary Stats table | SUM, AVERAGE, COUNT, COUNTA, MAX, MIN live |
| 1:10 – 1:25 | Concept 3 — SUMPRODUCT for revenue | Multiply two columns and sum in one step |
| 1:25 – 1:55 | Group exercise | Groups build table independently and verify |
| 1:55 – 2:00 | Debrief & close | Confirm answers, preview Thursday |

---

## Concept 1 — Formula Syntax Fundamentals (20 min)

**What to demonstrate:**

- Formula structure: `=FUNCTION(range)` — the `=` is mandatory
- Two ways to reference a column:
  - Full column: `D:D` — safe when new rows are added, slightly slower
  - Fixed range: `D2:D541910` — exact, faster, breaks if data grows
- Recommendation for this course: use full column references on large datasets
- Formula bar shows the formula; cell shows the result
- Copying formulas: `Ctrl+C` / `Ctrl+V` and the fill handle (bottom-right corner drag)
- Common error: `#VALUE!` when mixing text and numbers in a numeric function

**Expected output / verified value:** No output — concept only.

**Common mistakes to watch for:**
- Students typing the formula without the `=` sign — cell displays text, not a result
- Students selecting column D header instead of `D:D` in the formula — Excel may error

---

## Concept 2 — Building the Summary Stats Table (40 min)

**What to demonstrate:**

Create a new sheet called `Summary Stats` (right-click tab → Insert Sheet). Build this table live, one formula at a time:

| Metric | Formula | Verified Answer |
|---|---|---|
| Total rows of data | `=COUNTA(A:A)-1` | **541,909** |
| Total Quantity ordered | `=SUM(D:D)` | **5,176,450** |
| Average UnitPrice | `=AVERAGE(F:F)` | **£4.61** |
| Average Quantity per row | `=AVERAGE(D:D)` | **9.55** |
| Highest UnitPrice | `=MAX(F:F)` | **£38,970.00** |
| Lowest UnitPrice | `=MIN(F:F)` | **£-11,062.06** |
| Rows with a CustomerID | `=COUNT(G:G)` | **406,829** |
| Rows without CustomerID | `=COUNTA(A:A)-1-COUNT(G:G)` | **135,080** |

**Key teaching moment — COUNT vs COUNTA:**
Ask: *"Why does `COUNT(G:G)` return 406,829 instead of 541,909?"*

Answer: `COUNT` only counts **numeric** values. Blank cells are ignored. This surfaces the CustomerID missing data problem naturally.

`COUNTA` counts **any non-blank cell** — text, numbers, dates.

**Expected output / verified values:** See table above.

**Common mistakes to watch for:**
- Students using `COUNT(A:A)` for total rows — InvoiceNo is text, so COUNT returns 0. Must use `COUNTA`.
- `MIN(F:F)` returning 0 instead of negative — students may have filters still active from Week 1. Clear all filters first.

---

## Concept 3 — SUMPRODUCT for Revenue (15 min)

**What to demonstrate:**

Revenue is not a column in this dataset — it must be calculated:

> `Revenue = Quantity × UnitPrice`

Introduce `=SUMPRODUCT(D2:D541910, F2:F541910)` as the way to multiply two columns element-by-element and sum the result in one formula.

Add this row to the Summary Stats table:

| Metric | Formula | Verified Answer |
|---|---|---|
| Total Revenue (all rows) | `=SUMPRODUCT(D2:D541910,F2:F541910)` | **£9,747,747.93** |

**Discussion point:** *"This includes cancellations and returns — is this the true revenue? We will learn to filter this properly in Weeks 3 and 5."*

**Why SUMPRODUCT uses a fixed range:** Full column references cause SUMPRODUCT to be very slow on large files. Use `D2:D541910` here.

**Expected output / verified value:** **£9,747,747.93**

**Common mistakes to watch for:**
- Using `D:D, F:F` in SUMPRODUCT — much slower; avoid.
- Mismatched ranges (e.g. `D2:D541910` and `F1:F541909`) — returns `#VALUE!`.

---

## Group Exercise (30 min)

Open `exercises/week-02-wed-exercises.xlsx` → `Instructions` sheet.

Each group builds the Summary Stats table independently on the `Summary Stats Workspace` sheet, then verifies their answers.

**Questions:**

1. What is the total Quantity ordered across all rows?
   *(Full dataset: 5,176,450)*
2. What is the average UnitPrice across all rows?
   *(Full dataset: £4.61)*
3. What is the difference between `COUNT(G:G)` and `COUNTA(A:A)-1`? What does that difference represent?
   *(Full dataset: 135,080 — rows with no CustomerID)*
4. What is the highest UnitPrice in the dataset?
   *(Full dataset: £38,970.00)*
5. Create a `Revenue` column in column I (header: `Revenue`) with the formula `=D2*F2`. What is the value for row 2?
   *(Expected: £15.30 — Quantity=6, UnitPrice=£2.55)*

**Debrief:** Groups call out answers. Instructor confirms using verified values above.

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-02-wed-demo.xlsx` | Instructor demo workbook — open on screen during teaching |
| `exercises/week-02-wed-exercises.xlsx` | Distributed to students at exercise time |
| `solutions/week-02-wed-solutions.xlsx` | Instructor reference — do not share before exercise is complete |

---

## Assignment

> *Assignment is set at the end of Thursday's session — see Thursday lesson plan.*

---

## Instructor Notes

- Pace slowly on the COUNT vs COUNTA distinction — this is the most common source of confusion and is foundational for later weeks.
- When building the Summary Stats table live, type each formula slowly and read it aloud: *"COUNTA of column A, minus 1 for the header."*
- The negative MIN value (£-11,062.06) often surprises students — use it as a preview of data quality issues to address in Week 3.
- If any student already has a `Revenue` column from Week 1's group exercise, ask them to verify row 2 = **£15.30**.
