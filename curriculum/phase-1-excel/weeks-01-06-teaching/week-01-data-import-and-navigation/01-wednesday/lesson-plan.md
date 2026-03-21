# Week 01 — Wednesday: Business Context & Data Import
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 01 of 6
**Session:** Wednesday
**Topic:** Business Context & Data Import

---

## Pre-Session Checklist

- [ ] Dataset accessible: `data.csv` from `teaching-data.zip` (UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-01-wed-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-01-wed-exercises.xlsx`
- [ ] Projector / screen sharing ready
- [ ] LMS: pin Dataset Reference Card before session starts

---

## Learning Objectives

By the end of this session, students will be able to:

1. Understand what data analytics is and why it matters in business
2. Import a CSV file into Excel correctly
3. Navigate a large dataset confidently

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:20 | Part 1 — Business context intro | See Concept 1 below |
| 0:20 – 0:50 | Part 2 — Importing the dataset | Step-by-step, groups follow along |
| 0:50 – 1:20 | Part 3 — Basic navigation | Keyboard shortcuts + freeze panes |
| 1:20 – 1:50 | Part 4 — Group exercise | Groups explore, no formulas |
| 1:50 – 2:00 | Debrief & close | Groups present answers verbally |

---

## Concept 1 — Business Context (20 min)

**What to demonstrate:**

Introduce the scenario:
> *"You have just been hired as a data analyst at a UK-based online gift retailer. The company sells to customers across 38 countries. Your job is to turn their raw transaction records into business intelligence."*

Cover:
- What is a dataset? Rows = transactions, columns = attributes
- Why Excel? Entry point to data thinking before code
- The data analysis workflow: **Import → Explore → Clean → Analyse → Present**

**Expected output / verified value:** No output — discussion only.

**Common mistakes to watch for:** Students may confuse "row" with "record" — reinforce that each row is one product line on one invoice, not one whole order.

---

## Concept 2 — Importing the Dataset (30 min)

**What to demonstrate:**

Step-by-step (instructor demos, groups follow):

1. Open Excel → `Data` tab → `Get Data` → `From Text/CSV`
2. Select `data.csv`
3. In the preview, confirm delimiter is set to **Comma**
4. Click **Load** (not Transform — that is Week 5)
5. Verify the data landed correctly

**Expected output / verified values:**
- Row count visible in status bar: **541,909 rows**
- Column count: **8 columns**
- First row is the header: `InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country`

**Common mistakes to watch for:**
- Students clicking **Transform Data** instead of **Load** — they will open Power Query Editor (Week 5 content). Close it and reload with **Load**.
- Wrong delimiter selected (Tab instead of Comma) — data lands in a single column.

---

## Concept 3 — Basic Navigation (30 min)

**What to demonstrate:**

| Shortcut | Action | Expected result |
|---|---|---|
| `Ctrl + End` | Jump to last data cell | Row 541,910, Column H |
| `Ctrl + Home` | Return to A1 | Top-left cell |
| `Ctrl + Arrow keys` | Navigate to end of column | Bottom of each column |
| Freeze top row | `View → Freeze Panes → Freeze Top Row` | Header always visible while scrolling |
| Rename sheet tab | Double-click tab → type `Raw Data` | Tab shows "Raw Data" |

**Expected output / verified values:**
- `Ctrl + End` lands on **row 541,910, column H** (row 1 = header + 541,909 data rows)

**Common mistakes to watch for:**
- Students pressing `Ctrl + End` before data is fully loaded — they may land on a wrong row. Wait for the status bar to stop showing "Calculating".

---

## Group Exercise (30 min)

Each group of 10 answers these questions by exploring the data — **no formulas, eyes and scroll only**.

Open `exercises/week-01-wed-exercises.xlsx` → `Instructions` sheet.

**Questions:**

1. What does one row represent? *(One item line on an invoice)*
2. Can one invoice appear on multiple rows? Find an example and write down the InvoiceNo. *(Yes — e.g. InvoiceNo 536365 appears on rows 2–8)*
3. What is the earliest and latest date you can find in the InvoiceDate column? *(Expected: 01/12/2010 and 09/12/2011)*
4. What do you notice about some values in the CustomerID column? *(Many blanks — 24.9% of rows have no customer ID)*
5. Find a row where InvoiceNo starts with the letter C. Write down the full InvoiceNo. What might that mean? *(Cancellation — e.g. C536379)*

**Debrief:** Groups present answers verbally. Instructor confirms using the values above. No marking — this is a familiarisation exercise.

---

## Instructor Notes

- This is the first session — pace slowly on the import step. Many students will have never used the `Data → Get Data` ribbon.
- **"DOTCOM POSTAGE"** will appear in the data — if students ask, note it is a shipping fee line item, not a product. Good early discussion on data quality.
- **CustomerID stored as float** (17850.0) — this is a loading artefact. Note it; we fix it properly in Week 5 Power Query.
- December 2011 only runs to the 9th — worth mentioning if students ask about the date range.
