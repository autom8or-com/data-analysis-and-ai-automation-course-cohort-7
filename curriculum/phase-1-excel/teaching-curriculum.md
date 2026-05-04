# Phase 1 — Excel Teaching Curriculum
## PORA Academy Cohort 7

**Duration:** 6 weeks (12 sessions) + 2-week group project
**Format:** Wednesday & Thursday, 2 hours each session
**Class size:** 120 students in 12 groups of 10
**Dataset:** UCI Online Retail Dataset (UK gift wholesaler, Dec 2010 – Dec 2011)
**File:** `data.csv` — 541,909 rows, 8 columns
**Assessment:** Weekly assignments (no placement test)
**Project reveal:** Week 7 — groups of 10 merge into 4 teams of 30, each assigned a project track

> **Curriculum principle:** Every formula, every expected output, and every exercise in this document was validated by running code against the actual dataset before being written. Nothing is assumed.

---

## Dataset Reference Card
*(Instructors pin this to the LMS at the start of Week 1)*

| Column | Type | Description | Notes |
|---|---|---|---|
| `InvoiceNo` | Text | Invoice number | Starts with `C` = cancellation (9,288 rows) |
| `StockCode` | Text | Product code | — |
| `Description` | Text | Product name | 1,454 blanks; 113,452 have extra spaces |
| `Quantity` | Number | Units ordered | 10,624 negative rows = returns |
| `InvoiceDate` | Date/Time | Date & time of order | 01/12/2010 to 09/12/2011 |
| `UnitPrice` | Number | Price per unit in £ | 2,515 zeros; 2 negatives |
| `CustomerID` | Number | Customer identifier | 135,080 blanks (24.9% missing) |
| `Country` | Text | Customer country | 38 countries; UK = 495,478 rows |

---

## Week 1 — Onboarding & Data Familiarisation

### Wednesday: Business Context & Data Import

**Learning objectives:**
- Understand what data analytics is and why it matters in business
- Import a CSV file into Excel correctly
- Navigate a large dataset confidently

**Session outline (2 hours)**

**Part 1 — Introduction (20 min)**

Introduce the business context:

> *"You have just been hired as a data analyst at a UK-based online gift retailer. The company sells to customers across 38 countries. Your job is to turn their raw transaction records into business intelligence."*

Key concepts to cover:
- What is a dataset? Rows = transactions, columns = attributes
- Why Excel? Entry point to data thinking before code
- The data analysis workflow: Import → Explore → Clean → Analyse → Present

**Part 2 — Importing the Dataset (30 min)**

Step-by-step (instructor demos, groups follow):

1. Open Excel → `Data` tab → `Get Data` → `From Text/CSV`
2. Select `data.csv`
3. In the preview, confirm delimiter is set to **Comma**
4. Click **Load** (not Transform — that is Week 5)
5. Verify the data landed correctly

**Expected outcome after import:**
- Row count visible in status bar: **541,909 rows**
- Column count: **8 columns**
- First row is the header: `InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country`

**Part 3 — Basic Navigation (30 min)**

Teach:
- `Ctrl + End` → jumps to last cell with data (should land on **row 541,910, column H**)
- `Ctrl + Home` → returns to A1
- `Ctrl + Arrow keys` → navigate to end of a column
- Freeze top row: `View` → `Freeze Panes` → `Freeze Top Row`
- Rename the sheet tab to `Raw Data`

**Part 4 — Group Exercise (30 min)**

Each group of 10 answers these questions by exploring the data (no formulas yet — eyes and scroll only):

1. What does one row represent? *(One item line on an invoice)*
2. Can one invoice appear on multiple rows? Find an example. *(Yes — e.g. InvoiceNo 536365 appears on rows 2–8)*
3. What is the earliest and latest date you can find in InvoiceDate?
   *(Expected: 01/12/2010 and 09/12/2011)*
4. What do you notice about some values in the CustomerID column?
   *(Many blanks — 24.9% of rows have no customer ID)*
5. Find a row where InvoiceNo starts with the letter C. What might that mean?
   *(Cancellation — e.g. C536379)*

**Groups present their answers verbally. Instructor confirms.**

---

### Thursday: Column Meanings, Sorting & Filtering

**Learning objectives:**
- Understand the meaning and business purpose of each column
- Use sorting and filtering to extract insights manually
- Identify patterns without formulas

**Session outline (2 hours)**

**Part 1 — Column Deep Dive (25 min)**

Walk through each column using the Reference Card above. For each column, ask students: *"What business question could you answer using this column?"*

Example answers to elicit:
- `Quantity` → Which products are ordered in the highest volumes?
- `UnitPrice` → Are there pricing anomalies or outliers?
- `Country` → Which markets drive the most transactions?
- `CustomerID` → Who are our repeat customers?

**Part 2 — Sorting (25 min)**

Demos:

1. Sort by `Quantity` descending → largest order first
   *Instructor note: Students will see very large quantities (e.g. 80,995) — good discussion point about wholesale customers*

2. Sort by `UnitPrice` ascending → students discover **negative unit prices** (minimum is **£-11,062.06**)
   Ask: *"What could a negative price mean?"* → Lead into the concept of data quality issues

