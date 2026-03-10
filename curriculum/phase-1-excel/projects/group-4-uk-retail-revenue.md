# Group 4 — UK Retail Revenue Analysis
## PORA Academy Cohort 7 | Phase 1 Project

**Duration:** 2 weeks (4 facilitated sessions: Wed + Thu × 2 weeks)
**Dataset:** UCI Online Retail Dataset (same dataset used in teaching Weeks 1–6)
**File:** `data.csv`
**Group size:** 30 students (3 sub-groups of 10)
**Deliverable:** Excel workbook + 10-minute group presentation

> **This group has a unique advantage:** you have been working with this dataset for 6 weeks. You know its structure, its quirks, and its data quality issues. Your project is to go deeper — moving from descriptive statistics to business intelligence and strategic recommendations.

> **Curriculum principle:** Every formula, expected output, and insight in this brief was verified by running code against the actual dataset. No expected answer is assumed.

---

## Dataset Facts (Verified — Clean Data)

The project uses the **cleaned** version of the dataset built in Week 5–6 Power Query pipeline.

| Fact | Raw Data | Clean Data |
|---|---|---|
| Total rows | 541,909 | **~530,104** |
| Rows removed | — | ~11,805 (2.2%) |
| Total Revenue | £9,747,747.93 | **£10,666,684.54** |
| Unique customers (with ID) | 4,372 | **4,338** |
| Unique products | 4,070 | **4,015** |
| Unique invoices | 25,900 | **19,960** |
| Countries | 38 | 38 |
| International revenue | — | **£1,641,462.46 (15.4%)** |

*Note: Clean data excludes cancellations, returns, zero-price rows, and blank descriptions. CustomerID nulls remain — these are valid transactions from guest/anonymous customers.*

---

## Business Scenario

> *You are a data analyst presenting to the board of a UK-based online gift wholesaler. The company has 13 months of transaction data. The board wants to understand: Who are their most valuable customers? Which products drive the most revenue? Is international expansion working? And critically — what is happening with the business trajectory? Your Power Query pipeline from Weeks 5–6 is your starting point.*

---

## Session 1 (Wednesday, Week 7): Extending the Pipeline & Customer Analysis

**Objective:** Extend your Week 6 Power Query pipeline with new columns and begin customer segmentation.

### Tasks

**1. Extend Your Power Query Pipeline**

Open your Week 6 query. Add these additional columns:

| Column | M Formula | Notes |
|---|---|---|
| `Quarter` | `= "Q" & Number.ToText(Date.QuarterOfYear([InvoiceDate]))` | e.g. "Q1", "Q4" |
| `YearQuarter` | `= Number.ToText(Date.Year([InvoiceDate])) & "-Q" & Number.ToText(Date.QuarterOfYear([InvoiceDate]))` | e.g. "2011-Q4" |
| `IsWeekend` | `= if Date.DayOfWeek([InvoiceDate]) >= 5 then "Weekend" else "Weekday"` | Order day type |
| `UKorInternational` | `= if [Country] = "United Kingdom" then "UK" else "International"` | Market flag |

Reload to `Clean Data` sheet. Verify row count remains ~530,104.

**2. Revenue Summary Table** (new sheet: `Project Analysis`)

| Metric | Formula | Verified Value |
|---|---|---|
| Total clean revenue | `=SUM(RetailClean[Revenue])` | **£10,666,684.54** |
| UK revenue | `=SUMIF(RetailClean[Country],"United Kingdom",RetailClean[Revenue])` | **£9,025,222.08** |
| International revenue | `=SUMIF(RetailClean[UKorInternational],"International",RetailClean[Revenue])` | **£1,641,462.46** |
| International % | `=International/Total` | **15.4%** |
| Unique invoices | Count distinct InvoiceNo | **19,960** |
| Avg basket value (per invoice) | `=Total Revenue / Unique invoices` | **£534.40** |
| Median basket value | Build helper pivot and observe | **£303.84** |

**3. Quarterly Revenue Trend**

Build SUMIFS for each quarter:

| Quarter | Revenue | Formula |
|---|---|---|
| 2010-Q4 | **£823,746.14** | `=SUMIFS(Revenue,YearQuarter,"2010-Q4")` |
| 2011-Q1 | **£1,932,635.81** | — |
| 2011-Q2 | **£2,070,084.54** | — |
| 2011-Q3 | **£2,536,949.74** | — |
| 2011-Q4 | **£3,303,268.31** | — |

**Headline finding:** Revenue grew from £824K (Q4 2010) to £3.3M (Q4 2011) — a **301% quarterly increase** in just 12 months.

---

