# Week 01 — Thursday: Column Meanings, Sorting & Filtering
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 01 of 6
**Session:** Thursday
**Topic:** Column Meanings, Sorting & Filtering

---

## Pre-Session Checklist

- [ ] Dataset loaded from Wednesday session (or re-import if needed)
- [ ] Demo workbook open: `lecture-materials/week-01-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-01-thu-exercises.xlsx`
- [ ] Projector / screen sharing ready
- [ ] Weekly assignment text ready to share at session end

---

## Learning Objectives

By the end of this session, students will be able to:

1. Understand the meaning and business purpose of each column
2. Use sorting and filtering to extract insights manually
3. Identify data quality patterns without formulas

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:25 | Part 1 — Column deep dive | Walk through Reference Card |
| 0:25 – 0:50 | Part 2 — Sorting demos | 4 sort scenarios |
| 0:50 – 1:20 | Part 3 — Filtering demos | 6 filter scenarios with verified counts |
| 1:20 – 1:55 | Part 4 — Group exercise | Sort + filter questions |
| 1:55 – 2:00 | Assignment intro & close | Distribute assignment text |

---

## Concept 1 — Column Deep Dive (25 min)

**What to demonstrate:**

Walk through each column using the Dataset Reference Card. For each column, ask students: *"What business question could you answer using this column?"*

| Column | Type | Key fact | Business question |
|---|---|---|---|
| `InvoiceNo` | Text | Starts with `C` = cancellation (9,288 rows) | How many orders were cancelled? |
| `StockCode` | Text | Product identifier | Which products are most popular? |
| `Description` | Text | 1,454 blanks; 113,452 have extra spaces | What are our product categories? |
| `Quantity` | Number | 10,624 negative rows = returns | How many items were returned? |
| `InvoiceDate` | Date/Time | 01/12/2010 to 09/12/2011 | When is our peak trading period? |
| `UnitPrice` | Number | 2,515 zeros; 2 negatives | What is the price range? |
| `CustomerID` | Number | 135,080 blanks (24.9% missing) | Who are our repeat customers? |
| `Country` | Text | 38 countries; UK = 495,478 rows | Which markets drive revenue? |

**Expected output / verified value:** Discussion only.

**Common mistakes to watch for:** Students assume CustomerID is always present. Highlight the 24.9% missing figure early — it will matter throughout the course.

---

## Concept 2 — Sorting (25 min)

**What to demonstrate:**

1. Sort `Quantity` descending → largest order first
   - *Students will see very large quantities (e.g. 80,995) — good discussion point about wholesale customers*

2. Sort `UnitPrice` ascending → students discover **negative unit prices** (minimum is **£-11,062.06**)
   - Ask: *"What could a negative price mean?"* → data quality discussion

3. Sort `InvoiceDate` ascending → confirms date range **01/12/2010 to 09/12/2011**

4. Multi-level sort: Country A→Z, then UnitPrice descending within each country

**Expected output / verified values:**
- Lowest UnitPrice: **£-11,062.06**
- Date range confirmed: **01/12/2010 to 09/12/2011**

**Common mistakes to watch for:** Multi-level sort — students often add levels in the wrong order. Remind them the first sort key is the primary sort (Country), second key breaks ties within it (UnitPrice).

---

## Concept 3 — Filtering (30 min)

**What to demonstrate:**

1. Apply AutoFilter: `Data → Filter`
2. Filter `Country` = **United Kingdom** → **495,478 rows**
3. Clear → Filter `Country` = **Germany** → **9,495 rows**
4. Clear → Filter `InvoiceNo` → Text Filters → **Begins With** → `C` → **9,288 rows** (cancellations)
5. Clear → Filter `Quantity` → Number Filters → **Less Than** → `0` → **10,624 rows** (returns)
6. Clear → Filter `CustomerID` → **Blanks** → **135,080 rows**

**Expected output / verified values (full dataset):**

| Filter | Verified count |
|---|---|
| Country = United Kingdom | **495,478** |
| Country = Germany | **9,495** |
| InvoiceNo begins with C | **9,288** |
| Quantity < 0 | **10,624** |
| CustomerID = Blank | **135,080** |

*Note: The 2,000-row demo workbook will show smaller counts — these are full-dataset verified values. Tell students: "Your sample shows fewer rows — that is expected."*

**Common mistakes to watch for:** Students forgetting to clear the previous filter before applying the next one — they stack filters and get unexpected results.

---

## Group Exercise (35 min)

Open `exercises/week-01-thu-exercises.xlsx` → `Instructions` sheet. Use only sort and filter (no formulas).

**Questions:**

1. How many transactions came from **France**? *(Expected: 8,557)*
2. Which country besides the UK has the most transactions? *(Expected: Germany — 9,495)*
3. Filter to show only rows where Quantity is greater than 1,000. How many rows appear? *(Expected: 239 rows)*
4. Find the row with the highest UnitPrice that is NOT a cancellation and NOT a return. What is the UnitPrice and StockCode?
   *(Expected: £38,970.00, StockCode: DOT — sort UnitPrice descending after removing C-prefix rows)*
5. How many rows have a blank Description? *(Expected: 1,454 rows)*

**Debrief points:**
- Q2: Germany at 9,495 is just ahead of France at 8,557 — good market discussion.
- Q4: StockCode DOT = "DOTCOM POSTAGE" — a shipping fee line item, not a real product. Surfaces data quality discussion.
- Q5: 1,454 blank descriptions — reinforces why cleaning matters (covered properly in Week 3 and Week 5).

---

## Assignment (set at end of session)

Submit a short written response (1 paragraph per question, no formulas needed):

1. Describe in your own words what this dataset represents. Who collected it, what does each row mean, and what time period does it cover?
2. The CustomerID column is blank for 135,080 rows (24.9%). List two possible business reasons why a transaction might have no Customer ID.
3. You found that InvoiceNo values beginning with "C" are cancellations. Find and write down 3 example cancellation invoice numbers from the data.
4. The UnitPrice column contains negative values (minimum: £-11,062.06). What do you think negative prices represent, and why could this be a problem for analysis?

---

## Instructor Notes

- **Negative UnitPrice (£-11,062.06):** A known data quirk — likely an accounting adjustment. Do not resolve it yet; use it as motivation for Power Query cleaning in Week 5.
- **DOTCOM POSTAGE:** Students often flag this in Q4. It is a shipping fee coded as a product — good prompt for discussing what "data quality" means in practice.
- **Filter stacking confusion:** Very common at this stage. Walk the room during exercise time — look for students with multiple active filters.
- **CustomerID as float:** If students notice 17850.0 format, acknowledge it and say it will be fixed in Week 5.
