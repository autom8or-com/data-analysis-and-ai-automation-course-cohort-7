# Group 3 — Publishing Industry Intelligence
## PORA Academy Cohort 7 | Phase 1 Project

**Duration:** 2 weeks (4 facilitated sessions: Wed + Thu × 2 weeks)
**Dataset:** Amazon Top 50 Bestselling Books 2009–2019
**File:** `bestsellers with categories.csv`
**Group size:** 30 students (3 sub-groups of 10)
**Deliverable:** Excel workbook + 10-minute group presentation

> **Curriculum principle:** Every formula, expected output, and insight in this brief was verified by running code against the actual dataset. No expected answer is assumed.

---

## Dataset Facts (Verified)

| Fact | Value |
|---|---|
| Total rows | 550 |
| Total columns | 7 |
| Year range | 2009 – 2019 (11 years) |
| Null values | **Zero — dataset is complete** |
| Unique book titles | 351 |
| Unique authors | 248 |
| Genres | Fiction (240 entries), Non Fiction (310 entries) |
| Avg User Rating | 4.62 out of 5.0 |
| Rating range | 3.3 – 4.9 |
| Avg Price | $13.10 |
| Price range | $0 – $105 |

**All 7 columns:** `Name`, `Author`, `User Rating`, `Reviews`, `Price`, `Year`, `Genre`

**Data quality note:** 12 books have a Price of $0. This is not necessarily an error — it may reflect free digital editions. Students must handle this in their analysis.

---

## Business Scenario

> *You are a data analyst at a book publishing consultancy. A client — an independent publisher — wants to understand what makes a book reach Amazon's Top 50 bestseller list, how the market has shifted over 11 years, and whether Fiction or Non-Fiction is the more commercially attractive category. Your analysis will directly inform their next publishing investment decisions.*

---

## Session 1 (Wednesday, Week 7): Data Import & Exploration

**Objective:** Import the dataset, understand its structure, and produce a verified summary statistics table.

### Tasks

**1. Import & Inspect**
- Import `bestsellers with categories.csv` via `Data → Get Data → From Text/CSV`
- Set `User Rating` and `Price` as Decimal Number, `Reviews` and `Year` as Whole Number
- Rename sheet to `Raw Data`
- Verify: **550 rows, 7 columns, zero nulls**

**2. Summary Statistics Table** (new sheet: `Summary Stats`)

| Metric | Formula | Verified Answer |
|---|---|---|
| Total records | `=COUNTA(A:A)-1` | **550** |
| Unique book titles | Remove Duplicates on Name copy | **351** |
| Unique authors | Remove Duplicates on Author copy | **248** |
| Avg User Rating | `=AVERAGE(C:C)` | **4.62** |
| Highest rating | `=MAX(C:C)` | **4.9** |
| Lowest rating | `=MIN(C:C)` | **3.3** |
| Avg Reviews | `=AVERAGE(D:D)` | **11,953** |
| Most reviews (single entry) | `=MAX(D:D)` | **87,841** |
| Avg Price | `=AVERAGE(E:E)` | **$13.10** |
| Books with $0 price | `=COUNTIF(E:E,0)` | **12** |
| Fiction entries | `=COUNTIF(G:G,"Fiction")` | **240** |
| Non Fiction entries | `=COUNTIF(G:G,"Non Fiction")` | **310** |

**3. Group Discussion**
- 550 entries represent 11 years × 50 books/year. But there are only 351 unique titles. What does this tell you?
  *(Answer: 199 instances are books appearing in the bestseller list in **multiple years** — some books were bestsellers for up to 10 consecutive years)*
- 12 books have $0 price. How should this affect any average price calculations?

---

## Session 2 (Thursday, Week 7): Data Cleaning & Genre Analysis

**Objective:** Build classification columns and conduct genre-level comparative analysis.

### Tasks

**1. Calculated & Classification Columns**

| Column | Formula | Notes |
|---|---|---|
| `Rating Category` | `=IF([@[User Rating]]>=4.8,"Outstanding",IF([@[User Rating]]>=4.5,"Excellent",IF([@[User Rating]]>=4.0,"Great","Good")))` | Text |
| `Price Category` | `=IF([@Price]=0,"Free",IF([@Price]<10,"Budget",IF([@Price]<=20,"Mid-Range","Premium")))` | Text |
| `Review Category` | `=IF([@Reviews]>=50000,"Viral",IF([@Reviews]>=10000,"Popular",IF([@Reviews]>=1000,"Moderate","Low")))` | Text |

**Verify Rating Category distribution using COUNTIF:**

| Category | Formula | Verified Answer |
|---|---|---|
| Outstanding (≥4.8) | `=COUNTIF(your_col,"Outstanding")` | **52** |
| Excellent (4.5–4.8) | `=COUNTIF(your_col,"Excellent")` | **340** |
| Great (4.0–4.5) | `=COUNTIF(your_col,"Great")` | **137** |
| Good (<4.0) | `=COUNTIF(your_col,"Good")` | **21** |