## Session 2 (Thursday, Week 7): Customer Segmentation

**Objective:** Segment customers by purchase behaviour and identify the most valuable customer group.

### Tasks

**1. Customer Order Frequency** (using COUNTIF)

Add a column in a new `Customer Analysis` helper sheet:
- List all unique CustomerIDs (use Remove Duplicates on a CustomerID copy — exclude blanks)
- Count orders per customer: `=COUNTIF(RetailClean[CustomerID], [@CustomerID])`

**Verified customer distribution:**

| Segment | Order Count Range | Count | Formula hint |
|---|---|---|---|
| One-time buyers | = 1 invoice | **1,493** | `=COUNTIF(orders_col, 1)` |
| Occasional | 2–5 invoices | **1,973** | `=COUNTIFS(orders_col,">="&2,orders_col,"<="&5)` |
| Loyal | > 5 invoices | **872** | `=COUNTIF(orders_col,">"&5)` |

The most active customer placed **209 orders** in 13 months.

**2. Customer Value Tiers**

Add a tier column:
```
=IF([@OrderCount]>=20,"Top Tier",IF([@OrderCount]>=10,"High Value",IF([@OrderCount]>=5,"Mid Value","Standard")))
```

**3. Top 5 Customers by Revenue** (SUMIF on CustomerID)

| CustomerID | Revenue |
|---|---|
| 14646 | **£280,206.02** |
| 18102 | **£259,657.30** |
| 17450 | **£194,550.79** |
| 16446 | **£168,472.50** |
| 14911 | **£143,825.06** |

**Discussion:** The top 5 customers generate £1,046,711.67 — nearly **9.8% of total clean revenue**. If any one of them stopped ordering, what would that mean for the business?

---

## Independent Work (Between Sessions 2 & 3)

Each sub-group takes one dimension:
- **Sub-group A:** Product performance analysis
- **Sub-group B:** Geographic / international expansion analysis
- **Sub-group C:** Seasonal and time-based patterns

### Sub-group A — Product Performance

**Top 10 products by Revenue** (SUMIF on Description):

| Product | Revenue |
|---|---|
| DOTCOM POSTAGE | **£206,248.77** |
| REGENCY CAKESTAND 3 TIER | **£174,484.74** |
| PAPER CRAFT , LITTLE BIRDIE | **£168,469.60** |
| WHITE HANGING HEART T-LIGHT HOLDER | **£106,292.77** |
| PARTY BUNTING | **£99,504.33** |

**Important data quality discussion:**
- "DOTCOM POSTAGE" and "POSTAGE" are not physical products — they are shipping charges. Should they be included in a product revenue analysis?
- Groups must decide and justify their approach.

**Build:** Revenue concentration analysis — what % of revenue comes from the top 50 products (out of 4,015)?

### Sub-group B — Geographic Analysis

| Country | Revenue | % of Total |
|---|---|---|
| United Kingdom | £9,025,222.08 | 84.6% |
| Netherlands | £285,446.34 | 2.7% |
| EIRE | £283,453.96 | 2.7% |
| Germany | £228,867.14 | 2.1% |
| France | £209,715.11 | 2.0% |
| Australia | £138,521.31 | 1.3% |

Build SUMIFS for each of the top 8 international markets.
**Analysis question:** If the company's goal is to reach 25% international revenue (from current 15.4%), which 3 markets should they invest in most? Support your answer with the data.

### Sub-group C — Seasonal Patterns

**Monthly Revenue (clean data):**

| Month | Revenue | Invoices |
|---|---|---|
| Dec-10 | £823,746.14 | 1,559 |
| Jan-11 | £691,364.56 | 1,086 |
| Feb-11 | £523,631.89 | 1,100 |
| Mar-11 | £717,639.36 | 1,454 |
| Apr-11 | £537,808.62 | 1,246 |
| May-11 | £770,536.02 | 1,681 |
| Jun-11 | £761,739.90 | 1,533 |
| Jul-11 | £719,221.19 | 1,475 |
| Aug-11 | £759,138.38 | 1,361 |
| Sep-11 | £1,058,590.17 | 1,837 |
| Oct-11 | £1,154,979.30 | 2,040 |
| Nov-11 | £1,509,496.33 | 2,769 |
| Dec-11 | £638,792.68 | 819 |

**Note:** December 2011 appears low because the data ends on 09/12/2011 — an incomplete month. Groups must flag this caveat in their presentation.

**Question:** What is the "Christmas preparation window" in this data? When does the pre-Christmas surge begin and peak?

---

## Session 3 (Wednesday, Week 8): Pivot Tables & Charts

**Objective:** Build the analytical layer and identify the 3 key strategic findings.

