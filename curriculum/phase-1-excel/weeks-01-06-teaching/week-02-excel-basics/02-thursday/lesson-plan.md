# Week 02 — Thursday: COUNTIF, Conditional Formatting & Excel Tables
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 02 of 6
**Session:** Thursday
**Topic:** COUNTIF, Conditional Formatting & Excel Tables

---

## Pre-Session Checklist

- [ ] Dataset loaded with `Revenue` column added (from Wednesday exercise — column I = `=D2*F2`)
- [ ] Demo workbook open: `lecture-materials/week-02-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-02-thu-exercises.xlsx`
- [ ] Projector / screen sharing ready
- [ ] Weekly assignment text ready to share at end of session

---

## Learning Objectives

By the end of this session, students will be able to:

1. Use COUNTIF to count rows that meet a condition
2. Apply conditional formatting to highlight data patterns visually
3. Convert raw data to an Excel Table and use structured references

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap of Wednesday | Quick fire: what were the 8 formulas from the Summary Stats table? |
| 0:10 – 0:45 | Concept 1 — COUNTIF | Country counts + numeric criteria |
| 0:45 – 1:15 | Concept 2 — Conditional Formatting | 3 rules live on Raw Data sheet |
| 1:15 – 1:30 | Concept 3 — Excel Tables | Convert to Table, structured references |
| 1:30 – 1:55 | Group exercise | 5 tasks covering all three concepts |
| 1:55 – 2:00 | Assignment intro & close | Read out assignment, answer questions |

---

## Concept 1 — COUNTIF (35 min)

**What to demonstrate:**

Syntax: `=COUNTIF(range, criteria)`

On the `Summary Stats` sheet, add a **Country Transactions** section:

| Country | Formula | Verified Answer |
|---|---|---|
| United Kingdom | `=COUNTIF(H:H,"United Kingdom")` | **495,478** |
| Germany | `=COUNTIF(H:H,"Germany")` | **9,495** |
| France | `=COUNTIF(H:H,"France")` | **8,557** |
| EIRE | `=COUNTIF(H:H,"EIRE")` | **8,196** |
| Spain | `=COUNTIF(H:H,"Spain")` | **2,533** |

Then add a **Numeric Criteria** section:

| Condition | Formula | Verified Answer |
|---|---|---|
| Rows where Quantity > 10 | `=COUNTIF(D:D,">10")` | **132,631** |
| Rows where Quantity < 0 (returns) | `=COUNTIF(D:D,"<0")` | **10,624** |
| Rows where UnitPrice = 0 | `=COUNTIF(F:F,0)` | **2,515** |

**Key teaching moments:**
- Text criteria must be in quotes: `"United Kingdom"` — exact match, case-insensitive
- Comparison criteria in quotes with operator: `">10"` — operator inside the quotes
- Cross-check: COUNTIF Qty < 0 (10,624) matches the filter result from Week 1

**Expected output / verified values:** See tables above.

**Common mistakes to watch for:**
- Forgetting quotes around text criteria — returns 0 or error
- Country names with wrong capitalisation — COUNTIF is case-insensitive so this works, but reinforce consistent capitalisation

---

## Concept 2 — Conditional Formatting (30 min)

**What to demonstrate:**

Switch to the `Raw Data` sheet. Apply three rules live:

**Rule 1 — Highlight negative Quantity (returns):**
1. Select column D
2. `Home` → `Conditional Formatting` → `Highlight Cell Rules` → `Less Than` → `0` → Red fill
3. Result: all return rows visually flagged

**Rule 2 — Highlight blank CustomerID:**
1. Select column G
2. `CF` → `New Rule` → `Format only cells that contain` → change to **Blanks** → Orange fill
3. Result: missing CustomerID rows visible at a glance

**Rule 3 — Top 10% UnitPrice:**
1. Select column F
2. `CF` → `Top/Bottom Rules` → `Top 10%` → Green fill
3. Result: premium-priced products highlighted

**Discussion after each rule:** What business action could this insight trigger?
- Red → investigate return patterns
- Orange → why are 24.9% of transactions guest checkouts?
- Green → are high-price items high-margin?

**Expected output / verified value:** Visual highlighting only — no numeric output.