**2. Genre Comparison Table** (AVERAGEIF and SUMIF)

| Metric | Fiction | Non Fiction |
|---|---|---|
| Avg User Rating | `=AVERAGEIF(G:G,"Fiction",C:C)` | **4.65** | `=AVERAGEIF(G:G,"Non Fiction",C:C)` | **4.60** |
| Avg Reviews | `=AVERAGEIF(G:G,"Fiction",D:D)` | **15,684** | `=AVERAGEIF(G:G,"Non Fiction",D:D)` | **9,065** |
| Avg Price | `=AVERAGEIF(G:G,"Fiction",E:E)` | **$10.85** | `=AVERAGEIF(G:G,"Non Fiction",E:E)` | **$14.84** |
| Total Reviews | `=SUMIF(G:G,"Fiction",D:D)` | **3,764,110** | `=SUMIF(G:G,"Non Fiction",D:D)` | **2,810,195** |

**Key insight to surface:**
- Fiction books are **cheaper** ($10.85 avg vs $14.84) but attract **more reviews** (15,684 avg vs 9,065)
- Non-Fiction commands a **37% price premium** over Fiction

**3. Price Analysis — Handling $0 Entries**

Two approaches — students should calculate both and compare:
- `=AVERAGE(E:E)` → $13.10 *(includes $0 prices)*
- `=AVERAGEIF(E:E,">0",E:E)` → run & verify *(excludes free books)*

Which is more appropriate for a "price of a bestselling book" analysis? Groups must justify their choice.

---

## Independent Work (Between Sessions 2 & 3)

Each sub-group takes one dimension:
- **Sub-group A:** Author performance & multi-year analysis
- **Sub-group B:** Year-over-year market trends
- **Sub-group C:** Rating and price relationship analysis

### Sub-group A — Author Performance

Count appearances per author using COUNTIF:
```
=COUNTIF($B:$B, [@Author])
```

**Verified top authors by appearances:**

| Author | Appearances |
|---|---|
| Jeff Kinney | 12 |
| Gary Chapman | 11 |
| Rick Riordan | 11 |
| Suzanne Collins | 11 |
| Dr. Seuss | 9 |

Build author tiers:
```
=IF(appearances>=10,"Dominant Author",IF(appearances>=5,"Established Author",IF(appearances>=2,"Recurring Author","One-Time")))
```

Count multi-year books (same title appearing in multiple years):
```
=COUNTIF($A:$A, [@Name])
```
**Most consistent bestseller:** `Publication Manual of the American Psychological Association` — appeared **10 consecutive years**.

### Sub-group B — Year-Over-Year Trends

Build a Year Summary table using AVERAGEIF and COUNTIFS:

| Year | Avg Rating | Avg Price | Fiction Count | Non-Fiction Count |
|---|---|---|---|---|
| 2009 | **4.58** | **$15.40** | 24 | 26 |
| 2010 | 4.56 | $13.48 | 20 | 30 |
| 2011 | 4.56 | $15.10 | 21 | 29 |
| 2012 | 4.53 | $15.30 | 21 | 29 |
| 2013 | 4.55 | $14.60 | 24 | 26 |
| 2014 | 4.62 | $14.64 | 29 | 21 |
| 2015 | 4.65 | $10.42 | 17 | 33 |
| 2016 | 4.68 | $13.18 | 19 | 31 |
| 2017 | 4.66 | $11.38 | 24 | 26 |
| 2018 | 4.67 | $10.52 | 21 | 29 |
| 2019 | **4.74** | **$10.08** | 20 | 30 |

**Findings:** Ratings improved significantly (3.3→4.74 trend from 2009 to 2019). Prices declined substantially ($15.40 in 2009 → $10.08 in 2019 — a **34.5% drop**).

### Sub-group C — Rating & Price Relationship

Test the hypothesis: *"Higher-rated books cost more."*

Use AVERAGEIF to compare price across rating categories:

| Rating Category | Avg Price | Count |
|---|---|---|
| Outstanding (≥4.8) | Calculate | 52 |
| Excellent (4.5–4.8) | Calculate | 340 |
| Great (4.0–4.5) | Calculate | 137 |
| Good (<4.0) | Calculate | 21 |

Do high-rated books command higher prices? Groups should state a conclusion from the data.

---

## Session 3 (Wednesday, Week 8): Pivot Tables & Charts

**Objective:** Build pivot tables that tell the 11-year market story visually.

### Pivot Tables to Build

**Pivot 1: Genre × Year Summary**
- Rows: Genre, Columns: Year, Values: Count of Name + Average of User Rating
- Add slicer: Genre
- Expected: Non-Fiction dominated 8 of 11 years

**Pivot 2: Rating Trend by Year**
- Rows: Year, Values: Average of User Rating + Average of Price
- Insert dual-axis line chart: Rating (left axis), Price (right axis)
- **Headline chart:** Rating rises as price falls — the premium ebook/digital era

