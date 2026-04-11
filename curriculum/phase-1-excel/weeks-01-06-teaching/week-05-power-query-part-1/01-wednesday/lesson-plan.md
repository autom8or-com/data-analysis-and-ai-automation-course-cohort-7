# Week 05 — Wednesday: Introduction to Power Query
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 05 of 6
**Session:** Wednesday
**Topic:** Introduction to Power Query — Loading, Transforming & Filtering Data

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-05-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-05-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready
- [ ] Excel Data tab → "Get Data" visible (confirm Power Query is available)

---

## Learning Objectives

By the end of this session, students will be able to:

1. Explain what Power Query is and how it differs from manual Excel formulas
2. Load a CSV file into the Power Query Editor
3. Apply basic transformations: rename columns, change data types, remove unwanted columns
4. Filter rows using column filters (e.g. remove returns where Quantity < 0)
5. View and understand the Applied Steps pane
6. Load the transformed query result as an Excel table

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap: Week 4 pivot tables — what they can and can't do | Bridge to "why PQ?" |
| 0:10 – 0:25 | Part 1 — What is Power Query? Concept walkthrough | Whiteboard the ETL pipeline |
| 0:25 – 0:55 | Part 2 — Load data.csv into Power Query Editor | Live demo: Get Data → From Text/CSV |
| 0:55 – 1:20 | Part 3 — Basic transformations (rename, types, remove columns) | Students follow along |
| 1:20 – 1:40 | Part 4 — Filter rows: remove Quantity < 0 | Show Applied Steps pane |
| 1:40 – 2:00 | Group Exercise + debrief | Students work, instructor circulates |

---

## Concepts & Verified Outputs

### Concept 1 — What is Power Query?

Power Query is Excel's built-in ETL (Extract, Transform, Load) engine. Key selling points:

- **Repeatable:** every transformation is recorded as a step — re-run with one click
- **Non-destructive:** raw data is never changed; the query reads from the source
- **Scalable:** handles millions of rows — no formula dragging required

Open with: **Data tab → Get Data → From File → From Text/CSV**

Teaching point: *"Think of Power Query as a recipe. You write the recipe once; Excel follows it every time you refresh."*

---

### Concept 2 — Loading data.csv into the Editor

Steps to demo live:
1. Data → Get Data → From File → From Text/CSV
2. Browse to `data.csv` — Power Query previews the first 200 rows
3. Click **Transform Data** (NOT Load) to open the Power Query Editor
4. Show the four panes: Query Settings, Applied Steps, formula bar, data preview

**Verified on load:**
- Rows in preview: shows first 200 rows; full load = **541,909 rows** (full dataset) / **1,000 rows** (sample workbook)
- Columns detected: 8 — InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

Initial Applied Steps created automatically:
1. `Source` — connects to the CSV file
2. `Promoted Headers` — first row becomes column headers
3. `Changed Type` — Power Query guesses data types

---

### Concept 3 — Renaming Columns

Double-click a column header in the Power Query Editor to rename it.

Demo renames:
| Original | Rename to | Why |
|---|---|---|
| `InvoiceNo` | `InvoiceNo` | Keep as-is |
| `UnitPrice` | `UnitPrice (£)` | Add currency indicator |
| `CustomerID` | `CustomerID` | Keep as-is |

Show that each rename creates a new step in the Applied Steps pane: `Renamed Columns`.

---

### Concept 4 — Changing Data Types

Power Query auto-detects types but often gets them wrong. Demo corrections:

| Column | Auto-detected | Correct Type | How to change |
|---|---|---|---|
| InvoiceNo | Whole Number | Text | Right-click header → Change Type → Text |
| Quantity | Whole Number | Whole Number | (correct) |
| UnitPrice | Decimal Number | Decimal Number | (correct) |
| CustomerID | Whole Number | Text | Right-click → Change Type → Text |
| InvoiceDate | Text / DateTime | Date/Time | Change Type → Date/Time |

**Key teaching point:** InvoiceNo and CustomerID should be **Text**, not numbers — you never do arithmetic on them, and they may have leading zeros or letters (e.g. "536365", "C536391").

When changing a type, a dialog asks: *"Replace current step or add new step?"* — always choose **Add New Step**.

---

### Concept 5 — Removing Unwanted Columns

To remove a column: right-click header → **Remove Column**, or select multiple with Ctrl+click then right-click.

