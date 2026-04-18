# Week 06 — Thursday: Power Query Capstone — Full Pipeline & Refresh
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 06 of 6
**Session:** Thursday
**Topic:** Power Query Capstone — Building a Complete Analytics Pipeline from Scratch

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-06-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-06-thu-exercises.xlsx`
- [ ] Weekly assignment ready to share at end of session
- [ ] Projector / screen sharing ready
- [ ] Country Lookup table prepared (from Wednesday) ready to load

---

## Learning Objectives

By the end of this session, students will be able to:

1. Build a complete Power Query pipeline from scratch incorporating all weeks' transformations
2. Load multiple query outputs (clean row-level data and aggregated summaries) to separate sheets
3. Use the Refresh button to update all queries when source data changes
4. Pivot and unpivot columns to reshape data for different analytical needs
5. Connect Power Query output to a PivotTable and an Excel formula (SUMIF) to build a mini dashboard
6. Explain the full ETL pattern: where to put each transformation and why

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap all 5 weeks: formulas → pivot → Power Query progression | "Why PQ is the foundation for everything after" |
| 0:10 – 0:35 | Part 1 — Build the full pipeline live (all steps from scratch) | Students follow step-by-step |
| 0:35 – 0:55 | Part 2 — Pivot and Unpivot: reshaping data for analysis | Month pivot → revenue by country by month |
| 0:55 – 1:15 | Part 3 — Load to multiple sheets; connect PivotTable to Clean Data | Refreshable dashboard |
| 1:15 – 1:35 | Part 4 — Refresh behaviour: change source, refresh, watch tables update | Live "simulated data update" |
| 1:35 – 2:00 | Group Exercise + assignment intro + Phase 1 wrap-up | Celebrate finishing Excel phase! |

---

## Concepts & Verified Outputs

### Concept 1 — The Complete Pipeline (all steps in order)

Build this pipeline live from `data.csv` as a step-by-step recap of the entire Phase 1 Power Query content:

**Step sequence:**
1. `Source` — Load data.csv via Get Data → From Text/CSV → Transform Data
2. `Promoted Headers` — auto-created
3. `Changed Type` — auto-created (will fix manually)
4. `Changed Type 1` — Fix InvoiceNo → Text, CustomerID → Text, InvoiceDate → Date/Time
5. `Renamed Columns` — UnitPrice → UnitPrice (£)
6. `Filtered Rows` — Quantity ≥ 0 (remove returns)
7. `Trimmed Text` — Trim Description column (Transform → Format → Trim)
8. `Replaced Value` — EIRE → Ireland
9. `Filtered Rows1` — Remove blank CustomerID
10. `Added Custom` — Revenue = [Quantity] * [UnitPrice]
11. `Added Conditional Column` — Revenue Tier (High/Medium/Low)
12. `Added Year` — Year extracted from InvoiceDate
13. `Added Month Name` — Month Name extracted from InvoiceDate
14. `Added Day Name` — Day Name extracted from InvoiceDate

**Total Applied Steps on completion: 14**

**Verified on 1,000-row sample after all filters:**
- Starting rows: 1,000
- After Qty ≥ 0 filter: 990
- After blank CustomerID filter: 989
- Final clean rows: **989**
- Columns: 12 (original 8 + Revenue + Revenue Tier + Year + Month Name + Day Name — minus the UnitPrice rename which keeps the same column count)

> Full dataset clean rows (after same filters): approximately 397,884

---

### Concept 2 — Pivot Columns: Monthly Revenue by Country

**What Pivot does:** Takes unique values from one column and spreads them as new column headers — the opposite of Group By stacking.

**Setup — create a monthly summary query:**
1. Duplicate the clean pipeline query
2. Add a `Month` column (Add Column → Date → Month → Month — returns a number 1–12)
3. Group By: Country + Month, aggregation = Sum of Revenue
4. Then: **Transform tab → Pivot Column**
5. Values column: `Total Revenue`; Column to pivot: `Month`
6. Result: one column per month number, rows by country

**Verified on 1,000-row sample:**
- All rows are December 2010 (Month = 12 only)
- Pivot produces one column: `12`
- United Kingdom row shows total UK revenue

> Full dataset: 13 months span → 13 columns after pivot. Show this as the expected live result.

M formula for Pivot:
```
= Table.Pivot(#"Grouped Rows", List.Distinct(#"Grouped Rows"[Month]), "Month", "Total Revenue", List.Sum)
```

---

### Concept 3 — Unpivot Columns

**What Unpivot does:** The reverse — takes column headers and collapses them back into rows. Useful when data arrives in a wide format (one column per month) and needs to be reshaped into a tidy tall format.

**Demo:**
1. Start from the pivoted monthly table
2. Select all month columns (Ctrl+click)
3. **Transform tab → Unpivot Columns**
4. Result: two new columns — `Attribute` (the month number) and `Value` (the revenue)
5. Rename: Attribute → Month, Value → Revenue

Teaching point: *"Data from finance teams often arrives wide — one column per month. Unpivot is the first thing you do to make it usable for analysis or pivot tables."*

---

### Concept 4 — Loading Multiple Outputs

Load four separate query results to four sheets in one workbook:

| Query | Sheet Name | Contents |
|---|---|---|
| Clean row-level data | `Clean Sales` | All 989 rows (1K sample), 12 columns |
| Country Group By | `Revenue by Country` | Country + Total Revenue + Order Count |
| Monthly pivot | `Monthly Pivot` | Country rows, one column per month |
| Revenue Tier summary | `Tier Summary` | Revenue Tier + row count (Group By tier) |

Steps to load all four:
- Each query: **Home → Close & Load → Close & Load To… → Table → specify sheet name**
- All four load simultaneously; Queries & Connections pane shows all four

**Verified on 1,000-row sample — Tier Summary:**

| Revenue Tier | Count |
|---|---|
| High (> £50) | ~220 |
| Medium (£10–£50) | ~310 |
| Low (≤ £10) | ~459 |

> Exact counts: run live. These are approximate from the 1,000-row sample distribution.

---

### Concept 5 — Connect PivotTable to Clean Data Output

After loading `Clean Sales` as an Excel table:

1. Click anywhere in the `Clean Sales` table
2. **Insert → PivotTable → From Table/Range** — PivotTable connected to the query output
3. Configure: Rows = Country, Values = Sum of Revenue, Columns = Revenue Tier

The PivotTable now refreshes automatically when the PQ query refreshes. **Data → Refresh All** updates the source query AND the PivotTable in one click.

Teaching point: *"This is the full analytics stack: raw CSV → Power Query cleans and enriches → Excel Table → PivotTable summarises → chart visualises. Everything refreshes from one button."*

---

### Concept 6 — Simulated Data Refresh

**Demo: show the refresh cycle live**

1. Save the workbook
2. In the source `data.csv` (or a copy), delete 50 rows
3. Back in Excel: **Data → Refresh All**
4. All four tables update with the reduced row count
5. The connected PivotTable updates too

If editing the raw CSV live is risky: load a smaller "v2" CSV with a visible change instead.

Teaching point: *"In a real business this is the power of Power Query — the finance team updates the monthly sales file. You click Refresh. Your dashboard updates. No copy-pasting, no manual formula dragging."*

---

### Concept 7 — Full M Code View

Show the Advanced Editor (Home → Advanced Editor) for the full clean pipeline query.

The complete M code for the 14-step pipeline:

```m
let
    Source = Csv.Document(File.Contents("PATH\data.csv"),[Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"InvoiceNo", type text}, {"StockCode", type text}, {"Description", type text}, {"Quantity", Int64.Type}, {"InvoiceDate", type datetime}, {"UnitPrice", type number}, {"CustomerID", type text}, {"Country", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"UnitPrice", "UnitPrice (£)"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each [Quantity] >= 0),
    #"Trimmed Text" = Table.TransformColumns(#"Filtered Rows",{{"Description", Text.Trim, type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Trimmed Text","EIRE","Ireland",Replacer.ReplaceText,{"Country"}),
    #"Filtered Rows1" = Table.SelectRows(#"Replaced Value", each [CustomerID] <> null and [CustomerID] <> ""),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows1", "Revenue", each [Quantity] * [#"UnitPrice (£)"], type number),
    #"Added Conditional Column" = Table.AddColumn(#"Added Custom", "Revenue Tier", each if [Revenue] > 50 then "High" else if [Revenue] > 10 then "Medium" else "Low", type text),
    #"Added Year" = Table.AddColumn(#"Added Conditional Column", "Year", each Date.Year([InvoiceDate]), Int64.Type),
    #"Added Month Name" = Table.AddColumn(#"Added Year", "Month Name", each Date.MonthName([InvoiceDate]), type text),
    #"Added Day Name" = Table.AddColumn(#"Added Month Name", "Day Name", each Date.DayOfWeekName([InvoiceDate]), type text)
in
    #"Added Day Name"
```

Teaching point: *"Everything you did by clicking in the GUI was writing this M code for you. Advanced users edit M directly — but for 90% of business tasks, the GUI is all you need."*

---

## Group Exercise

**Questions (20 min):**

1. Build the **complete 14-step pipeline** from scratch (or open your workbook from Wednesday and add the missing steps). When complete, how many Applied Steps are listed?
   *(Expected: 14)*

2. Load the clean data to a sheet called `Clean Sales`. How many rows does the table contain?
   *(Expected: 989 on the 1,000-row sample)*

3. Create a separate Group By query that calculates **Total Revenue by Revenue Tier**. Load it to a sheet called `Tier Summary`. Which Revenue Tier has the highest total revenue in your sample?
   *(Run live — "High" tier rows are fewer but larger; expected: High has the highest total)*

4. On the `Clean Sales` table, insert a **PivotTable** (Insert → PivotTable → From Table/Range). Build a pivot showing **Revenue by Country**. Which country has the highest total revenue?
   *(Expected: United Kingdom dominates)*

5. Click **Data → Refresh All**. What happens to the four loaded tables?
   *(Expected: all tables refresh from the query — row counts and values update)*

**Debrief points:**
- What is the difference between Close & Load (to Table) and Connection Only? When would you use Connection Only?
- If you add a new column to the source CSV, what happens after Refresh? Does PQ automatically include it?
- Why is connecting a PivotTable to a PQ output better than connecting it directly to the CSV?

---

## Weekly Assignment

*Set at the end of this session — students complete before the project kick-off (Week 7 group reveal).*

1. **Build the complete 14-step pipeline** on your own `data.csv` file and load the output to a sheet called `Clean Sales`. Screenshot your Applied Steps pane showing all 14 steps in order.

2. Create a **Group By query** on the clean data that calculates, for each `Country`:
   - `Total Revenue` (Sum of Revenue)
   - `Order Count` (Count Rows)
   - `Avg Revenue per Order` (Average of Revenue)
   Load the result to a sheet called `Country Analysis`.

3. Create a **Conditional Column** called `Market Type` with these rules:
   - Country = "United Kingdom" → "Domestic"
   - Else → "International"
   Group By `Market Type` and calculate Total Revenue and Order Count. Load to a sheet called `Market Summary`.

4. Extract `Year`, `Month Name`, and `Day Name` from InvoiceDate. Then Group By `Day Name` to find which **day of the week** has the highest average revenue per order. Load to a sheet called `Daily Pattern`.

5. On your `Clean Sales` output table, insert a PivotTable showing **Revenue Tier by Country** (Revenue Tier in columns, Country in rows, Sum of Revenue as values). Take a screenshot.

6. Add a formula-based check on a separate `Audit` sheet: use `=COUNTA(CleanSales[InvoiceNo])` and `=SUM(CleanSales[Revenue])` to verify your pipeline row count and total revenue. Compare these to the Group By totals from task 2.

**Submission:** Send your completed `.xlsx` workbook to the course Google Drive folder before the next session.

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-06-thu-demo.xlsx` | Instructor demo — Clean Data (989 rows), Calculated Columns, Country Summary, Tier Summary |
| `exercises/week-06-thu-exercises.xlsx` | Student workbook — Raw Data + Instructions + Column Workspace |
| `solutions/week-06-thu-solutions.xlsx` | Instructor reference — all sheets completed with verified values |

---

## Phase 1 Excel Wrap-Up

This is the final session of Phase 1. Acknowledge the journey:

| Week | Topic | Key skill unlocked |
|---|---|---|
| 1 | Data Import & Navigation | Working with raw data in Excel |
| 2 | Excel Basics | Formulas, references, named ranges |
| 3 | Advanced Functions | XLOOKUP, nested IFs, conditional logic |
| 4 | Pivot Tables & Charts | Aggregation and visual storytelling |
| 5 | Power Query Part 1 | ETL — load, clean, transform |
| 6 | Power Query Part 2 | Merge, enrich, pipeline + refresh |

*Next: Phase 2a Python — same data analysis concepts, new tool. Power Query will feel familiar.*

---

## Instructor Notes

- **Full pipeline from scratch:** This is the most important session — it's the consolidation of everything. Take time to do it properly. If you run short, skip Pivot/Unpivot (Concept 2–3) and focus on the full pipeline (Concept 1) and loading (Concept 4).
- **Multiple queries in one workbook:** Show the Queries & Connections pane with all four queries listed. Students are often surprised that PQ manages multiple queries simultaneously.
- **Refresh All:** The "wow moment" for most students. Run this slowly and deliberately so everyone sees all tables update at once.
- **Assignment Q6 (COUNTA audit formula):** The structured table reference `CleanSales[InvoiceNo]` will only work if the loaded table is named `CleanSales`. Show students how to rename a table: Table Design tab → Table Name field.
- **Phase transition note:** Remind students that everything they've learned in Phase 1 applies in Python. pandas DataFrames are Power Query in code. VLOOKUP is `.merge()`. Group By is `.groupby()`. Framing Phase 2a as "Power Query but with code" helps enormously.
- **openpyxl note:** The demo workbook contains static tables for Clean Data (989 rows) and all summary sheets. Power Query connections and PivotTables must be built live during class. The workbook shows the expected end result for students to check against.