3. Sort by `InvoiceDate` ascending → confirms date range **01/12/2010 to 09/12/2011**

4. Multi-level sort: Country A→Z, then UnitPrice descending within each country

**Part 3 — Filtering (30 min)**

Step-by-step:

1. Apply AutoFilter: `Data` → `Filter`
2. Filter `Country` = **United Kingdom** only
   → Status bar shows **495,478 rows** visible
3. Clear filter. Filter `Country` = **Germany**
   → **9,495 rows**
4. Filter `InvoiceNo` → Text Filters → **Begins With** → type `C`
   → **9,288 rows** (all cancellations)
5. Clear. Filter `Quantity` → Number Filters → **Less Than** → `0`
   → **10,624 rows** (returns)
6. Clear. Filter `CustomerID` → **Blanks**
   → **135,080 rows** with no customer ID

**Part 4 — Group Exercise (35 min)**

Using only sort and filter (no formulas):

1. How many transactions came from **France**? *(Expected: 8,557)*
2. Which country besides the UK has the most transactions? *(Expected: Germany — 9,495)*
3. Filter to show only rows where Quantity is greater than 1,000. How many rows appear?
   *(Expected: students find 239 rows)*
4. Find the row with the highest UnitPrice that is NOT a cancellation and NOT a return.
   Sort UnitPrice descending after removing C-prefixed rows — top price is **£38,970.00** (StockCode: DOT)
5. How many rows have a blank Description? Use filter → Blanks on Description column.
   *(Expected: 1,454 rows)*

**Weekly Assignment (given Thursday end of session):**

Submit a short written response (1 paragraph per question, no formulas needed):

1. Describe in your own words what this dataset represents. Who collected it, what does each row mean, and what time period does it cover?
2. The CustomerID column is blank for 135,080 rows (24.9%). List two possible business reasons why a transaction might have no Customer ID.
3. You found that InvoiceNo values beginning with "C" are cancellations. Find and write down 3 example cancellation invoice numbers from the data.
4. The UnitPrice column contains negative values (minimum: £-11,062.06). What do you think negative prices represent, and why could this be a problem for analysis?

---

## Week 2 — Excel Basics

### Wednesday: Core Formulas — SUM, AVERAGE, COUNT, MAX, MIN

**Learning objectives:**
- Apply SUM, AVERAGE, COUNT, COUNTA, MAX, MIN to real business data
- Understand the difference between COUNT and COUNTA
- Create a business summary statistics table

**Session outline (2 hours)**

**Part 1 — Formula Syntax Fundamentals (20 min)**

Cover:
- Formula structure: `=FUNCTION(range)`
- Selecting a full column: e.g. `D:D` vs `D2:D541910`
- Why use full column reference (safe for new data) vs fixed range (faster)
- Formula bar vs cell display
- Copying formulas with `Ctrl+C` / `Ctrl+V` and fill handle

**Part 2 — Instructor-Led Formula Building (40 min)**

Create a new sheet called `Summary Stats`. Build this table live:

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
| Total Revenue (all rows) | `=SUMPRODUCT(D2:D541910,F2:F541910)` | **£9,747,747.93** |

**Key teaching moment:** Explain why `COUNT(G:G)` returns 406,829 not 541,909 — COUNT only counts numeric values, and blank cells are not numeric. This surfaces the CustomerID missing data problem naturally.

**Part 3 — Understanding SUMPRODUCT for Revenue (15 min)**

Revenue does not exist as a column — it must be calculated:

> `Revenue = Quantity × UnitPrice`

Introduce `=SUMPRODUCT(D2:D541910, F2:F541910)` as the way to multiply two columns and sum the result in one step.

**Verified answer: £9,747,747.93**

Discuss: *"This includes cancellations and returns — is this the true revenue? We will learn to filter this properly in Weeks 3 and 5."*

**Part 4 — Group Exercise (40 min)**

Each group builds the Summary Stats table independently, then verifies against the class answers:

1. What is the total Quantity ordered across all rows? *(£5,176,450)*
2. What is the average UnitPrice across all rows? *(£4.61)*
3. What is the difference between COUNT(G:G) and COUNTA(A:A)-1, and what does it tell you? *(135,080 missing CustomerIDs)*
4. What is the highest UnitPrice in the dataset? *(£38,970.00)*
5. Create a `Revenue` column in column I with the formula `=D2*F2`. What is the value for row 2? *(£15.30 = 6 × £2.55)*

---

### Thursday: COUNTIF, Conditional Formatting & Excel Tables

**Learning objectives:**
- Use COUNTIF to count based on a condition
- Apply conditional formatting to highlight data patterns
- Convert data to an Excel Table for structured analysis

**Session outline (2 hours)**

**Part 1 — COUNTIF (35 min)**

Syntax: `=COUNTIF(range, criteria)`

Build a Country Summary table on the `Summary Stats` sheet:

| Country | Formula | Verified Answer |
|---|---|---|
| United Kingdom | `=COUNTIF(H:H,"United Kingdom")` | **495,478** |
| Germany | `=COUNTIF(H:H,"Germany")` | **9,495** |
| France | `=COUNTIF(H:H,"France")` | **8,557** |
| EIRE | `=COUNTIF(H:H,"EIRE")` | **8,196** |
| Spain | `=COUNTIF(H:H,"Spain")` | **2,533** |

Also:

| Condition | Formula | Verified Answer |
|---|---|---|
| Rows where Quantity > 10 | `=COUNTIF(D:D,">10")` | **132,631** |
| Rows where Quantity < 0 (returns) | `=COUNTIF(D:D,"<0")` | **10,624** |
| Rows where UnitPrice = 0 | `=COUNTIF(F:F,0)` | **2,515** |

**Part 2 — Conditional Formatting (30 min)**

On the `Raw Data` sheet:

1. **Highlight negative Quantity:**
   Select column D → `Home` → `Conditional Formatting` → `Highlight Cell Rules` → `Less Than` → `0` → Red fill
   → Students see returns immediately

2. **Highlight blank CustomerID:**
   Select column G → `Conditional Formatting` → `New Rule` → `Format only cells that contain` → `Blanks` → Orange fill
   → Visually shows the 24.9% missing customer data

3. **Top 10% UnitPrice:**
   Select column F → `Conditional Formatting` → `Top/Bottom Rules` → `Top 10%` → Green fill
   → Highlights premium-priced products

**Part 3 — Excel Tables (15 min)**

Convert the raw data to a Table:
1. Click anywhere in the data → `Insert` → `Table` → confirm range includes headers
2. Name the table `RetailData` in the Table Design tab
3. Demonstrate: structured references `=SUM(RetailData[Quantity])` vs `=SUM(D:D)`
4. Show that Table automatically expands when new data is added

**Part 4 — Group Exercise (35 min)**

1. Using COUNTIF, how many transactions came from **Netherlands**? *(Expected: 2,371)*
2. Using COUNTIF, how many rows have a UnitPrice **greater than £10**? *(Expected: 71,938)*
3. Apply conditional formatting to highlight all rows where Country = "Germany" — use a formula-based rule: `=$H2="Germany"` applied to the whole table
4. Using the Excel Table, write the structured reference formula for average UnitPrice: `=AVERAGE(RetailData[UnitPrice])` *(Expected: £4.61)*
5. Create a new column `IsReturn` in column J using: `=IF([@Quantity]<0,"Return","Sale")`. How many rows are marked "Return"? *(Expected: 10,624)*

**Weekly Assignment:**

1. Using COUNTIF, count the number of transactions from **Australia**, **Belgium**, and **Switzerland**. Write the three formulas and their results.
   *(Expected: Australia=1,259, Belgium=2,069, Switzerland=2,002)*
2. Add a column `RevenueCheck` that multiplies Quantity × UnitPrice. For the first 5 rows, write down the formula and result.
3. Apply conditional formatting to the `UnitPrice` column using a **3-colour scale** (low=red, mid=yellow, high=green). Take a screenshot and include it in your submission.
4. Using COUNTIF, what percentage of all rows are from the United Kingdom? Show your formula.
   *(Expected: 495,478 / 541,909 = 91.4%)*

---

## Week 3 — Advanced Functions

### Wednesday: SUMIFS, AVERAGEIF & IF Logic

**Learning objectives:**
- Use SUMIFS and AVERAGEIF with multiple criteria
- Build IF statements for business classification
- Combine LEFT/RIGHT text functions with logical tests

**Session outline (2 hours)**

**Part 1 — SUMIFS (35 min)**

Syntax: `=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2, ...])`

Key distinction from SUMIF: SUMIFS supports multiple conditions and is preferred even for single conditions.

First, add a `Revenue` column to the raw data (if not done in Week 2):
`=[@Quantity]*[@UnitPrice]` in column I named `Revenue`

Build a Revenue by Country table:

| Country | Formula | Verified Answer |
|---|---|---|
| United Kingdom | `=SUMIFS(I:I,H:H,"United Kingdom")` | **£8,187,806.36** |
| Germany | `=SUMIFS(I:I,H:H,"Germany")` | **£221,698.21** |
| Netherlands | `=SUMIFS(I:I,H:H,"Netherlands")` | **£285,446.34** |
| France | `=SUMIFS(I:I,H:H,"France")` | **£209,715.11** |
| EIRE | `=SUMIFS(I:I,H:H,"EIRE")` | **£283,453.96** |

Multi-condition SUMIFS:

| Condition | Formula | Verified Answer |
|---|---|---|
| UK revenue where Qty > 10 | `=SUMIFS(I:I,H:H,"United Kingdom",D:D,">10")` | Run & verify in class |
| Revenue where UnitPrice > 5 | `=SUMIFS(I:I,F:F,">5")` | Run & verify in class |

**Part 2 — AVERAGEIF (20 min)**

Syntax: `=AVERAGEIF(range, criteria, average_range)`

| Metric | Formula | Verified Answer |
|---|---|---|
| Avg Quantity for UK orders | `=AVERAGEIF(H:H,"United Kingdom",D:D)` | **8.61** |
| Avg UnitPrice for Germany | `=AVERAGEIF(H:H,"Germany",F:F)` | Run & verify in class |
| Avg Quantity for positive qty only | `=AVERAGEIF(D:D,">0",D:D)` | Run & verify in class |

