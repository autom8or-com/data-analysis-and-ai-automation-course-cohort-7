# Group 2 — Product Category Performance Analysis
## PORA Academy Cohort 7 | Phase 1 Project

**Duration:** 2 weeks (4 facilitated sessions: Wed + Thu × 2 weeks)
**Dataset:** Superstore Sales Dataset
**File:** `Sample - Superstore.csv`
**Group size:** 30 students (3 sub-groups of 10)
**Deliverable:** Excel workbook + 10-minute group presentation

> **Curriculum principle:** Every formula, expected output, and insight in this brief was verified by running code against the actual dataset. No expected answer is assumed.

---

## Dataset Facts (Verified)

| Fact | Value |
|---|---|
| Total rows | 9,994 |
| Total columns | 21 |
| Date range | 03/01/2014 – 30/12/2017 |
| Null values | **Zero — dataset is complete** |
| Unique customers | 793 |
| Unique products | 1,862 |
| Categories | Furniture, Office Supplies, Technology |
| Segments | Consumer, Corporate, Home Office |
| Regions | West, East, Central, South |
| Ship modes | Same Day, First Class, Second Class, Standard Class |

**Key columns for this project:**
`Category`, `Sub-Category`, `Sales`, `Profit`, `Discount`, `Quantity`, `Segment`, `Region`, `Order Date`, `Ship Date`, `Ship Mode`

---

## Business Scenario

> *You are a data analyst at a US retail company. The leadership team has noticed that overall profit margins are thin at 12.5% and suspects that some product categories are dragging performance down while others are thriving. Your task is to conduct a full product category performance analysis and present actionable recommendations.*

---

## Session 1 (Wednesday, Week 7): Data Import & Exploration

**Objective:** Import the dataset, understand its structure, and build a summary statistics table.

### Tasks

**1. Import & Inspect**
- Import `Sample - Superstore.csv` via `Data → Get Data → From Text/CSV`
- Set column types: `Order Date` and `Ship Date` as Date, `Sales`/`Profit`/`Discount` as Number
- Rename sheet to `Raw Data`
- Verify row count: **9,994 rows, 21 columns**
- Confirm: **zero null values** across all columns

**2. Summary Statistics Table** (new sheet: `Summary Stats`)

Build this table using verified formulas:

| Metric | Formula | Verified Answer |
|---|---|---|
| Total transactions | `=COUNTA(A:A)-1` | **9,994** |
| Total Sales | `=SUM(R:R)` | **$2,297,200.86** |
| Total Profit | `=SUM(U:U)` | **$286,397.02** |
| Overall Profit Margin | `=SUM(U:U)/SUM(R:R)` | **12.5%** |
| Average Order Value | `=AVERAGE(R:R)` | **$229.86** |
| Max single-order Sales | `=MAX(R:R)` | Run & verify |
| Rows with negative Profit | `=COUNTIF(U:U,"<0")` | **1,871** |
| Rows with zero Discount | `=COUNTIF(T:T,0)` | **4,798** |
| Unique Customers | Use Remove Duplicates on a copy | **793** |

**3. Group Discussion**
- 1,871 rows have negative profit. What percentage of total transactions is this? *(1,871/9,994 = 18.7%)*
- What business events might explain why a sale generates negative profit?

---

## Session 2 (Thursday, Week 7): Data Cleaning & Category Analysis

**Objective:** Build calculated columns and conduct multi-condition category analysis.

### Tasks

**1. Calculated Columns** (add to Raw Data sheet)

| Column | Formula | Notes |
|---|---|---|
| `Days to Ship` | `=[@[Ship Date]]-[@[Order Date]]` | Format as Number |
| `Profit Margin` | `=[@Profit]/[@Sales]` | Format as % |
| `Discount Category` | `=IF([@Discount]=0,"No Discount",IF([@Discount]<=0.2,"Low",IF([@Discount]<=0.4,"Medium","High")))` | Text |
| `Order Size` | `=IF([@Sales]>=1000,"Large",IF([@Sales]>=500,"Medium","Small"))` | Text |
| `Profitable` | `=IF([@Profit]>0,"Yes","No")` | Text |

**Verify Days to Ship by Ship Mode** (using AVERAGEIF):