### Pivot Tables to Build

**Pivot 1: Monthly Revenue Trend**
- Rows: Month (from InvoiceDate grouped), Values: Sum of Revenue + Count of InvoiceNo
- Dual view: both value (£) and volume (invoices) over time
- Insert: Line chart showing the November 2011 peak

**Pivot 2: Revenue by Country (International Focus)**
- Rows: Country, Values: Sum of Revenue
- Filter: exclude United Kingdom to see the international picture clearly
- Insert: Horizontal bar chart

**Pivot 3: Customer Segmentation Summary**
- From your Customer Analysis sheet: Segment Tier, Count of customers, Total Revenue
- Insert: Pie chart showing what % of revenue comes from Top Tier vs Standard customers

**Pivot 4: Top 20 Products by Revenue**
- Rows: Description, Values: Sum of Revenue
- Top 10 filter applied
- Insert: Horizontal bar chart (Top 10 products)
- Add slicer: UKorInternational

**Dashboard preview check:** Do all 4 charts tell a coherent story about the business?

---

## Session 4 (Thursday, Week 8): Final Dashboard & Presentation

**Objective:** Build the polished final dashboard and prepare presentation narrative.

### Dashboard Sheet

**KPI Row:**

| KPI | Formula | Verified Value |
|---|---|---|
| Total Revenue | `=SUM(RetailClean[Revenue])` | **£10,666,684.54** |
| Total Transactions | `=COUNTA(RetailClean[InvoiceNo])` | **~530,104** |
| Unique Customers | Distinct CustomerID count | **4,338** |
| International Revenue % | International / Total | **15.4%** |
| Q4 2011 Revenue | SUMIFS | **£3,303,268.31** |
| Revenue Growth (Q4 2010 → Q4 2011) | (Q4 2011 - Q4 2010) / Q4 2010 | **+301%** |

**Charts on Dashboard:**
1. Monthly Revenue trend (line chart — the full 13-month picture)
2. Top 10 International Markets (horizontal bar — excluding UK)
3. Customer Tier Distribution (pie — revenue by tier)
4. Top 10 Products by Revenue (bar)

**Slicers:** `UKorInternational` and `YearQuarter` — both connected to all charts

### Final Verification Checklist

Before presenting, verify these numbers match:
- [ ] Total clean revenue = **£10,666,684.54**
- [ ] International revenue = **£1,641,462.46 (15.4%)**
- [ ] Q4 2011 is the highest quarter at **£3,303,268.31**
- [ ] November 2011 is the highest single month at **£1,509,496.33**
- [ ] Top customer (ID 14646) revenue = **£280,206.02**

---

## Deliverables

### Excel Workbook (60%)

| Sheet | Contents | Marks |
|---|---|---|
| `Clean Data` | Extended Power Query output (~530K rows, 12 columns) | 10 |
| `Project Analysis` | Quarterly revenue, UK vs International, customer distribution | 15 |
| `Customer Analysis` | Customer tiers, top customers by revenue | 15 |
| `Pivot Analysis` | 4 pivot tables + charts, verified values | 10 |
| `Dashboard` | 6 KPIs, 4 charts, 2 slicers, professional formatting | 10 |

### Presentation (40%)

**10 minutes. Structure:**
1. Business context: what this data represents (1 min)
2. Revenue trajectory: 301% quarterly growth — what's driving it? (2 min)
3. Customer concentration risk: top 5 customers = 9.8% of revenue (2 min)
4. International expansion: current state and 3-market recommendation (3 min)
5. One risk and one opportunity the board should act on (2 min)

**Assessment:**

| Criteria | Marks |
|---|---|
| Business insight quality | 15 |
| Visual communication | 15 |
| Technical accuracy | 10 |

---

## Expected Business Insights

Groups that complete this project correctly should be able to state:

1. **Revenue grew 301% from Q4 2010 to Q4 2011.** This is a wholesale Christmas gifting business — the business is highly seasonal and the Q4 surge is structural, not a one-off event. The company must plan inventory and staffing accordingly.

2. **Customer concentration is a significant risk.** The top 5 customers generate 9.8% of total revenue. Losing even one of them would be material. The company should identify retention strategies for these high-value wholesale accounts.

3. **International revenue is 15.4% of total, with Netherlands, EIRE, and Germany as the top markets.** These three countries together represent 7.5% of total revenue. If the company targets 25% international, these markets have proven demand and should receive dedicated account management.

4. **Anonymous transactions (no CustomerID) represent 24.9% of rows.** This means the company cannot identify nearly a quarter of its customers. A customer account incentive programme would unlock significant retention and retargeting capability.