Demo: remove no columns from this dataset (all 8 are useful), but demonstrate removing and undoing via the Applied Steps pane — show students they can delete any step by clicking the X.

Teaching point: *"In a real project you'd strip out columns your analysis doesn't need. This week we keep all 8."*

---

### Concept 6 — Filtering Rows: Remove Returns

Returns have **Quantity < 0**. To filter them out:

1. Click the filter arrow on the `Quantity` column
2. Choose **Number Filters → Greater Than or Equal To**
3. Enter `0` → OK
4. Observe Applied Steps: `Filtered Rows` added

**Verified on 1,000-row sample:**
- Rows before filter: **1,000**
- Rows with Quantity < 0: **10**
- Rows after filter: **990**

> Full dataset: 541,909 rows before; sample rows with Quantity < 0 differs from full-dataset cancellation count (which counts InvoiceNo starting with "C") — emphasise these are different definitions.

Show the M formula in the formula bar:
```
= Table.SelectRows(#"Changed Type", each [Quantity] >= 0)
```

---

### Concept 7 — The Applied Steps Pane

Show the complete Applied Steps pane after all transformations:
1. Source
2. Promoted Headers
3. Changed Type
4. Renamed Columns
5. Changed Type 1 (CustomerID → Text, InvoiceNo → Text)
6. Filtered Rows

Click each step to see the data state at that point — time travel through transformations.

---

### Concept 8 — Loading to Excel

**Home → Close & Load → Close & Load To…**

Options:
- **Table** (in existing or new sheet) — recommended for further analysis
- **PivotTable** — load directly into a pivot
- **Connection Only** — no output yet; can connect later

Demo: load as a **Table** to a new sheet called `Clean Data`.

After loading, show the **Queries & Connections** pane (Data → Queries & Connections). Right-click the query → **Refresh** to re-run all steps.

---

## Group Exercise

**Questions (20 min):**

1. Load `data.csv` into Power Query using **Get Data → From Text/CSV**. Click *Transform Data* (do NOT click Load). How many columns does Power Query detect automatically?

2. Change the data type of `InvoiceNo` and `CustomerID` to **Text**. What step name appears in the Applied Steps pane after this change?

3. Filter the `Quantity` column to keep only rows where **Quantity ≥ 0**. On your 1,000-row sample, how many rows remain after filtering?
   *(Expected: 990 rows — 10 returns removed)*

4. Rename the column `UnitPrice` to `UnitPrice (£)`. Write the M formula that Power Query generates (visible in the formula bar after renaming).
   *(Expected: `= Table.RenameColumns(...)` — show it on screen)*

5. Load the transformed query as a Table to a new sheet. What is the name Power Query gives the new sheet by default?

**Debrief points:**
- Did anyone accidentally click *Load* instead of *Transform Data*? (Walk them through closing and re-opening from Queries & Connections)
- Why is it important to change CustomerID to Text and not leave it as a number?
- What happens if you delete a step in the middle of the Applied Steps list?

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-05-wed-demo.xlsx` | Instructor demo workbook — end-state with PQ Steps Log and sample clean table |
| `exercises/week-05-wed-exercises.xlsx` | Distributed to students — Raw Data sheet only; students build the query |
| `solutions/week-05-wed-solutions.xlsx` | Instructor reference — completed PQ Steps Log with all transformation details |

---

## Instructor Notes

- **"Transform Data" vs "Load":** This is the #1 mistake. Once students click Load without transforming, close the query and reopen via Data → Queries & Connections → right-click → Edit.
- **Type change dialog — "Replace" vs "Add new step":** Always choose *Add New Step*. Replacing the auto-generated Changed Type step removes the record of what the original types were.
- **Applied Steps are deletable and reorderable — with risk:** If you delete an early step, downstream steps may break. Demonstrate this briefly so students understand dependencies.
- **M formula bar:** Some students will be curious. Tell them M is a functional language Power Query writes for you — they don't need to write it manually this week.
- **Refresh behaviour:** The query remembers the file path. If students move `data.csv`, the query will break with a "file not found" error. Show them how to update the source path via Applied Steps → Source → gear icon.
- **openpyxl note:** The demo workbook shows static PQ Steps Log and Clean Data tables — Power Query connections cannot be saved by openpyxl. Recreate the live query during class; the workbook shows the expected end result.