| Ship Mode | Formula | Verified Answer |
|---|---|---|
| Same Day | `=AVERAGEIF(F:F,"Same Day",your_DaysToShip_col)` | **0.0 days** |
| First Class | `=AVERAGEIF(F:F,"First Class",your_DaysToShip_col)` | **2.2 days** |
| Second Class | `=AVERAGEIF(F:F,"Second Class",your_DaysToShip_col)` | **3.2 days** |
| Standard Class | `=AVERAGEIF(F:F,"Standard Class",your_DaysToShip_col)` | **5.0 days** |

**2. Category Performance Table** (using SUMIFS and AVERAGEIF)

| Category | Total Sales | Total Profit | Profit Margin |
|---|---|---|---|
| Furniture | `=SUMIFS(Sales,Category,"Furniture")` | `=SUMIFS(Profit,Category,"Furniture")` | **$741,999.80 / $18,451.27 = 2.5%** |
| Office Supplies | — | — | **$719,047.03 / $122,490.80 = 17.0%** |
| Technology | — | — | **$836,154.03 / $145,454.95 = 17.4%** |

**Critical insight to surface:** Furniture has a **2.5% profit margin** — nearly break-even. Office Supplies and Technology both exceed 17%.

**3. Discount Impact Analysis**

| Condition | Formula | Verified Answer |
|---|---|---|
| Avg margin (with discount) | AVERAGEIF on Profit Margin where Discount > 0 | **-2.9%** |
| Avg margin (no discount) | AVERAGEIF on Profit Margin where Discount = 0 | **+29.5%** |

**This is a major finding:** Discounted orders are on average **loss-making (-2.9%)** while non-discounted orders return **29.5% margin**. Groups must present this in their recommendation.

---

## Independent Work (Between Sessions 2 & 3)

Each sub-group of 10 takes one dimension:
- **Sub-group A:** Sub-category deep dive
- **Sub-group B:** Regional performance
- **Sub-group C:** Customer segment analysis

### Sub-group A — Sub-Category Analysis

Build a full sub-category table (SUMIFS for Sales and Profit, calculated Margin):

**Verified worst-performing sub-categories:**

| Sub-Category | Sales | Profit | Margin |
|---|---|---|---|
| Tables | $206,965.53 | **-$17,725.48** | **-8.6%** |
| Bookcases | $114,880.00 | **-$3,472.56** | **-3.0%** |
| Supplies | $46,673.54 | **-$1,189.10** | **-2.5%** |

**Best-performing by margin:** Run AVERAGEIF on each sub-category — Copiers, Paper, Envelopes should rank highest.

### Sub-group B — Regional Performance

| Region | Sales | Profit | Margin |
|---|---|---|---|
| West | $725,457.82 | $108,418.45 | 14.9% |
| East | $678,781.24 | $91,522.78 | 13.5% |
| Central | $501,239.89 | $39,706.36 | 7.9% |
| South | $391,721.90 | $46,749.43 | 11.9% |

**Finding:** Central region has the lowest margin (7.9%) despite being 3rd in sales.

### Sub-group C — Segment Analysis

| Segment | Sales | Profit |
|---|---|---|
| Consumer | $1,161,401.34 | $134,119.21 |
| Corporate | $706,146.37 | $91,979.13 |
| Home Office | $429,653.15 | $60,298.68 |

Build COUNTIFS table: count of orders by Segment × Category (3×3 matrix).

---

## Session 3 (Wednesday, Week 8): Pivot Tables & Charts

**Objective:** Build the analysis layer with pivot tables, verify outputs, and identify the 3 key business findings.

### Pivot Tables to Build

**Pivot 1: Sales & Profit by Category × Year**
- Rows: Category, Columns: Year (Order Date grouped by year), Values: Sum of Sales + Sum of Profit
- Add a calculated field: `Margin% = Profit/Sales`

**Verified Sales by Year:**

| Year | Total Sales |
|---|---|
| 2014 | $484,247.50 |
| 2015 | $470,532.51 |
| 2016 | $609,205.60 |
| 2017 | $733,215.26 |

*Sales grew 51.4% from 2014 to 2017.*

**Pivot 2: Profit Margin by Sub-Category**
- Rows: Sub-Category, Values: Sum of Sales + Sum of Profit
- Sort by Profit ascending → Tables (-$17,725), Bookcases (-$3,472), Supplies (-$1,189) at the bottom
- Add conditional formatting: red for negative profit