**Common mistakes to watch for:**
- Selecting the whole sheet instead of a single column — use `Manage Rules` to show students how to reorder or delete rules
- Multiple conflicting rules on the same column — stacked in priority order

---

## Concept 3 — Excel Tables (15 min)

**What to demonstrate:**

Convert the Raw Data to a formal Excel Table:

1. Click anywhere in the data on the `Raw Data` sheet
2. `Insert` → `Table` → confirm range includes headers → OK
3. In the `Table Design` tab, rename the table to `RetailData`

Show structured references:

| Formula | Equivalent | Result |
|---|---|---|
| `=SUM(RetailData[Quantity])` | `=SUM(D:D)` | **5,176,450** |
| `=AVERAGE(RetailData[UnitPrice])` | `=AVERAGE(F:F)` | **£4.61** |

**Benefits:**
- Table auto-expands when new rows are added
- `[@Quantity]` refers to "this row's Quantity" — useful for row-level formulas
- Column headers are protected from accidental deletion

**Expected output / verified values:** Same as Wednesday AVERAGE and SUM results.

**Common mistakes to watch for:**
- Clicking OK without checking "My table has headers" — headers become data row 1
- Table name with spaces (e.g. `Retail Data`) — table names cannot contain spaces

---

## Group Exercise (30 min)

Open `exercises/week-02-thu-exercises.xlsx` → `Instructions` sheet.

**Questions:**

1. Using COUNTIF, how many transactions came from **Netherlands**?
   *(Full dataset: 2,371)*
2. Using COUNTIF, how many rows have a UnitPrice **greater than £10**?
   *(Full dataset: 71,938)*
3. Apply conditional formatting to highlight all rows where `Country = "Germany"` using a formula-based rule: `=$H2="Germany"`. How many rows are highlighted?
   *(Full dataset: 9,495 — matches COUNTIF result)*
4. Using the Excel Table, write the structured reference formula for average UnitPrice.
   *(Expected: `=AVERAGE(RetailData[UnitPrice])` → £4.61)*
5. Add a column `IsReturn` to the Table using: `=IF([@Quantity]<0,"Return","Sale")`. How many rows are marked "Return"?
   *(Full dataset: 10,624 — consistent with COUNTIF and Week 1 filter)*

**Debrief:** Groups share answers. Confirm that Q1/Q2 (COUNTIF), Q3 (CF), Q4 (Table), Q5 (IF in Table) cover all three concepts from today.

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-02-thu-demo.xlsx` | Instructor demo workbook — open on screen during teaching |
| `exercises/week-02-thu-exercises.xlsx` | Distributed to students at exercise time |
| `solutions/week-02-thu-solutions.xlsx` | Instructor reference — do not share before exercise is complete |

---

## Assignment (set at end of this session)

Read aloud and share on the LMS before students leave.

1. Using COUNTIF, count transactions from **Australia**, **Belgium**, and **Switzerland**. Write the three formulas and results.
   *(Expected: Australia=1,259 | Belgium=2,069 | Switzerland=2,002)*

2. Add a column `RevenueCheck` (Quantity × UnitPrice). For rows 2–6, write the formula and result for each row.

3. Apply conditional formatting to the `UnitPrice` column using a **3-colour scale** (low=red, mid=yellow, high=green). Take a screenshot and include it in your submission.

4. Using COUNTIF, what percentage of all rows are from the United Kingdom? Show your formula.
   *(Expected: `=COUNTIF(H:H,"United Kingdom")/(COUNTA(A:A)-1)` → 91.4%)*

**Submission:** LMS assignment portal. Due before Week 3 Wednesday session.

---

## Instructor Notes

- The COUNTIF UK result (495,478) should match exactly what students saw filtering by UK in Week 1 — make this connection explicitly. Formulas and filters are two ways to get the same answer.
- For Q5 (IsReturn), the `[@Quantity]` syntax only works inside a Table. If students haven't converted to a Table yet, they need `=IF(D2<0,"Return","Sale")` instead.
- Assignment Q4 uses a percentage formula: format the cell as Percentage to display 91.4%. Students may struggle with why `COUNTA(A:A)-1` is in the denominator.
- If time is short, Concept 3 (Excel Tables) can be a 10-min demonstration only — Q4 and Q5 from the group exercise can become take-home.
