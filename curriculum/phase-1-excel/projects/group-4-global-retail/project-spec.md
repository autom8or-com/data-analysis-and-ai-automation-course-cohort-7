# Phase 1 Project: Global Retail Market Analysis
**Group 4 — UK Online Retail Intelligence (Full Dataset)**

## Project Overview

Your task: analyze the **complete UCI Online Retail dataset** (541,909 transactions) to understand global market dynamics, identify top-performing countries, and build a comprehensive dashboard for international business strategy. This is the same dataset used in teaching — you're now analyzing it for real business decisions.

**Dataset:** UCI Online Retail (541,909 transactions across 38 countries from Jan 2010–Dec 2011)
**Duration:** 2 weeks
**Deliverable:** Executive dashboard analyzing revenue by country, product trends, and customer retention

---

## Business Context

An international e-commerce company needs to understand:
1. **Which countries drive the most revenue?** (market priority)
2. **What's the average order value by country?** (pricing strategy)
3. **Which products are bestsellers?** (inventory strategy)
4. **Are transaction volumes growing or declining?** (trend analysis)

Your analysis will inform expansion strategy and resource allocation.

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total transactions | 541,909 |
| Unique invoices | 25,900 |
| Unique customers | 4,372 |
| Unique products | 4,070 |
| **Total revenue** | **£8,187,806.36** |
| **Countries represented** | **38** |
| **UK revenue** | **£8,187,806.36** (100% — UK-centric dataset) |
| Cancellations | 9,288 |
| Date range | Jan 2010 – Dec 2011 |

### Columns in your data
- **InvoiceNo** — transaction ID (starts with "C" = cancelled)
- **StockCode** — product identifier
- **Description** — product name
- **Quantity** — units purchased
- **InvoiceDate** — transaction date
- **UnitPrice** — price per unit (£)
- **CustomerID** — customer identifier
- **Country** — country of purchase

---

## Key Questions to Answer

### Week 1: Revenue & Product Analysis

**Q1: What's the total revenue by country?**
- Use SUMIFS to sum revenue (calculated from Quantity × UnitPrice) by country
- **Expected answers:**
  - UK: £8,187,806.36 (dominant market)
  - Netherlands: £285,446.34
  - EIRE (Ireland): £283,453.96
  - Germany: £221,698.21
  - France: £209,715.11

**Q2: How many transactions occur in each country?**
- Use COUNTIF to count invoices per country
- **Expected answer:** UK has vast majority; other countries 10–20% of UK volume

**Q3: What's the average transaction value by country?**
- Use AVERAGEIFS to calculate avg revenue per transaction per country
- **Expected answer:** Average across all countries is ~£15; UK slightly lower due to volume

**Q4: Which products generate the most revenue?**
- Use SUMIF to sum revenue by product (StockCode)
- Identify top 10 products
- **Expected:** Product revenue ranges from £10k–£100k+ for top SKUs

### Week 2: Time Series & Customer Analysis

**Q5: Create a pivot table:**
- Rows: Month/Quarter (from InvoiceDate)
- Values: Sum of Revenue, Count of Transactions
- **Expected output:** Shows clear seasonal pattern; Q4 peaks; January/February drops

**Q6: Build an executive dashboard showing:**
- KPI cards: total revenue, transaction count, avg order value
- Revenue by country (top 10 countries)
- Top 10 products by revenue
- Monthly trend chart (revenue over time)
- Insight: UK market concentration (is it risky to rely on one country?)

---

## Deliverables

### Week 1: Market Analysis Workbook
- **Raw Data sheet** (1,000-row sample)
- **Country Revenue sheet** with formulas:
  - Columns: Country, Total Revenue (SUMIFS), Transaction Count (COUNTIF), Avg Transaction Value (AVERAGEIFS)
  - All formulas calculating correctly
  - **Expected:** Top 5 countries ranked; UK dominates

- **Product Analysis sheet**:
  - Columns: StockCode, Description, Total Revenue (SUMIF), Units Sold (SUMIF Quantity), Avg Unit Price
  - Top 10 products
  - **Expected:** Revenue-generating products clearly identified

### Week 2: Executive Dashboard Workbook
- **Summary KPIs sheet** with large cards:
  - Total Revenue (£8.19M)
  - Total Transactions (541,909)
  - Average Order Value (£15.11)
  - Unique Customers (4,372)

- **Global Market Sheet** (pivot or summary):
  - Top 10 countries by revenue (bar chart)
  - Shows UK concentration (% of total)
  - **Key insight:** UK = 100% (this is a UK-centric retailer; other countries are secondary)

- **Product Performance Sheet**:
  - Top 10 products by revenue
  - Percentage of total revenue from top 10