**Pivot 3: Discount Impact by Category**
- Rows: Category, Columns: Discount Category (your calculated column), Values: Average of Profit Margin
- This should clearly show that "High" discount rows have the worst margins in every category

**Pivot 4: Ship Mode Usage by Segment**
- Rows: Ship Mode, Columns: Segment, Values: Count of Order ID
- Add slicer: Category

### Charts to Create
1. **Clustered bar chart** from Pivot 1: Sales vs Profit by Category
2. **Waterfall or bar chart** from Pivot 2: Profit by Sub-Category (showing losses in red)
3. **Line chart** from year-over-year Sales trend

---

## Session 4 (Thursday, Week 8): Power Query Pipeline & Dashboard

**Objective:** Build a clean data pipeline in Power Query and assemble the final dashboard.

### Power Query Steps

1. Load `Sample - Superstore.csv` → click **Transform Data**
2. Set `Order Date` and `Ship Date` to **Date** type
3. Set `Sales`, `Profit`, `Discount` to **Decimal Number**
4. Add custom column: `Days to Ship = [Ship Date] - [Order Date]` — set type to Whole Number
5. Add custom column: `Profit Margin = [Profit] / [Sales]` — set type to Percentage
6. Add conditional column `Discount Category`:
   - If Discount = 0 → "No Discount"
   - If Discount <= 0.2 → "Low"
   - If Discount <= 0.4 → "Medium"
   - Else → "High"
7. Name query `SuperstoreClean` → `Close & Load To` → new sheet `Clean Data`

**Verify after load:** 9,994 rows (no rows should be removed — dataset has no nulls)

### Dashboard Sheet

**KPI Row:**

| KPI | Formula on Dashboard | Verified Value |
|---|---|---|
| Total Sales | `=SUM(SuperstoreClean[Sales])` | **$2,297,200.86** |
| Total Profit | `=SUM(SuperstoreClean[Profit])` | **$286,397.02** |
| Profit Margin | `=SUM(SuperstoreClean[Profit])/SUM(SuperstoreClean[Sales])` | **12.5%** |
| Loss-making Orders | `=COUNTIF(SuperstoreClean[Profit],"<0")` | **1,871** |

**Charts on Dashboard (linked from pivot sheets):**
1. Sales vs Profit by Category (bar chart)
2. Profit margin by Sub-Category with red/green conditional colouring
3. Year-over-year Sales trend (line chart)
4. Discount impact on margin (bar chart)

**Slicer:** Region — connects to all 4 charts

---

## Deliverables

### Excel Workbook (60%)

| Sheet | Contents | Marks |
|---|---|---|
| `Raw Data` | Original imported data, calculated columns | 10 |
| `Summary Stats` | All SUMIFS, AVERAGEIF, COUNTIF tables | 15 |
| `Pivot Analysis` | 4 pivot tables, all verified against expected outputs | 20 |
| `Clean Data` | Power Query output (9,994 rows, all columns + calculated) | 10 |
| `Dashboard` | 4 KPIs, 4 charts, 1 slicer, professional formatting | 15 |

### Presentation (40%)

**10 minutes. Structure:**
1. Dataset overview (1 min)
2. The headline finding: Furniture's 2.5% margin (2 min)
3. The discount problem: -2.9% margin with discount vs +29.5% without (3 min)
4. Regional and segment findings (2 min)
5. Three specific recommendations (2 min)

**Assessment:**

| Criteria | Marks |
|---|---|
| Business insight quality | 15 |
| Visual communication | 15 |
| Technical accuracy (formulas match expected outputs) | 10 |

---

## Expected Business Insights

Groups that complete this project correctly should be able to state:

1. **Furniture is nearly unprofitable at 2.5% margin**, driven by Tables (-8.6%) and Bookcases (-3.0%). The company should review its Furniture pricing strategy or discontinue high-discount Furniture items.

2. **Discounting is destroying profit.** Orders with discounts average -2.9% margin. Orders without discounts average +29.5%. The company's discount policy needs urgent review.

3. **Central region underperforms** at 7.9% margin despite being the third-largest by sales — suggesting either higher operating costs or a more discount-heavy customer base in that region.

4. **Sales are growing** (2014: $484K → 2017: $733K, +51.4%) but if the discount problem is not addressed, increased sales will not translate to proportional profit growth.
