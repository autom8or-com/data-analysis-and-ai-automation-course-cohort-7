# Week 04 — Wednesday: Pivot Tables — Summarise Data Instantly
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 04 of 6
**Session:** Wednesday
**Topic:** Pivot Tables — Summarise Data Instantly

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-04-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-04-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready

---

## Learning Objectives

By the end of this session, students will be able to:

1. Create a pivot table from raw transactional data using Insert → PivotTable
2. Drag fields into Rows, Columns, Values, and Filters to answer business questions
3. Change the Value Field Settings (Sum, Count, Average) and apply number formatting
4. Filter and sort pivot tables to isolate specific countries or products

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap: Week 3 formulas (SUMIFS, IF, TRIM) | Quick-fire Q&A |
| 0:10 – 0:20 | Why pivot tables? Motivation & anatomy | Slides / whiteboard |
| 0:20 – 0:50 | Part 1 — First Pivot Table: Revenue by Country | Build live from raw data |
| 0:50 – 1:15 | Part 2 — Adding dimensions: Country × OrderType | Two-field pivot |
| 1:15 – 1:40 | Part 3 — Value Field Settings & Filters | Count, Average, formatting |
| 1:40 – 2:00 | Group Exercise + debrief | Students work, instructor circulates |

---

## Concepts & Verified Outputs

### Setup: Revenue and OrderType Columns

Before building pivots, ensure these columns exist from Week 3:

**Revenue (column I):**
```
=[@Quantity]*[@UnitPrice]
```

**OrderType (column J):**
```
=IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")
```

If students don't have these, build them now — they are prerequisites.

---

### Concept 1 — Your First Pivot Table: Revenue by Country

**Steps (demonstrate live):**
1. Click any cell in the data range
2. `Insert → PivotTable → New Worksheet`
3. Drag `Country` to **Rows**
4. Drag `Revenue` to **Values** (defaults to Sum)
5. Right-click any value → Number Format → `£#,##0.00`

**Verified full-dataset results:**

| Country | Sum of Revenue |
|---|---|
| United Kingdom | **£8,187,806.36** |
| Netherlands | **£284,661.54** |
| EIRE | **£263,276.82** |
| Germany | **£221,698.21** |
| France | **£197,403.90** |
| Australia | **£137,077.27** |
| Switzerland | **£56,385.35** |
| Spain | **£54,774.58** |
| Belgium | **£40,910.96** |
| Sweden | **£36,595.91** |

> **Note:** Students working on the 1,000-row sample will see only 4 countries (United Kingdom, France, Australia, Netherlands) with much smaller totals. This is expected — the sample is a slice of the full dataset.

**Teaching point:** Pivot tables summarise hundreds of thousands of rows into a compact table in seconds — no formulas needed.

---

### Concept 2 — Two-Field Pivot: Revenue by Country × OrderType

**Steps:**
1. Keep `Country` in Rows
2. Drag `OrderType` to **Columns**
3. Revenue stays in Values

**Verified full-dataset results (top 5 countries):**

| Country | Sale | Cancellation |
|---|---|---|
| United Kingdom | £9,003,097.96 | -£815,291.60 |
| Netherlands | £285,446.34 | -£784.80 |
| EIRE | £283,453.96 | -£20,177.14 |
| Germany | £228,867.14 | -£7,168.93 |
| France | £209,715.11 | -£12,311.21 |

**Teaching point:** Negative cancellation values are expected — they represent returned revenue. This is a real business insight: the UK has the most cancellations by far (£815K).

---

### Concept 3 — Value Field Settings: Count & Average

Show students how to change what the Values area calculates:

**Count of transactions by Country:**
1. Drag `InvoiceNo` to Values (defaults to Count)
2. Right-click → Value Field Settings → Count

**Verified full-dataset transaction counts (top 5):**

| Country | Count of InvoiceNo |
|---|---|
| United Kingdom | 495,478 |
| Germany | 9,495 |
| France | 8,557 |
| EIRE | 8,196 |
| Spain | 2,533 |

**Average UnitPrice by Country:**
1. Clear existing pivot or start a new one
2. Country in Rows, UnitPrice in Values
3. Right-click → Value Field Settings → Average

**Verified (positive-quantity transactions only):**

| Country | Avg UnitPrice |
|---|---|
| United Kingdom | £3.79 |
| Netherlands | £2.64 |
| EIRE | £4.88 |
| Germany | £3.71 |
| France | £4.40 |

---

### Concept 4 — Filtering and Sorting

**Report Filter:**
1. Drag `Country` to **Filters** area (above the pivot)
2. Select "United Kingdom" only → pivot shows UK-only data
3. Show multi-select option

**Sorting:**
1. Right-click any revenue value → Sort → Largest to Smallest
2. Show that the sort persists when data refreshes

**Top N filter:**
1. Click the Row Labels dropdown → Value Filters → Top 10
2. Set to "Top 5 by Sum of Revenue"

---

## Group Exercise

**Questions (20 min):**

1. Create a pivot table showing **Sum of Revenue by Country**. Which country has the highest revenue in your sample?
   *(Full dataset expected: United Kingdom — £8,187,806.36)*

2. Add `OrderType` as a Column field. What is the total cancellation value for the United Kingdom?
   *(Full dataset expected: -£815,291.60)*

3. Create a new pivot table showing **Count of InvoiceNo by Country**. Which country has the most transactions?
   *(Full dataset expected: United Kingdom — 495,478)*

4. Change the pivot to show **Average of UnitPrice by Country**. Which country has the highest average unit price among the top 5 by revenue?
   *(Full dataset expected: EIRE — £4.88)*

**Debrief points:**
- Sample pivot will show fewer countries — that's fine, the technique is what matters
- Negative cancellation revenue is real data, not an error
- Point out how fast pivots are compared to building SUMIFS for every country manually

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-04-wed-demo.xlsx` | Instructor demo — static pivot result tables (pivot tables cannot be created programmatically) |
| `exercises/week-04-wed-exercises.xlsx` | Distributed to students — raw data + instructions, blank workspace |
| `solutions/week-04-wed-solutions.xlsx` | Instructor reference — completed pivot result tables |

---

## Instructor Notes

- **Pivot tables cannot be created by openpyxl:** The demo workbook contains static tables showing the expected results. You must **create the actual pivot table live** in class — the static tables serve as your answer key.
- **Revenue column prerequisite:** If students don't have Revenue (column I) from Week 3, build it now. The pivot won't work without it.
- **OrderType column prerequisite:** Same — build it from `IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")` if missing.
- **"Count" vs "Sum":** When you drag a text field (like InvoiceNo) to Values, Excel defaults to Count. When you drag a number field (like Revenue), it defaults to Sum. Students confuse these constantly.
- **Refresh data:** If students add formulas to the raw data after creating the pivot, they must right-click → Refresh to update.
- **Grand Totals:** By default, pivots show Grand Totals. Leave them on for now — they're useful for verification.
- **Sample vs full dataset:** Remind students that their 1,000-row sample produces smaller numbers and fewer countries than the full dataset. The verified values in this plan are from the full 541,909 rows.