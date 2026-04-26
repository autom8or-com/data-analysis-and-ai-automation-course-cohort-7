# Phase 1 Project: Product Category Performance Analysis
**Group 2 — Superstore Sales Intelligence**

## Project Overview

Your task: analyze **9,994 sales transactions** from a global retail business to understand which product categories drive profit, identify underperforming segments, and build a dashboard for regional decision-makers. You'll uncover why a category with high sales might have low profit.

**Dataset:** Superstore (9,994 transactions across 3 product categories, 4 regions, 3 customer segments from Jan–Sep 2017)
**Duration:** 2 weeks
**Deliverable:** Excel dashboard with profit/sales analysis, regional breakdown, and segment comparison

---

## Business Context

The CFO needs to understand:
1. **Which categories are profitable?** (many companies sell at a loss)
2. **Which regions and segments drive profit?** (not all sales are equal)
3. **What's the profit margin by category?** (pricing strategy)
4. **Where are we losing money?** (unprofitable segments)

Your analysis will inform pricing, product focus, and regional strategy.

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total transactions | 9,994 |
| Unique orders | 5,009 |
| Unique customers | 793 |
| **Total sales** | **£2,297,200.86** |
| **Total profit** | **£286,397.02** |
| **Profit margin** | **12.5%** |
| Date range | Jan 2017 – Sep 2017 |

### Columns in your data
- **Order ID** — unique order identifier
- **Order Date** — when the order was placed
- **Category** — Furniture, Office Supplies, Technology
- **Sub-Category** — type within category (e.g., Tables, Chairs, Copiers)
- **Sales** — revenue (£)
- **Profit** — net profit after costs (£)
- **Quantity** — units sold
- **Segment** — Consumer, Corporate, Home Office
- **Region** — West, East, Central, South
- **State** — US state

---

## Key Questions to Answer

### Week 1: Category & Segment Analysis

**Q1: What's the total sales and profit by category?**
- Use SUMIF to calculate sales and profit for each category
- **Expected answers:**
  - Furniture: £742,000 sales, £18,451 profit (2.5% margin — unprofitable!)
  - Office Supplies: £719,047 sales, £122,491 profit (17% margin)
  - Technology: £836,154 sales, £145,455 profit (17.4% margin)

**Q2: Which segment is most profitable?**
- Use SUMIFS to calculate profit by segment
- **Expected answers:**
  - Consumer: £134,119 profit (47% of total)
  - Corporate: £91,979 profit (32% of total)
  - Home Office: £60,299 profit (21% of total)

**Q3: What's the average profit per transaction by category?**
- Use AVERAGEIF to calculate average profit
- **Expected answers:**
  - Furniture: £2.29 per transaction (highly unprofitable!)
  - Office Supplies: £5.35 per transaction
  - Technology: £20.97 per transaction

**Q4: How many transactions are profitable vs. unprofitable?**
- Use COUNTIF to count transactions where Profit < 0
- **Expected answer:** Approximately 1,000+ transactions are unprofitable (negative profit)

### Week 2: Regional Analysis & Dashboard

**Q5: Create a pivot table:**
- Rows: Region
- Columns: Category
- Values: Sum of Profit
- **Expected output:** Shows which regions/category combinations are losing money

**Q6: Build a dashboard showing:**
- KPI cards: total sales, total profit, profit margin %
- Category breakdown (% of total profit by category)
- Region ranking (profit by region)
- Segment comparison (profit by segment)
- Critical insight: Which category is dragging down profit?

---

## Deliverables

### Week 1: Analysis Workbook
- **Raw Data sheet** (1,000-row sample)
- **Category Analysis sheet** with formulas:
  - Columns: Category, Total Sales, Total Profit, Profit Margin %, Avg Profit per Transaction
  - All SUMIF and AVERAGEIF formulas calculating correctly
  - **Expected:** 3 rows (one per category)

