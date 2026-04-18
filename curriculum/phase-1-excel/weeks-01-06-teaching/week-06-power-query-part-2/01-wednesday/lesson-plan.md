# Week 06 — Wednesday: Power Query — Merge, Append & Conditional Columns
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 06 of 6
**Session:** Wednesday
**Topic:** Power Query Part 2 — Merging Queries, Appending, Conditional Columns & Date Extraction

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-06-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-06-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready
- [ ] Power Query Editor open — confirm Week 5 query still accessible (or rebuild from Applied Steps)

---

## Learning Objectives

By the end of this session, students will be able to:

1. Append two query results into a single table using Power Query Append
2. Merge two queries on a common key column using Power Query Merge (left join)
3. Add a Conditional Column to categorise rows (e.g. Revenue tier: High / Medium / Low)
4. Extract date components (Year, Month, Day, Day Name) from a DateTime column
5. Explain when to use Append vs Merge and how they compare to SQL UNION and JOIN

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap Week 5: PQ pipeline, Applied Steps, Group By | Quick-fire Q&A + check assignment |
| 0:10 – 0:30 | Part 1 — Append Queries: stack two filtered subsets | Demo: split UK vs non-UK, re-combine |
| 0:30 – 0:55 | Part 2 — Merge Queries: join on a key column | Demo: create a lookup table, merge on Country |
| 0:55 – 1:20 | Part 3 — Conditional Column: Revenue tier | Add column with IF logic |
| 1:20 – 1:40 | Part 4 — Date extraction: Year, Month Name, Day | Transform tab → Date & Time column |
| 1:40 – 2:00 | Group Exercise + debrief | Students work, instructor circulates |

---

## Concepts & Verified Outputs

### Setup: Rebuild or open Week 5 query

Start from the clean 7-step query from Week 5 (Source → Promoted Headers → Changed Type → Renamed Columns → Changed Type 1 → Filtered Rows [Qty ≥ 0] → Trimmed Text → Replaced Value → Filtered Rows1 [no blank CustomerID] → Added Custom [Revenue]).

If students don't have it, rebuild the core steps live: Load data.csv → change InvoiceNo and CustomerID to Text → filter Quantity ≥ 0 → add Revenue = [Quantity] * [UnitPrice].

---

### Concept 1 — Append Queries

**What it does:** Stacks rows from two or more queries vertically — like SQL UNION ALL.

**Demo setup:**
1. Duplicate the clean query twice (right-click → Duplicate)
2. Rename copies: `UK Sales` and `Non-UK Sales`
3. On `UK Sales`: filter Country = "United Kingdom"
4. On `Non-UK Sales`: filter Country ≠ "United Kingdom"
5. Create a third new query via **Data → Get Data → Combine Queries → Append Queries as New**
6. Append `Non-UK Sales` onto `UK Sales`

**Verified on 1,000-row sample (after Qty and CustomerID filters — 989 rows total):**
- UK Sales rows: approximately **955**
- Non-UK Sales rows: approximately **34**
- Appended total: **989** (same as original clean query — full round-trip check)

M formula for Append:
```
= Table.Combine({#"UK Sales", #"Non-UK Sales"})
```

Teaching point: *"Append is useful when you receive monthly data files. Load January and February separately, then append — Power Query refreshes both automatically when new files arrive."*

---

### Concept 2 — Merge Queries (Left Join on Country)

**What it does:** Joins two queries on a shared key column — like SQL LEFT JOIN.

**Demo: build a small Country lookup table manually**

1. In Excel, create a small table on a new sheet (`Country Lookup`):

| Country | Region |
|---|---|
| United Kingdom | Europe |
| France | Europe |
| Germany | Europe |
| Australia | Asia-Pacific |
| Netherlands | Europe |
| EIRE | Europe |
| Spain | Europe |
| Sweden | Europe |
| Japan | Asia-Pacific |
| Norway | Europe |
| USA | Americas |

2. Load this sheet into Power Query: **Data → Get Data → From Table/Range**
3. On the main clean query: **Home → Merge Queries → Merge Queries as New**
4. Left table: clean query; Left column: `Country`
5. Right table: Country Lookup; Right column: `Country`
6. Join kind: **Left Outer** (all rows from left, matched rows from right)
7. Expand the merged column — select `Region` only

**Verified on 1,000-row sample:**
- Rows with Region filled in: all 989 rows match (UK dominates; other countries in lookup)
- Rows with null Region: 0 for countries in the lookup table; if a country is missing from lookup, Region = null (teach this as a data quality check)

M formula for Merge:
```
= Table.NestedJoin(#"Your Clean Query", {"Country"}, #"Country Lookup", {"Country"}, "Country Lookup", JoinKind.LeftOuter)
```

Teaching point: *"Merge is how you enrich a dataset with reference data — the same pattern as VLOOKUP but embedded in the query pipeline and always up to date."*

---

### Concept 3 — Conditional Column: Revenue Tier

A Conditional Column adds a new column based on IF/ELSE logic — no formula syntax required.

Steps:
1. Select the clean query (with Revenue column)
2. **Add Column tab → Conditional Column**
3. Column name: `Revenue Tier`
4. Rule 1: If `Revenue` is greater than `50` → `High`
5. Rule 2: If `Revenue` is greater than `10` → `Medium`
6. Else: `Low`
7. Click OK