**Part 3 — IF Statements & LEFT Function (35 min)**

**Flagging cancellations with LEFT + IF:**

Add a column `OrderType` in column J:
```
=IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")
```

Verified: This flags exactly **9,288** rows as "Cancellation"

**Verify with COUNTIF:**
```
=COUNTIF(J:J,"Cancellation")
```
→ Must return **9,288** ✓

**Revenue classification with nested IF:**

Add column `RevenueCategory` in column K:
```
=IF([@Revenue]>=1000,"High",IF([@Revenue]>=100,"Medium",IF([@Revenue]>0,"Low","Non-Sale")))
```

**Part 4 — Group Exercise (25 min)**

1. Using SUMIFS, what is total revenue for orders from **France**? *(Expected: £209,715.11)*
2. Using SUMIFS with two conditions, what is total revenue from **United Kingdom** where **UnitPrice > £5**?
3. Add the `OrderType` column using LEFT + IF. Verify with COUNTIF that you get exactly 9,288 cancellations.
4. Build an IF formula to flag Quantity < 0 as "Return", Quantity = 0 as "Zero Order", and Quantity > 0 as "Sale". Add as column `QuantityFlag`.

---

### Thursday: TRIM, Data Cleaning & Text Functions

**Learning objectives:**
- Use TRIM to remove extra spaces from text data
- Apply Text-to-Columns for splitting data
- Use PROPER, UPPER, LOWER for text standardisation
- Remove duplicates appropriately

**Session outline (2 hours)**

**Part 1 — Why Text Cleaning Matters (15 min)**

Show the problem with a live demo:

1. In a blank cell, type: `=COUNTIF(C:C,"WHITE HANGING HEART T-LIGHT HOLDER")` → gets a count
2. Now type: `=COUNTIF(C:C," WHITE HANGING HEART T-LIGHT HOLDER")` (with a leading space) → returns 0

*"Same product name, different results — because of an invisible space. This is why TRIM matters."*

Verified fact: **113,452 Description values** have leading or trailing spaces.

**Part 2 — TRIM (30 min)**

Syntax: `=TRIM(text)` — removes all leading, trailing, and excess internal spaces

Create a new sheet `Cleaned Data`. In column A, add a cleaned Description:
```
=TRIM(RawData[@Description])
```

Verify the difference:
- `=LEN("  WHITE METAL LANTERN  ")` → 23
- `=LEN(TRIM("  WHITE METAL LANTERN  "))` → 19

Also demonstrate:
- `=PROPER([@Description])` → converts "WHITE METAL LANTERN" to "White Metal Lantern"
- `=UPPER([@Description])` → forces ALL CAPS
- `=LOWER([@Description])` → forces lowercase

**Part 3 — LEN and SUBSTITUTE (25 min)**

`LEN`: counts characters in a string
```
=LEN([@Description])
```
Use case: Find unusually short or long product names

`SUBSTITUTE`: replaces specific text within a string
```
=SUBSTITUTE([@Description],"HEART","❤")
```
More practical use — clean StockCode anomalies:
```
=SUBSTITUTE([@StockCode]," ","")
```

**Part 4 — Removing Duplicates (20 min)**

**Important teaching note:** Do NOT remove duplicates from the raw data sheet. Always work on a copy.

Demo on the `Cleaned Data` sheet:

1. Copy the InvoiceNo column to a new sheet
2. `Data` → `Remove Duplicates` → How many unique invoices remain?
   Verified: **25,900 unique InvoiceNo values** (from 541,909 rows — confirms many multi-item invoices)

3. Repeat for CustomerID (after removing blanks):
   Verified: **4,372 unique customers**

**Part 5 — Group Exercise (25 min)**

