# Group 4 — Global Retail Market Analysis — Grading Rubric

## Overview
This rubric assesses Group 4's UCI Online Retail project across 6 dimensions. Each dimension has full (90–100%), partial (70–89%), and incomplete (<70%) criteria. Total weight = 100%.

**Total Points:** 100 | **Passing:** 70 | **Good:** 80 | **Excellent:** 90+

---

## Rubric Dimensions

### 1. Formulas Accurate (25 points)

**What we're assessing:** Do your SUMIFS, COUNTIF, and AVERAGEIFS formulas produce correct values from the full 541,909-row dataset?

| Score | Criteria |
|---|---|
| **23–25** (Full) | ✅ All formulas working correctly. UK revenue = £8,187,806.36. Top 5 countries calculated: Netherlands £285k, EIRE £283k, Germany £222k, France £210k. AVERAGEIFS for avg transaction value correct. COUNTIF for transaction counts correct by country. All cell references proper, no hardcoding. |
| **17–22** (Partial) | ⚠️ Most formulas correct (85–95%). Top countries present but 1–2 calculations off by <5%. Average transaction values within acceptable range. Some reference issues. |
| **<17** (Incomplete) | ❌ Multiple formula errors OR hardcoded values instead of formulas OR incorrect SUMIFS/AVERAGEIFS logic. Expected KPIs significantly off. |

**Specific checks:**
- [ ] Total revenue calculated = £8.19M?
- [ ] UK revenue = £8.19M (100% — dominance clear)?
- [ ] Top 5 countries ranked correctly?
- [ ] Average transaction value calculated (overall £15+)?
- [ ] COUNTIF for transaction counts working?

---

### 2. Country Analysis (20 points)

**What we're assessing:** Do you correctly analyze the UK market concentration and identify expansion opportunities?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Clearly identifies UK dominance (100% of total revenue or near-100%). Shows top 10 countries. Recognizes Netherlands, EIRE, Germany, France as growth opportunities. Analysis is complete: revenue, transaction count, avg order value by country. Insight: UK market concentration is a business risk. |
| **14–17** (Partial) | ⚠️ UK dominance identified but not emphasized. Top countries present; 1–2 calculations off. International expansion potential mentioned but not analyzed. |
| **<14** (Incomplete) | ❌ Country analysis missing/incorrect OR UK dominance not identified. |

**Specific checks:**
- [ ] UK revenue = 100% (or near-100%) of total?
- [ ] Top 5 countries ranked: Netherlands, EIRE, Germany, France, Sweden?
- [ ] % of total revenue shown for each country?

---

### 3. Product Insights (15 points)

**What we're assessing:** Do you correctly identify top-performing products?

| Score | Criteria |
|---|---|
| **14–15** (Full) | ✅ Top 10 products identified and ranked by revenue. SUMIF for product revenue working correctly. Recognizes product concentration (top 10 products = large % of total). Revenue-generating products clearly identified. |
| **11–13** (Partial) | ⚠️ Top products identified; 1–2 ranking errors. Revenue calculations mostly correct. Product concentration mentioned but not quantified. |
| **<11** (Incomplete) | ❌ Product analysis missing or significantly incorrect. Top products not identified. |

**Specific checks:**
- [ ] Top 10 products by revenue ranked?
- [ ] SUMIF calculating revenue by product (StockCode)?
- [ ] Revenue ranges reasonable (£10k–£100k+)?

---

### 4. Dashboard Design (20 points)

**What we're assessing:** Is your dashboard professional and highlighting key strategic insights?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Professional layout. KPI cards prominent (Total Revenue, Transactions, Avg Order Value, Customer Count). Country ranking chart clearly shows UK dominance. Top 10 products visible. Time series chart shows seasonality. Consistent formatting. Easy to read and navigate. |
| **14–17** (Partial) | ⚠️ Good layout; most charts present. UK dominance visible but not emphasized. Time series or product analysis less polished. Minor formatting issues. |
| **<14** (Incomplete) | ❌ Cluttered layout. Charts missing or hard to read. Formatting inconsistent. Strategic insights buried. |

**Specific checks:**
- [ ] KPI cards: Total Revenue (£8.19M), Transactions (541,909), Avg Order Value (£15), Customers (4,372)?
- [ ] Country ranking chart (bar chart showing top 10)?
- [ ] Top 10 products visible?
- [ ] Time series chart showing monthly/quarterly trend?