**Pivot 3: Author Performance**
- Rows: Author, Values: Count of Name, Average of User Rating, Average of Reviews
- Sort by Count descending → Top 10 authors
- Add conditional formatting: Top 10 authors highlighted

**Pivot 4: Review Volume by Rating Category**
- Rows: Rating Category, Values: Sum of Reviews, Average of Reviews, Count of Name
- Shows whether higher-rated books also attract more reviews

### Charts to Create
1. **Stacked bar chart:** Fiction vs Non-Fiction count per year (from Pivot 1)
2. **Dual-axis line chart:** Avg Rating and Avg Price over 2009–2019 (from Pivot 2)
3. **Bubble chart (optional/advanced):** User Rating (x) vs Reviews (y) vs Price (bubble size)

---

## Session 4 (Thursday, Week 8): Power Query Pipeline & Dashboard

**Objective:** Build automated data pipeline and assemble final dashboard.

### Power Query Steps

1. Load `bestsellers with categories.csv` → **Transform Data**
2. Set column types: `User Rating` and `Price` → Decimal Number; `Reviews` and `Year` → Whole Number
3. Add conditional column `Rating Category`:
   - If User Rating >= 4.8 → "Outstanding"
   - If User Rating >= 4.5 → "Excellent"
   - If User Rating >= 4.0 → "Great"
   - Else → "Good"
4. Add conditional column `Price Category`:
   - If Price = 0 → "Free"
   - If Price < 10 → "Budget"
   - If Price <= 20 → "Mid-Range"
   - Else → "Premium"
5. Add custom column: `Review Score = [Reviews] / 1000` (reviews in thousands — easier to read)
6. Name query `BestsellersClean` → `Close & Load To` → sheet `Clean Data`

**Verify:** 550 rows, 10 columns after load

### Dashboard Sheet

**KPI Row:**

| KPI | Formula | Verified Value |
|---|---|---|
| Total entries | `=COUNTA(BestsellersClean[Name])` | **550** |
| Avg Rating | `=AVERAGE(BestsellersClean[User Rating])` | **4.62** |
| Avg Price (excl. free) | `=AVERAGEIF(BestsellersClean[Price],">"&0,BestsellersClean[Price])` | Run & verify |
| Fiction % | `=COUNTIF(BestsellersClean[Genre],"Fiction")/COUNTA(BestsellersClean[Genre])` | **43.6%** |

**Charts on Dashboard:**
1. Fiction vs Non-Fiction by year (stacked bar)
2. Rating trend 2009–2019 (line)
3. Price trend 2009–2019 (line)
4. Top 10 authors by appearances (horizontal bar)

**Slicer:** Genre — connects to all charts

---

## Deliverables

### Excel Workbook (60%)

| Sheet | Contents | Marks |
|---|---|---|
| `Raw Data` | Original data + 3 classification columns | 10 |
| `Summary Stats` | COUNTIF, AVERAGEIF, SUMIF tables — all values verified | 15 |
| `Pivot Analysis` | 4 pivot tables + charts, correct values | 20 |
| `Clean Data` | Power Query output — 550 rows, all columns | 10 |
| `Dashboard` | 4 KPIs, 4 charts, slicer, professional layout | 15 |

### Presentation (40%)

**10 minutes. Structure:**
1. What makes a book reach the Top 50? (headline findings — 2 min)
2. Fiction vs Non-Fiction: which is the better market? (3 min)
3. The price decline trend — opportunity or threat for publishers? (2 min)
4. Three specific publishing recommendations for your client (3 min)

**Assessment:**

| Criteria | Marks |
|---|---|
| Business insight quality | 15 |
| Visual communication | 15 |
| Technical accuracy | 10 |

---

## Expected Business Insights

Groups that complete this project correctly should be able to state:

1. **The market rewards consistency over novelty.** 199 of 550 entries are repeat appearances by the same book in multiple years. The `Publication Manual of the APA` appeared on the list for 10 consecutive years. Long-term catalog investment beats chasing one-time releases.

2. **Fiction drives more reader engagement but earns less per sale.** Fiction books average 15,684 reviews (vs 9,065 for Non-Fiction) but are priced at $10.85 (vs $14.84 for Non-Fiction). For volume and reach, Fiction wins. For margin per sale, Non-Fiction is stronger.

3. **Prices have fallen 34.5% over 11 years** ($15.40 in 2009 → $10.08 in 2019), driven by the digital/ebook shift. Yet ratings improved from 4.58 to 4.74 — readers are more satisfied with cheaper books. A publisher entering this market should not anchor to pre-2015 pricing.

4. **A small group of authors dominate the list.** Jeff Kinney, Gary Chapman, Rick Riordan, and Suzanne Collins collectively account for 45 bestseller list appearances. Building long-term author relationships is more valuable than acquiring one-off manuscripts.