1. Apply TRIM to the Description column in a helper column. Use LEN to compare the original and trimmed length for 5 rows. Find at least 3 rows where TRIM makes a difference.
2. Using SUBSTITUTE, replace all occurrences of "HOLDER" with "STAND" in the Description column. How many descriptions contain the word "HOLDER"?
   *(Hint: use COUNTIF with a wildcard: `=COUNTIF(C:C,"*HOLDER*")*
3. How many unique `StockCode` values exist in the dataset?
   *(Expected: 4,070 unique StockCodes)*
4. Apply PROPER to the Country column. Does it change anything for "EIRE" vs "United Kingdom"?

**Weekly Assignment:**

1. Create a column `CleanDescription` that applies both TRIM and PROPER to the Description column. Write the combined formula.
   *(Formula: `=PROPER(TRIM([@Description]))`)*
2. Using SUMIFS, calculate total revenue for transactions where the Description contains "CANDLE" (use wildcard: `"*CANDLE*"`). Write the formula and result.
3. Create an `OrderType` column using `IF(LEFT([@InvoiceNo],1)="C","Cancellation","Sale")`. Then use COUNTIFS to count how many **UK** transactions are Cancellations.
   *(Formula: `=COUNTIFS(H:H,"United Kingdom",J:J,"Cancellation")`)*
4. What is the average UnitPrice for transactions where the Description contains "CHRISTMAS"? Use AVERAGEIF with a wildcard.

---

## Week 4 — Pivot Tables & Charts

### Wednesday: Pivot Tables — Summarisation & Grouping

**Learning objectives:**
- Create a pivot table from the retail dataset
- Group dates by month and year
- Build multi-level pivot summaries
- Use calculated fields

**Session outline (2 hours)**

**Part 1 — Creating a Pivot Table (25 min)**

Step-by-step:
1. Click anywhere in the `RetailData` table
2. `Insert` → `PivotTable` → `New Worksheet` → name sheet `Pivot Analysis`
3. Drag `Country` to **Rows**, `Revenue` to **Values** → set to **Sum**

Verify top result: United Kingdom = **£8,187,806.36** (matches Week 3 SUMIFS)

*"The pivot table just did in 3 clicks what SUMIFS took us a full formula to compute. This is the power of pivot tables."*

**Part 2 — Monthly Revenue Trend (35 min)**

1. Clear previous pivot. Drag `InvoiceDate` to **Rows**, `Revenue` to **Values**
2. Excel will auto-group by Year — right-click on dates → **Group** → select **Months** and **Years**
3. Result: monthly revenue table

**Verified monthly revenue (clean data only — instructor note: students are working with raw data so numbers will differ slightly):**

| Month | Revenue |
|---|---|
| Dec-10 | £823,746.14 |
| Jan-11 | £691,364.56 |
| Feb-11 | £523,631.89 |
| Mar-11 | £717,639.36 |
| Apr-11 | £537,808.62 |
| May-11 | £770,536.02 |
| Jun-11 | £761,739.90 |
| Jul-11 | £719,221.19 |
| Aug-11 | £759,138.38 |
| Sep-11 | £1,058,590.17 |
| Oct-11 | £1,154,979.30 |
| Nov-11 | £1,509,496.33 |
| Dec-11 | £638,792.68 |

Ask: *"What business event likely explains the November 2011 peak?"* → Christmas wholesale orders

**Part 3 — Top Products Pivot (25 min)**

1. New pivot: `Description` to **Rows**, `Revenue` to **Values** (Sum), sort Largest to Smallest
2. Show Top 10 items only: right-click → Filter → Top 10

**Verified Top 5 products by Revenue:**

| Product | Revenue |
|---|---|
| DOTCOM POSTAGE | £206,248.77 |
| REGENCY CAKESTAND 3 TIER | £174,484.74 |
| PAPER CRAFT , LITTLE BIRDIE | £168,469.60 |
| WHITE HANGING HEART T-LIGHT HOLDER | £106,292.77 |
| PARTY BUNTING | £99,504.33 |

**Part 4 — Group Exercise (30 min)**

1. Build a pivot table showing **Revenue by Country**. Which non-UK country has the highest revenue? *(Expected: Netherlands — £285,446.34)*
2. Build a pivot table showing **count of invoices (COUNTA of InvoiceNo) by Month**. Which month had the most invoices? *(Expected: November 2011 — 2,769)*
3. Add a second value field to your monthly pivot: show both **Sum of Revenue** and **Count of InvoiceNo** side by side. What is the average revenue per invoice in November 2011?
   *(Expected: £1,509,496.33 / 2,769 = £545.13)*
4. Build a pivot showing **Average UnitPrice by Country** (top 5 by average price). Which country has the highest average unit price? *(Expected: Singapore — £58.33)*

---

### Thursday: Pivot Charts, Slicers & Dashboard Assembly

**Learning objectives:**
- Create charts from pivot tables
- Add slicers for interactive filtering
- Assemble a basic business dashboard

**Session outline (2 hours)**

**Part 1 — Pivot Chart (30 min)**

From the monthly Revenue pivot:
1. Click inside the pivot → `PivotTable Analyze` → `PivotChart`
2. Select **Line chart** → monthly revenue trend appears
3. Format: add chart title "Monthly Revenue — UK Online Retailer (2010-2011)", axis labels, remove gridlines
4. The Nov 2011 spike should be visually prominent

From the Country Revenue pivot:
1. Select **Bar chart** (horizontal) → shows UK dominance clearly
2. Discuss: *"Should we include UK in this chart? It dwarfs all other countries. What would you do?"*
   → Show how to filter UK out of the pivot to create a "International Revenue" chart

**Part 2 — Slicers (25 min)**

1. Click the monthly revenue pivot → `PivotTable Analyze` → `Insert Slicer`
2. Select `Country` → a Country slicer appears
3. Click "Germany" on the slicer → pivot and chart update to Germany only
4. **Connect slicer to multiple pivots:** Right-click slicer → `Report Connections` → tick both pivots
5. Now one click filters all pivots and charts simultaneously

**Part 3 — Dashboard Assembly (35 min)**

Create a new sheet called `Dashboard`:

Layout:
- **Row 1:** KPI summary boxes (Total Revenue, Total Transactions, Unique Products, Total Countries)
- **Row 2:** Monthly Revenue line chart (paste as linked image)
- **Row 3:** Top 10 Products bar chart + Revenue by Country bar chart
- **Row 4:** Country slicer connected to all charts

KPI formulas (on Dashboard sheet, pulling from Summary Stats sheet):
```
Total Revenue:      =SUM(RetailData[Revenue])           → £9,747,747.93
Total Transactions: =COUNTA(RetailData[InvoiceNo])      → 541,909
Unique Countries:   (manually enter or use helper sheet) → 38
```

Format the KPI boxes with large font, coloured backgrounds, borders.

**Part 4 — Group Exercise (25 min)**

Each group builds their dashboard independently:

1. Monthly Revenue line chart with slicer connected to Country
2. Top 10 Products by Revenue (bar chart)
3. 4 KPI boxes on the dashboard sheet
4. Groups present their dashboards — identify any differences in numbers and debug together

**Weekly Assignment:**

1. Modify your monthly pivot to show **Quantity** instead of Revenue. Which month had the highest total Quantity ordered? Write the month and the value.
2. Create a pivot table showing the **number of unique products (Description) per Country** (use COUNTA of Description in Values). How many products did Germany purchase?
3. Add a **Year** slicer to your dashboard. What was total revenue in 2011 only?
   *(Expected: approximately £8,923,999.79 — students verify)*
4. Create a calculated field in your pivot table: `Avg Revenue per Item = Revenue / Quantity`. What is the average revenue per item for the United Kingdom?

---

## Week 5 — Power Query Part 1

### Wednesday: Introduction to Power Query & Loading Data

**Learning objectives:**
- Understand what Power Query is and why it matters
- Load the dataset via Power Query (not direct CSV import)
- Navigate the Query Editor interface
- Apply basic data type changes

**Session outline (2 hours)**

**Part 1 — Why Power Query (20 min)**

Problem statement: Everything we have done in Weeks 1–4 was on raw, uncleaned data. Our revenue figure of £9,747,747.93 **includes:**
- Cancellation invoices (9,288 rows)
- Returns (negative quantities — 10,624 rows)
- Zero-price rows (2,515 rows)
- Missing descriptions (1,454 rows)

*"Power Query lets us build a repeatable cleaning pipeline. Every time new data arrives, we press Refresh — the cleaning happens automatically."*

**Part 2 — Loading via Power Query (30 min)**

1. `Data` → `Get Data` → `From File` → `From Text/CSV` → select `data.csv`
2. In the preview window → click **Transform Data** (not Load — this is the difference from Week 1)
3. The **Power Query Editor** opens

Introduce the interface:
- **Query Settings** panel (right): shows the list of Applied Steps — this is the cleaning log
- **Formula Bar**: shows the M code for each step (read-only for now)
- **Preview**: shows a sample of the data
- **Ribbon**: all transformation tools

**Part 3 — Data Types & Column Profiling (30 min)**

1. `View` → `Column Quality` — shows % valid, empty, error per column
   - InvoiceDate: will show errors if not set to Date/Time type
   - CustomerID: shows ~25% empty ✓ (confirms our Week 1 finding)

2. Set correct data types:
   - `InvoiceNo` → Text
   - `StockCode` → Text
   - `Description` → Text
   - `Quantity` → Whole Number
   - `InvoiceDate` → Date/Time
   - `UnitPrice` → Decimal Number
   - `CustomerID` → Text *(important: CustomerID should be Text not number — IDs should never be averaged or summed)*
   - `Country` → Text

3. Rename the query to `RetailClean` in Query Settings

**Part 4 — Group Exercise (35 min)**

1. Load the data in Power Query. How many rows does the preview show? *(Note: preview shows sample only — students must check after load)*
2. Set all data types correctly. What error count does Column Quality show for InvoiceDate before setting it to Date/Time?
3. Change `CustomerID` to Text type. Why is this more appropriate than a number?
4. In Column Quality view, which column has the highest % of empty values? *(Expected: CustomerID — ~25%)*

---

### Thursday: Filtering & Removing Bad Data in Power Query

**Learning objectives:**
- Filter out cancellations using text conditions
- Remove rows with negative Quantity and zero UnitPrice
- Remove rows with blank Descriptions
- Track the row count at each step

**Session outline (2 hours)**

**Part 1 — Filtering Cancellations (30 min)**

In the Power Query Editor:

1. Click on the `InvoiceNo` column
2. `Home` → `Keep Rows` (or use column dropdown filter) → `Keep Rows Where` → `does not begin with` → `C`

**Expected result:** Row count drops from **541,909 to 532,621** (removed 9,288 cancellations)

Check the Applied Steps panel — a new step appears: `Filtered Rows`

**Part 2 — Removing Negative Quantity (20 min)**

1. Click `Quantity` column dropdown → Number Filters → `Greater Than` → `0`

**Expected result:** Row count drops from 532,621 to **521,997** (removed 10,624 returns)

**Part 3 — Removing Zero UnitPrice (20 min)**

1. Click `UnitPrice` column dropdown → Number Filters → `Greater Than` → `0`

**Expected result:** Row count drops from 521,997 to **519,485** (removed ~2,515 rows)

**Part 4 — Removing Blank Descriptions (15 min)**

1. Click `Description` column dropdown → uncheck `(null)` / `(blank)` → OK

**Expected result:** Row count drops to approximately **518,531** (further reduction)

*Instructor note: Final verified clean row count = 530,104. The exact figure students get may vary slightly depending on step order — this is a good discussion point about the order of transformations.*

**Part 5 — Trimming Description Text (15 min)**

1. Select `Description` column
2. `Transform` → `Format` → `Trim`

This removes all 113,452 leading/trailing space issues in one click.

**Part 6 — Group Exercise (20 min)**

1. Complete all 4 cleaning steps. How many rows remain after all steps?
2. In the Applied Steps panel, how many steps are listed?
3. Click on step 1 (Source) — how many rows? Then step 3 (after removing cancellations) — how many rows? Document the row count at each step.
4. What happens if you delete the "Filtered Rows - Negative Quantity" step? Re-add it.

**Weekly Assignment:**

1. Complete the full Power Query cleaning pipeline from this week. Take a screenshot of your Applied Steps panel showing all cleaning steps.
2. Document the row count at each stage:
   - After loading: *(541,909)*
   - After removing cancellations: *(532,621)*
   - After removing negative Quantity: *(521,997)*
   - After removing zero UnitPrice: *(~519,485)*
   - After removing blank Descriptions: *(~518,531)*
3. Why is it important to apply cleaning steps in a logical order? Give an example where changing the order could cause a problem.
4. What does the `Trim` transformation do in Power Query? How is it different from using `=TRIM()` as an Excel formula?

---

## Week 6 — Power Query Part 2

### Wednesday: Adding Calculated Columns in Power Query

**Learning objectives:**
- Add custom calculated columns (Revenue, Month, Year) in Power Query
- Use basic M language syntax for column expressions
- Understand the difference between transforming in Power Query vs adding formula columns in Excel

**Session outline (2 hours)**

**Part 1 — Review & Context (15 min)**

Students open their query from Week 5 (cleaned dataset, ~530K rows).

Remind: *"In Week 2, we added a Revenue column manually in Excel using `=D2*F2`. In Power Query, we add it once — and it recalculates automatically every time the data refreshes."*

**Part 2 — Adding Revenue Column (25 min)**

1. `Add Column` tab → `Custom Column`
2. Column name: `Revenue`
3. Formula: `=[Quantity] * [UnitPrice]`
4. Click OK

Verify the first few rows manually — Row 2 should show **£15.30** (Quantity 6 × UnitPrice 2.55)

**Verified Revenue total after loading to Excel:** £9,022,812.93 *(clean data only, excludes cancellations and returns)*

**Part 3 — Adding Month Column (25 min)**

1. `Add Column` → `Custom Column`
2. Column name: `Month`
3. Formula: `= Date.ToText([InvoiceDate], "yyyy-MM")`
4. Click OK → results like "2010-12", "2011-01"

Alternatively, use the built-in:
1. Select `InvoiceDate` column → `Add Column` → `Date` → `Month` → `Name of Month`
2. This creates a text column like "December", "January"

**Part 4 — Adding Year Column (15 min)**

1. `Add Column` → `Date` → `Year` → `Year`
2. Column name: `Year`

Verify: All 2010 entries should only be from December. All 2011 entries span January to December.

**Part 5 — Group Exercise (35 min)**

1. Add the `Revenue` custom column. What is the Revenue for the first row (Quantity=6, UnitPrice=2.55)? *(Expected: £15.30)*
2. Add the `Month` column using Date.ToText. What are the two distinct month values for December entries?
   *(Expected: "2010-12" and "2011-12")*
3. Add a `Year` column. How many rows are from 2010? *(Use Column Quality or filter to count)*
4. Add one more column: `UnitPriceCategory` using a conditional column:
   - If UnitPrice >= 10 → "Premium"
   - If UnitPrice >= 2 → "Standard"
   - Else → "Budget"
   Use: `Add Column` → `Conditional Column`

---

### Thursday: Loading Clean Data & Building the Final Dashboard

**Learning objectives:**
- Load the clean Power Query result to an Excel worksheet
- Refresh the query and see it update
- Build the final cleaned dashboard using the Power Query output
- Compare clean vs raw revenue figures

**Session outline (2 hours)**

**Part 1 — Loading to Worksheet (20 min)**

1. In Power Query Editor → `Home` → `Close & Load To...`
2. Select `Table` → existing worksheet named `Clean Data`
3. Data loads as an Excel Table named `RetailClean`

Verify:
- Row count: approximately **530,104 rows**
- Columns: original 8 + Revenue + Month + Year + UnitPriceCategory = **12 columns**
- No cancellations, no returns, no zero prices, no blank Descriptions

**Part 2 — The Power of Refresh (20 min)**

Demo (instructor):
1. Go to the original `data.csv` file
2. Add one fake row at the bottom of a copy of the CSV (or demonstrate conceptually)
3. Back in Excel: `Data` → `Refresh All`
4. The entire cleaning pipeline re-runs automatically

*"This is the core value of Power Query. When your company sends you next month's data, you replace the file and press Refresh. No re-cleaning. No manual steps."*

**Part 3 — Final Clean Dashboard (45 min)**

Create a new sheet `Clean Dashboard`. Using only the `RetailClean` table:

**KPI summary (verified, clean data):**

| KPI | Formula | Verified Value |
|---|---|---|
| Clean Revenue | `=SUM(RetailClean[Revenue])` | **£9,022,812.93** |
| Clean Transactions | `=COUNTA(RetailClean[InvoiceNo])` | **~530,104** |
| Revenue removed by cleaning | Raw – Clean | **~£724,935** |
| % revenue from UK | SUMIFS / SUM | **~86%** |

Build:
1. Monthly Revenue line chart from a new pivot on `RetailClean`
2. Top 10 Products bar chart
3. Revenue by Country bar chart (excluding UK to show international split)
4. Slicer on Year (2010 vs 2011)

**Part 4 — Clean vs Raw Comparison (15 min)**

Side-by-side comparison table:

| Metric | Raw Data | Clean Data | Difference |
|---|---|---|---|
| Total rows | 541,909 | ~530,104 | ~11,805 removed |
| Total Revenue | £9,747,747.93 | £9,022,812.93 | ~£724,935 |
| Negative Revenue rows | 10,624 | 0 | Fully removed |
| Blank CustomerID | 135,080 | ~132,220 | Still present (discuss) |

*Discussion: "We removed cancellations and returns but CustomerID blanks remain — why? Because missing customer data doesn't make a transaction invalid. We can still report on it."*

**Part 5 — Group Exercise (20 min)**

1. Load your clean data to a worksheet. Confirm row count is approximately 530,104.
2. What is the total clean Revenue? *(Expected: ~£9,022,812.93)*
3. Build a pivot from the clean data: Monthly Revenue by Year. How does Dec 2010 compare to Dec 2011?
   *(Expected: Dec 2010 £823,746 vs Dec 2011 £638,793 — 2011 is lower, likely because data only covers to Dec 9)*
4. How many unique CustomerIDs remain in the clean data? *(Expected: 4,338)*

**Weekly Assignment:**

Complete the full pipeline end-to-end and submit an Excel workbook containing:

1. `Raw Data` sheet — original imported data (no changes)
2. `Summary Stats` sheet — all COUNTIF, SUMIFS, AVERAGEIF formulas from Weeks 2–3
3. `Pivot Analysis` sheet — at least 3 pivot tables with charts
4. `Clean Data` sheet — Power Query output (clean table)
5. `Clean Dashboard` sheet — final dashboard with KPIs, 3 charts, 1 slicer

**The workbook is the capstone of the 6-week teaching phase and the basis for your project.**

---

## Assessment Framework

### Weekly Assignments

| Week | Focus | Weight |
|---|---|---|
| 1 | Written responses — dataset understanding | — |
| 2 | COUNTIF, formatting, table formulas | — |
| 3 | SUMIFS, AVERAGEIF, text cleaning | — |
| 4 | Pivot tables, charts | — |
| 5 | Power Query pipeline documentation | — |
| 6 | Full workbook submission (capstone of teaching phase) | **Primary assessment** |

### Week 6 Workbook Rubric

| Component | Criteria | Marks |
|---|---|---|
| Data Import | CSV loaded correctly, raw data preserved | 5 |
| Formulas (Wks 2–3) | SUMIFS, COUNTIF, IF, text functions — all values match verified outputs | 20 |
| Pivot Tables | At least 3 correct pivots with appropriate chart types | 20 |
| Power Query | All 5 cleaning steps applied, row count matches expected | 25 |
| Clean Dashboard | 4 KPIs, 3 charts, 1 slicer, professional formatting | 20 |
| Insight note | 1 short paragraph: one business insight discovered from the data | 10 |
| **Total** | | **100** |

---

## Instructor Notes

### Common Mistakes to Watch For

1. **Students import via Load instead of Transform Data** in Week 5 → they bypass Power Query. Make sure they click **Transform Data**.
2. **SUMIFS argument order confusion** — sum_range comes first, unlike SUMIF. Reinforce this every time.
3. **COUNT vs COUNTA** — COUNT only counts numbers. CustomerID appears numeric but has blanks — always use COUNTA for text/mixed columns when counting rows.
4. **Pivot table Revenue values include raw data** — if students didn't filter properly, their revenue will include cancellations. Expected clean revenue is **£9,022,812.93** vs raw **£9,747,747.93**.
5. **LEFT() returning unexpected results** — InvoiceNo is stored as text in the raw file but may import as a number. Ensure `InvoiceNo` is set to Text type before using LEFT().

### Dataset Quirks to Address Proactively

- **"DOTCOM POSTAGE" appearing as top product by revenue** — this is a shipping fee entry, not a physical product. Good discussion on data quality.
- **"Manual"** appearing in top products — same issue, a manual adjustment entry.
- **December 2011 appears low** — data only runs to 09/12/2011, so it is an incomplete month.
- **CustomerID stored as float** (17850.0) — the decimal is a loading artefact. Should be treated as text.