---

### 5. Time Series & Trends (10 points)

**What we're assessing:** Do you correctly analyze temporal patterns (seasonality, growth)?

| Score | Criteria |
|---|---|
| **9–10** (Full) | ✅ Time series chart clearly shows seasonality (peak Oct–Nov, drop Jan–Feb). Year-over-year comparison shows growth from 2010 to 2011. Trend is identifiable and explained. |
| **7–8** (Partial) | ⚠️ Time series present; seasonality partially visible. Year-over-year data included but not emphasized. |
| **<7** (Incomplete) | ❌ Time series analysis missing or chart unclear. Trends not identified. |

**Specific checks:**
- [ ] Monthly revenue trend charted?
- [ ] Seasonality visible (Q4 peak, Q1 drop)?
- [ ] Year-over-year comparison shown (2010 vs 2011)?

---

### 6. Strategic Insight (10 points)

**What we're assessing:** Does your analysis provide actionable recommendations?

| Score | Criteria |
|---|---|
| **9–10** (Full) | ✅ Dashboard answers strategic questions: "Is UK concentration a risk?" (YES — entire revenue). "Where should we expand?" (Netherlands, EIRE, Germany top opportunities). "How do we manage seasonality?" (Insight: Q4 peaks, Q1 drops). Recommendations are data-driven. |
| **7–8** (Partial) | ⚠️ Insights present but not fully developed. Recommendations vague or not fully supported. |
| **<7** (Incomplete) | ❌ Strategic recommendations missing or unclear. |

**Specific checks:**
- [ ] Recommendation to expand internationally?
- [ ] Discussion of UK market concentration risk?
- [ ] Seasonality impact noted?

---

## Scoring Summary

| Dimension | Weight | Your Score | Weighted |
|---|---|---|---|
| Formulas Accurate | 25% | __/25 | __/25 |
| Country Analysis | 20% | __/20 | __/20 |
| Product Insights | 15% | __/15 | __/15 |
| Dashboard Design | 20% | __/20 | __/20 |
| Time Series & Trends | 10% | __/10 | __/10 |
| Strategic Insight | 10% | __/10 | __/10 |
| **TOTAL** | 100% | | **__/100** |

---

## Common Mistakes

1. **Large dataset = slow formulas:** SUMIFS on 541,909 rows can be slow. Use structured references (tables) or SUBTOTAL if filtering.
2. **Forgetting to exclude cancelled transactions:** If you want a "Net Revenue" analysis, filter out invoices starting with "C" using COUNTIF or manual filtering.
3. **Wrong date format:** InvoiceDate may be in various formats. Use DATE functions or pivot table date grouping for month/quarter analysis.
4. **Missing time series:** A project on a 2-year dataset MUST include time-based analysis (monthly or quarterly trend).
5. **Hardcoding country names:** Use SUMIFS with cell references: `=SUMIFS(revenue, country, A2)` not `=SUMIFS(revenue, country, "UK")`.

---

## Bonus (Optional, +5 points max)

- **Customer analysis:** Top 10 customers by revenue OR repeat purchase rate (+3 points)
- **Product category breakdown:** If available, analyze by product category or sub-category (+3 points)
- **Seasonal adjustment:** Calculate seasonal index (actual revenue vs. trend) (+3 points)
- **Executive brief:** 1-page strategic memo (market expansion, inventory planning, cash flow) (+3 points)

---

## Grade Scale

| Score | Grade | Interpretation |
|---|---|---|
| 90–100 | A | Excellent — identifies UK concentration risk; clear international expansion strategy; professional dashboard |
| 80–89 | B | Good — correct analysis; strong country and product insights; clear presentation |
| 70–79 | C | Acceptable — analysis mostly correct; insights present; some gaps in strategic recommendations |
| 60–69 | D | Below standard — multiple criteria not met |
| <60 | F | Incomplete or missing substantial work |

---

## Context Reminder

This is the same dataset you've analyzed throughout Weeks 1–6 teaching. You now understand it deeply. This project asks you to analyze it like a business analyst: move from "learning Excel techniques" to "using Excel to drive business decisions." Your formulas are the foundation; your insights are the value.

Good luck! 📊
