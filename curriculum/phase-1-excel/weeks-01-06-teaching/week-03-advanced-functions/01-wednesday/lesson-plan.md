# Week 03 — Wednesday: SUMIFS, AVERAGEIF & IF Logic
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 03 of 6
**Session:** Wednesday
**Topic:** SUMIFS, AVERAGEIF & IF Logic

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-03-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-03-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready

---

## Learning Objectives

By the end of this session, students will be able to:

1. Use SUMIFS and AVERAGEIF with multiple criteria to aggregate revenue by segment
2. Build IF statements for business classification (order type, revenue tier)
3. Combine LEFT/RIGHT text functions with logical tests to flag cancellations

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap: Week 2 formulas (COUNTA, COUNTIF, SUMIF) | Quick-fire Q&A |
| 0:10 – 0:45 | Part 1 — SUMIFS: Revenue by Country | Build summary table live |
| 0:45 – 1:05 | Part 2 — AVERAGEIF: Average metrics by segment | One formula at a time |
| 1:05 – 1:40 | Part 3 — IF + LEFT: Order type & revenue category | Two new helper columns |
| 1:40 – 2:00 | Group Exercise + debrief | Students work, instructor circulates |

---

## Concepts & Verified Outputs

### Setup: Revenue Column

Before any aggregation, add a `Revenue` column (column I):
```
=[@Quantity]*[@UnitPrice]
```
This is the `sum_range` for all SUMIFS formulas.

---

### Concept 1 — SUMIFS

**Syntax:** `=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2, ...])`

Key teaching point: SUMIFS is preferred over SUMIF even for single conditions — it supports multiple criteria and is more consistent.

**Revenue by Country (build this table live):**

| Country | Formula | Full Dataset Verified |
|---|---|---|
| United Kingdom | `=SUMIFS(I:I,H:H,"United Kingdom")` | **£8,187,806.36** |
| Germany | `=SUMIFS(I:I,H:H,"Germany")` | **£221,698.21** |
| Netherlands | `=SUMIFS(I:I,H:H,"Netherlands")` | **£285,446.34** |
| France | `=SUMIFS(I:I,H:H,"France")` | **£209,715.11** |
| EIRE | `=SUMIFS(I:I,H:H,"EIRE")` | **£283,453.96** |

> Sample values will differ — run live and note results.

**Multi-condition SUMIFS:**
```
=SUMIFS(I:I,H:H,"United Kingdom",D:D,">10")   ← UK revenue where Qty > 10
=SUMIFS(I:I,F:F,">5")                          ← Revenue where UnitPrice > 5
```

---

### Concept 2 — AVERAGEIF

**Syntax:** `=AVERAGEIF(range, criteria, average_range)`

| Formula | Full Dataset Verified |
|---|---|
| `=AVERAGEIF(H:H,"United Kingdom",D:D)` | **8.61** (avg quantity per UK order) |
| `=AVERAGEIF(H:H,"Germany",F:F)` | Run & verify in class |
| `=AVERAGEIF(D:D,">0",D:D)` | Avg quantity for positive orders only |

---

### Concept 3 — IF + LEFT: OrderType Column

Add column J — `OrderType`:
```
=IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")
```

Verify immediately:
```
=COUNTIF(J:J,"Cancellation")
```
**Full dataset verified: 9,288 cancellations.**
Sample count will be smaller — run live.

---

### Concept 4 — Nested IF: RevenueCategory Column

Add column K — `RevenueCategory`:
```
=IF([@Revenue]>=1000,"High",IF([@Revenue]>=100,"Medium",IF([@Revenue]>0,"Low","Non-Sale")))
```

Teaching point: Excel evaluates top-down — order from largest to smallest threshold matters.

---

## Group Exercise

**Questions (25 min):**

1. Using SUMIFS, what is total revenue for orders from **France**?
   *(Full dataset expected: £209,715.11)*

2. Using SUMIFS with two conditions, what is total revenue from **United Kingdom** where **UnitPrice > £5**?

3. Add the `OrderType` column using LEFT + IF. Verify with COUNTIF that you get the right number of cancellations on your sample.

4. Build an IF formula to flag Quantity:
   - `< 0` → "Return"
   - `= 0` → "Zero Order"
   - `> 0` → "Sale"
   Add this as column `QuantityFlag`.

**Debrief points:**
- Did everyone get the same France revenue? Why might results differ on the sample?
- What happens if the nested IF order is reversed (Low before High)?
- Where might LEFT(InvoiceNo, 1) produce unexpected results?

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-03-wed-demo.xlsx` | Instructor demo workbook — end-state with all formulas filled |
| `exercises/week-03-wed-exercises.xlsx` | Distributed to students — blank answer cells |
| `solutions/week-03-wed-solutions.xlsx` | Instructor reference — do not share before exercise is complete |

---

## Instructor Notes

- **SUMIFS vs SUMIF:** Students often reach for SUMIF first. Redirect to SUMIFS — it handles multi-condition cases and the syntax is more predictable.
- **Criteria must be quoted:** `"United Kingdom"` not `United Kingdom`. This is the #1 error.
- **LEFT returns text:** The comparison `LEFT(A2,1)="C"` works because both sides are text. Comparing to a number (e.g. `=1`) will silently fail.
- **Nested IF order matters:** Always check the highest threshold first. If you write Low before High, every row will be "Low".
- **Revenue column prerequisite:** Confirm students have column I (Revenue = Quantity × UnitPrice) before the SUMIFS section. If they didn't build it in Week 2, do it now.
