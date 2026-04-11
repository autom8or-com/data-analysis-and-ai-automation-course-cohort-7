# Week 05 — Thursday: Power Query Text Cleaning, Group By & Custom Columns
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 05 of 6
**Session:** Thursday
**Topic:** Power Query — Text Cleaning, Group By Aggregation & Custom Columns

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-05-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-05-thu-exercises.xlsx`
- [ ] Weekly assignment ready to share at end of session
- [ ] Projector / screen sharing ready
- [ ] Wednesday's query still open or re-built from Applied Steps

---

## Learning Objectives

By the end of this session, students will be able to:

1. Clean text data in Power Query using Trim, Replace Values, and Change Case transformations
2. Remove rows with null/blank values in a specific column
3. Add a custom calculated column (Revenue = Quantity × UnitPrice) using Power Query
4. Use Group By to aggregate data (total revenue and order count by country)
5. Load a clean, aggregated dataset back to Excel for further analysis

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap Wednesday: load, type, filter, Applied Steps | Quick-fire Q&A |
| 0:10 – 0:35 | Part 1 — Text cleaning (Trim, Replace Values, Change Case) | Build on Wednesday's query |
| 0:35 – 0:55 | Part 2 — Remove blank rows (null CustomerID) | Show filter vs Remove Blank Rows |
| 0:55 – 1:20 | Part 3 — Add Custom Column (Revenue = Quantity × UnitPrice) | Introduce M formula bar |
| 1:20 – 1:40 | Part 4 — Group By: revenue by country | Aggregation without pivot tables |
| 1:40 – 2:00 | Group Exercise + debrief + assignment intro | |

---

## Concepts & Verified Outputs

### Setup: Start from Wednesday's query

Open the Power Query Editor for the query created on Wednesday (Queries & Connections pane → right-click → Edit). The Applied Steps should already include: Source, Promoted Headers, Changed Type, Renamed Columns, Changed Type 1, Filtered Rows.

Today's steps add on top of this clean foundation.

---

### Concept 1 — Trim: Remove Extra Spaces from Description

**Why:** Leading/trailing spaces in Description cause COUNTIF and VLOOKUP mismatches (same concept as TRIM in Week 3 formulas — now done at source level, not in a helper column).

Steps:
1. Select the `Description` column
2. **Transform tab → Format → Trim**
3. New Applied Step: `Trimmed Text`

The M formula generated:
```
= Table.TransformColumns(#"Filtered Rows",{{"Description", Text.Trim, type text}})
```

**Full dataset fact:** 113,452 Description values have leading or trailing spaces — Trim cleans all of them in one step.

---

### Concept 2 — Replace Values

Demo: fix a specific value in the Country column — "EIRE" → "Ireland".

Steps:
1. Select the `Country` column
2. **Transform tab → Replace Values**
3. Value to find: `EIRE` / Replace with: `Ireland`
4. Applied Step added: `Replaced Value`

M formula:
```
= Table.ReplaceValue(#"Trimmed Text","EIRE","Ireland",Replacer.ReplaceText,{"Country"})
```

**Verified on sample:** The sample contains 0 rows with Country = "EIRE" (those appear later in the full dataset). Demo this live and note: *"On the 1,000-row sample, EIRE doesn't appear, but the step is still recorded — it will apply when the full dataset is loaded."*

Full dataset: EIRE appears 8,196 times — all renamed in one step.

---

### Concept 3 — Remove Rows with Blank CustomerID

**Why:** Rows without a CustomerID cannot be attributed to a customer — flag this for analysis context.

Steps:
1. Click the filter arrow on `CustomerID`
2. Uncheck `null` → OK
3. Applied Step: `Filtered Rows1`

**Verified on 1,000-row sample:**
- Rows before: 990 (after Wednesday's Quantity filter)
- Rows with blank CustomerID: **1**
- Rows after: **989**

> Full dataset: ~135,080 rows have no CustomerID (sales to walk-in customers). Removing them is a deliberate analytical choice — explain this trade-off to students.

---

### Concept 4 — Add Custom Column: Revenue

Custom columns add calculated fields without touching the source data.

Steps:
1. **Add Column tab → Custom Column**
2. Column name: `Revenue`
3. Formula: `[Quantity] * [UnitPrice]`
4. Click OK

The formula bar shows:
```
= Table.AddColumn(#"Filtered Rows1", "Revenue", each [Quantity] * [UnitPrice], type number)
```

**Verified on 1,000-row sample (positive qty rows, after CustomerID filter):**
- Revenue column: `[Quantity] * [UnitPrice]` for each row
- Total Revenue (SUM check after loading): derived from 989 rows

Teaching point: *"This is identical to the `=[@Quantity]*[@UnitPrice]` formula we wrote manually in Week 3 — but here it's in the query, so every row is calculated automatically on refresh, for any dataset size."*

---

### Concept 5 — Group By: Revenue by Country

Group By collapses the row-level data into summary aggregations — similar to a pivot table but fully scriptable.

Steps:
1. **Transform tab → Group By**
2. Group By column: `Country`
3. Add aggregation: New column name = `Total Revenue`, Operation = `Sum`, Column = `Revenue`
4. Add second aggregation: `Order Count`, Operation = `Count Rows`
5. OK

Applied Step: `Grouped Rows`

**Verified on 1,000-row sample (after all prior steps):**

| Country | Total Revenue (£) | Order Count |
|---|---|---|
| United Kingdom | ~23,299 | ~955 |
| France | ~346 | ~20 |
| Australia | ~884 | ~14 |

> Sample values — run live and note results. Full dataset: UK dominates at ~£8.2M.

M formula:
```
= Table.Group(#"Added Custom", "Country", {{"Total Revenue", each List.Sum([Revenue]), type number}, {"Order Count", each Table.RowCount(_), Int64.Type}})
```

---

### Concept 6 — Load to Excel

After Group By, load the summary to a new sheet:
- **Home → Close & Load → Close & Load To…**
- Select **Table** → New Worksheet
- Name the sheet `Country Summary`

Also show loading the un-grouped clean data as a separate query (duplicate the query before the Group By step, load as `Clean Data`).

---

## Group Exercise

**Questions (20 min):**

1. Apply **Trim** to the `Description` column. What step name appears in Applied Steps?
   *(Expected: `Trimmed Text`)*

2. Add a **Custom Column** called `Revenue` with formula `[Quantity] * [UnitPrice]`. What data type does Power Query assign to the new column automatically?

3. Use **Group By** to count the number of orders per `Country` in your sample. Which country has the most orders?
   *(Expected: United Kingdom, ~955 on the 1,000-row sample)*

4. Remove rows where `CustomerID` is blank. How many rows remain in your sample after this filter?
   *(Expected: 989 rows)*

5. Load the grouped Country summary as an Excel Table. In your loaded table, what is the `Total Revenue` value for United Kingdom?
   *(Run live — approximately £23,299 on the sample)*

**Debrief points:**
- What is the difference between filtering Quantity < 0 (Wednesday) and removing blank CustomerIDs (today)?
- If you add a step and it breaks a downstream step — how do you fix it? (Delete the broken step and re-add)
- Why is Group By more powerful than a standard pivot table for this workflow?

---

## Weekly Assignment

*Set at the end of this session — students complete before next Wednesday.*

1. Starting fresh from `data.csv`, build a complete Power Query pipeline with these steps in order:
   - Load the file and click *Transform Data*
   - Change `InvoiceNo` and `CustomerID` to Text type
   - Apply Trim to the `Description` column
   - Filter rows to keep only **Quantity ≥ 1** (exclude zeros and returns)
   - Remove rows where **CustomerID is blank**
   - Add a Custom Column `Revenue` = `[Quantity] * [UnitPrice]`
   - Load the clean data as an Excel Table to a sheet called `Clean Sales`

   **Report:** How many rows does your Clean Sales table contain?
   *(Expected on the 1,000-row sample: 989 rows)*

2. On the same query (before loading), add a **Group By** step to calculate:
   - `Total Revenue` (Sum of Revenue) by Country
   - Load this summary to a second sheet called `Revenue by Country`
   
   Write down the Total Revenue for **United Kingdom** from your sample.

3. In the Power Query Editor, click each Applied Step in order. Write a one-sentence description of what each step does (at least 6 steps must be described).

4. What happens to your Excel tables if you move `data.csv` to a different folder? How would you fix the broken query?
   *(Answer: Source step breaks; fix via Applied Steps → Source → gear icon → update file path)*

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-05-thu-demo.xlsx` | Instructor demo workbook — PQ Steps Log, Clean Data sheet (989 rows), Country summary |
| `exercises/week-05-thu-exercises.xlsx` | Distributed to students — Raw Data + Cleaning Tracker sheet |
| `solutions/week-05-thu-solutions.xlsx` | Instructor reference — all cleaning steps documented with row counts |

---

## Instructor Notes

- **Duplicate the query before Group By:** Students often accidentally Group By the wrong query. Show them how to right-click a query → Duplicate, then apply Group By to the duplicate while keeping the row-level clean data separate.
- **M formula bar curiosity:** Students will ask about the formula language. Encourage curiosity but keep focus on the GUI. Tell them Week 6 introduces one custom M formula manually.
- **Custom Column type mismatch:** If `[Quantity]` is Text (not Number), the multiplication fails with a type error. This is a great teachable moment — always fix types before adding calculated columns.
- **Group By multiple columns:** You can group by multiple columns at once (e.g. Country + InvoiceDate month). Demonstrate briefly if time allows.
- **Assignment Q4 (broken path):** Make sure students understand that Power Query queries store an absolute file path. Moving the source file is a very common real-world pain point.
- **openpyxl note:** The demo workbook contains static Clean Data and Country Summary tables that approximate the PQ output. Recreate the live query during class — the workbook shows the expected end result for students to check against.