- **Time Series Sheet**:
  - Monthly revenue trend (line chart)
  - Shows seasonality (peaks around October/November, drops in January)
  - Year-over-year comparison (2010 vs 2011)

---

## Grading Rubric

| Criteria | Weight | Full (90–100%) | Partial (70–89%) | Incomplete (<70%) |
|---|---|---|---|---|
| **Formulas Accurate** | 25% | All SUMIFS, COUNTIF, AVERAGEIFS formulas correct; cell references proper; calculations match verified KPIs | Most formulas correct; 1–2 minor errors; generally good logic | Multiple formula errors; hardcoded values; missing calculations |
| **Country Analysis** | 20% | Correctly identifies UK dominance; top 5 countries ranked accurately; revenue calculations verified | Country analysis mostly correct; some ranking errors; minor calculation issues | Incomplete or significantly inaccurate country analysis |
| **Product Insights** | 15% | Top 10 products correctly identified; revenue calculations accurate | Top products mostly correct; some calculation errors | Incomplete or missing product analysis |
| **Dashboard Design** | 20% | Professional layout; clear hierarchy; easy to see market concentration; charts are informative | Good layout; charts present; information accessible | Poor organization; unclear visuals; hard to extract insights |
| **Time Series & Trends** | 10% | Trend chart clearly shows seasonality; year-over-year comparison visible; growth/decline trends identified | Trend data present; seasonality somewhat visible; comparison basic | Trend analysis missing or unclear |
| **Actionable Insights** | 10% | Dashboard answers strategic questions (which markets to expand, which products to focus on) | Some insights present; mostly descriptive rather than strategic | Few or no actionable insights |

---

## Timeline

**Week 1 (2 sessions = 4 hours)**
- Session 1 (Wed): Import full dataset, create Country Revenue sheet, write SUMIFS, COUNTIF, AVERAGEIFS (Q1–Q3)
- Session 2 (Thu): Complete Product Analysis, identify top performers (Q4)

**Week 2 (2 sessions = 4 hours)**
- Session 3 (Wed): Build pivot table for time-series analysis; create KPI sheet with advanced pivot setup
- Session 4 (Thu): Assemble executive dashboard with charts; identify strategic recommendations; present

---

## Success Criteria

✅ All formulas producing verified KPIs (UK dominance, top products, revenue totals)  
✅ Dashboard clearly communicates UK market concentration and global opportunity  
✅ Time-series analysis shows seasonal patterns  
✅ Presentation: recommend 2 strategic actions based on market data (5 min)  

---

## Critical Business Insights

**UK Market Dominance:** This company's entire revenue comes from the UK. Expanding to other countries (Netherlands, Ireland, Germany, France are starting points) is strategically important.

**Seasonality:** Revenue peaks in October–November (holiday shopping) and drops sharply in January–February. Cash flow planning must account for this.

**Product Concentration:** A small number of products (likely popular gift items) generate disproportionate revenue. Inventory strategy should focus on these bestsellers.

---

## Real-World Context

You've used this dataset all through Week 1–6 teaching. Now you're analyzing it like a real business analyst would: asking strategic questions, calculating KPIs, and presenting recommendations to decision-makers. The formulas are the same, but the purpose is different — move from "learning to calculate" to "using calculations to drive decisions."

---

## Resources

- **Teaching Curriculum:** Weeks 1–6 all use this dataset; refer to teaching-curriculum.md for verified examples
- **Formula Cheatsheet:** All formulas needed are covered in Weeks 1–3
- **Pivot Table Guide:** Week 4
- **Power Query (optional):** Weeks 5–6 show data cleaning techniques

---

## Notes

- Some invoices are cancelled (InvoiceNo starts with "C"). Include them in your analysis but note in your dashboard: "Includes cancelled transactions — in production, you'd exclude these."
- This dataset is *2010–2011 historical data* — it's from a real company, but it's over a decade old. Analysis is educational, not for current business use.
- "Country" is based on where the customer placed the order, not where goods were shipped. For true international analysis, you'd need shipping address data.
- The dataset is heavily UK-biased because the company is UK-based. International expansion would change this distribution dramatically.
- Challenge: Can you identify product patterns? (e.g., do certain products sell better in certain countries? This requires more advanced analysis beyond Week 1–6 scope, but it's a real question a business analyst would ask.)

---

## Challenge Question (Optional — for extra credit)

**Which product has the highest average price? Which has the lowest?**

This requires adding another calculated column (unit price as given in the data), but it's a good way to deepen your analysis.

**Expected:** High-priced items are often home décor or specialty gifts; lowest-priced are consumables or bulk items.