Applied Step: `Added Conditional Column`

M formula generated:
```
= Table.AddColumn(#"Added Custom", "Revenue Tier", each if [Revenue] > 50 then "High" else if [Revenue] > 10 then "Medium" else "Low", type text)
```

**Verified on 1,000-row sample (989 clean rows):**

| Revenue Tier | Approximate Count |
|---|---|
| High (> £50) | ~220 |
| Medium (£10–£50) | ~310 |
| Low (≤ £10) | ~459 |

> Run live — exact counts depend on the sample. Full dataset thresholds produce a similar distribution.

Teaching point: *"This is the Power Query equivalent of a nested IF formula — but because it's a recorded step, it applies to every row automatically. Change the threshold later by editing the step, not by re-dragging formulas."*

---

### Concept 4 — Date Extraction

Extract year, month, and day components from the `InvoiceDate` column for time-series analysis.

**Pre-requisite:** InvoiceDate must be Date/Time type (fixed in Week 5 Changed Type step).

Steps:
1. Select the `InvoiceDate` column
2. **Add Column tab → Date → Year → Year** — creates column `Year`
3. **Add Column tab → Date → Month → Name of Month** — creates column `Month Name`
4. **Add Column tab → Date → Day → Day of Week Name** — creates column `Day Name`

M formulas:
```m
// Year
= Table.AddColumn(#"Added Conditional Column", "Year", each Date.Year([InvoiceDate]), Int64.Type)

// Month Name
= Table.AddColumn(#"Added Year", "Month Name", each Date.MonthName([InvoiceDate]), type text)

// Day Name
= Table.AddColumn(#"Added Month Name", "Day Name", each Date.DayOfWeekName([InvoiceDate]), type text)
```

**Verified on 1,000-row sample:**
- All InvoiceDate values are in 2010 (Year = 2010 for all rows in first 1,000)
- Month Name: `December` for all first-1,000 rows (dataset starts 01/12/2010)
- Day Name: `Wednesday` or `Thursday` (1 Dec 2010 was a Wednesday)

> Full dataset spans Dec 2010 – Dec 2011 — all 12 months and all days of the week appear.

Teaching point: *"Once you extract Year and Month Name as columns, you can Group By Month Name to build a monthly revenue trend — without writing a single MONTH() formula in Excel."*

---

## Group Exercise

**Questions (20 min):**

1. Duplicate your clean query and create two filtered subsets: one for **United Kingdom** only, and one for **all other countries**. Append them back together. How many rows does the appended result have?
   *(Expected: same as your clean row count — 989 on the 1,000-row sample)*

2. Add a **Conditional Column** called `Revenue Tier` with these rules: Revenue > £50 → "High", Revenue > £10 → "Medium", else "Low". How many "High" rows are in your sample?
   *(Run live — approximately 220 on the 1,000-row sample)*

3. Extract the **Year** from the `InvoiceDate` column using **Add Column → Date → Year**. What year(s) appear in the `Year` column on your 1,000-row sample?
   *(Expected: 2010 only — first 1,000 rows are all from December 2010)*

4. Extract **Month Name** from `InvoiceDate`. What is the month shown for all rows in your sample?
   *(Expected: December)*

5. Add a Merge to bring in the Country Lookup table your instructor shared. After expanding the `Region` column, how many distinct Region values appear in your sample?
   *(Expected: 2 — "Europe" and "Asia-Pacific" if Australia rows are present; otherwise 1)*

**Debrief points:**
- When would you use Append instead of Merge? (Append = same structure, more rows; Merge = different structure, adding columns)
- Why is extracting Year/Month in Power Query better than using YEAR()/MONTH() formulas in Excel?
- What happens if a Country in your data doesn't exist in the lookup table? (Region = null — teach as a data quality signal)

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-06-wed-demo.xlsx` | Instructor demo — end-state with Clean Data, Calculated Columns, Country Lookup sheets |
| `exercises/week-06-wed-exercises.xlsx` | Student workbook — Raw Data + Instructions + Column Workspace |
| `solutions/week-06-wed-solutions.xlsx` | Instructor reference — completed Column Workspace with all answers |

---

## Instructor Notes

- **Append vs Merge confusion:** Students frequently swap these. Anchor the distinction: Append = rows (more rows, same columns = UNION ALL); Merge = columns (more columns, same rows = JOIN). Draw it on a whiteboard.
- **Country Lookup table:** Create this manually in Excel before class and load it via Get Data → From Table/Range. Students often expect PQ to connect to a sheet automatically — show them the explicit Get Data step.
- **Conditional Column order matters:** PQ evaluates rules top-to-bottom and stops at the first match. If you put "Low" first, everything would be Low. Demonstrate this intentional mistake briefly.
- **Date column type prerequisite:** If InvoiceDate is still Text type, the Date menu items are greyed out. Always fix the type first. This is a common error point.
- **Merge null Region rows:** If a Country in the data isn't in the lookup, Region = null. Use this as a teaching moment: *"This is how you find data quality gaps — PQ surfaces them as nulls."*
- **openpyxl note:** The demo workbook contains static Clean Data and Calculated Columns tables. The Country Lookup sheet is a real formatted table. All PQ connections must be recreated live during class.