- **Segment Analysis sheet**:
  - Columns: Segment, Total Profit, Transaction Count, Avg Profit per Transaction
  - All SUMIFS and COUNTIF formulas
  - **Expected:** 3 rows (Consumer, Corporate, Home Office)

### Week 2: Dashboard Workbook
- **Summary KPIs sheet** with 4 large metric cards:
  - Total Sales (£2.3M)
  - Total Profit (£286k)
  - Profit Margin (12.5%)
  - Unprofitable Transactions (count)

- **Category Profitability sheet** (pivot or summary):
  - Shows Furniture is the profit problem
  - Includes margin % by category

- **Regional Performance sheet**:
  - Profit by region, ranked
  - **Expected:** West (£268k) > East (£251k) > Central (£190k) > South (£-76k — NEGATIVE!)

- **Segment Comparison sheet**:
  - Bar chart comparing profit by segment
  - Shows Consumer drives most profit

---

## Grading Rubric

| Criteria | Weight | Full (90–100%) | Partial (70–89%) | Incomplete (<70%) |
|---|---|---|---|---|
| **Formulas Accurate** | 25% | All SUMIF, SUMIFS, AVERAGEIF, COUNTIF formulas correct; cell references proper; calculations match expected values | Most formulas correct; 1–2 minor calculation errors; generally good logic | Multiple formula errors; hardcoded values; incorrect grouping |
| **Category Analysis** | 20% | Correctly identifies Furniture as unprofitable; calculates all margins accurately | Identifies key categories but some margin calculations off | Missing category analysis or major calculation errors |
| **Segment Breakdown** | 15% | Correctly segments profit by Consumer/Corporate/Home Office; identifies Consumer as top performer | Segmentation mostly correct; minor calculation errors | Incomplete or incorrect segment analysis |
| **Dashboard Design** | 20% | Professional, clear layout; appropriate charts; easy to spot the profit problem; KPI cards prominent | Readable layout; basic charts; insights present but not highlighted | Poor organization; unclear visuals; insights hard to find |
| **Regional Insight** | 10% | Dashboard clearly shows South region is unprofitable; chart supports finding | Regional data present; insight somewhat clear | Regional analysis missing or unclear |

---

## Timeline

**Week 1 (2 sessions = 4 hours)**
- Session 1 (Wed): Import data, create Category Analysis sheet, write SUMIF & AVERAGEIF (Q1, Q3)
- Session 2 (Thu): Complete Segment Analysis with SUMIFS (Q2, Q4); identify unprofitable patterns

**Week 2 (2 sessions = 4 hours)**
- Session 3 (Wed): Build pivot tables for regional analysis; create Summary KPIs sheet
- Session 4 (Thu): Assemble dashboard with charts; highlight key findings; present

---

## Success Criteria

✅ All formulas producing verified KPIs (Furniture unprofitability, segment breakdown)  
✅ Dashboard clearly communicates the profit problem (not all high-sales categories are profitable)  
✅ Pivot table correctly breaks down profit by region/category  
✅ Presentation: identify the 3 biggest profit drivers and 1 area of concern in 5 minutes  

---

## Critical Finding

**Furniture is a profit killer:** It represents 32% of sales (£742k) but only 6.4% of profit (£18k). This is the kind of insight that drives business strategy. Why? (This would require detailed analysis of costs — beyond Week 1–6 scope — but you're identifying the problem.)

---

## Resources

- **Formula Cheatsheet:** Weeks 1–3 cover SUMIF, SUMIFS, AVERAGEIF, COUNTIF with examples
- **Pivot Table Guide:** Week 4 teaching curriculum
- **Keyboard Shortcuts:** Available in resources folder

---

## Notes

- The South region shows **negative profit** overall. This is real in some datasets — a region may generate sales volume but at unsustainable margins.
- "Profit" = Sales − Cost of Goods Sold − Operating Expenses. A negative profit means the company lost money on that transaction.
- Focus on **why** (which categories/regions/segments drive profit), not just **how much**.
- Your dashboard should answer: "Where should we focus to improve profitability?" — insights matter more than numbers alone.
