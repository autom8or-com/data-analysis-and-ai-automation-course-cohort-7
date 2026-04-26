# Phase 1 Project: Customer Satisfaction Intelligence
**Group 1 — Amazon Product Reviews Analysis**

## Project Overview

Your task: analyze **50,000 Amazon product reviews** to understand customer satisfaction patterns and identify which products generate the most helpful reviews. You'll build a professional dashboard that helps product managers understand review quality, not just quantity.

**Dataset:** Amazon Reviews (50,000 reviews across 20,290 products from 2002–2012)
**Duration:** 2 weeks
**Deliverable:** Excel dashboard with 3–4 summary sheets + 1 interactive pivot analysis

---

## Business Context

Amazon sellers and product managers need to understand:
1. **Which products have the most reviews?** (product visibility)
2. **What's the average rating?** (customer satisfaction)
3. **Which reviews are most helpful?** (review credibility)
4. **How has satisfaction changed over time?** (trends)

Your analysis will help leadership identify top-performing products and understand review quality beyond star ratings.

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total reviews | 50,000 |
| Unique products | 20,290 |
| Unique reviewers | 37,663 |
| Date range | Feb 2002 – Oct 2012 |
| **Average rating** | **3.0 / 5.0** |
| **High-value reviews** (HelpRatio ≥ 0.75) | **15,968 (31.9%)** |

### Columns in your data
- **ProductId** — Amazon product identifier
- **Score** — Star rating (1–5)
- **HelpRatio** — Proportion of reviewers who found the review helpful (0–1)
- **ReviewDate** — Date review was posted
- **Summary** — Review title
- **Text** — Full review body (not needed for analysis)

---

## Key Questions to Answer

### Week 1: Data Exploration & Formulas

**Q1: Which products have the most reviews?**
- Use COUNTIF to count reviews per product
- **Expected answer (top product):** Product B006MONQMC has 92 reviews

**Q2: What's the average rating?**
- Use AVERAGEIF to calculate average score
- **Expected answer:** Overall average is 3.0 / 5.0
- Also calculate by rating level (1-star, 2-star, etc.)

**Q3: How many high-value reviews does each product have?**
- Use COUNTIFS to count reviews with HelpRatio ≥ 0.75
- Create a column: `High-Value Review Count`
- **Expected answer:** 15,968 total high-value reviews across all products

**Q4: What's the help ratio trend by year?**
- Use SUMIFS and COUNTIFS to calculate average HelpRatio by year
- **Expected answer:** Average HelpRatio by year ranges from 0.30 (2002) to 0.41 (2012)

### Week 2: Pivot Tables & Dashboard

**Q5: Create a pivot table summarizing:**
- Rows: Star rating (1–5)
- Values: Count of reviews, Average HelpRatio
- **Expected output:**
  - Each star rating has exactly 10,000 reviews (the data is perfectly balanced)
  - 5-star reviews have avg HelpRatio of 0.45; 1-star has 0.35

**Q6: Build a dashboard with:**
- KPI cards: total reviews, average rating, high-value review count
- Trend chart: reviews posted per year
- Summary table: top 10 products by review count
- Pivot table: rating distribution

---

## Deliverables

### Week 1: Data Analysis Workbook
- **Raw Data sheet** (1,000-row sample for exploration)
- **Analysis sheet** with formulas answering Q1–Q4
  - Column headers: ProductId, ReviewCount, AvgRating, HighValueCount, HelpRatioByYear
  - All COUNTIF, AVERAGEIF, COUNTIFS formulas written correctly
  - Expected: 20 rows of unique products with metrics

### Week 2: Dashboard Workbook
- **Data Preparation sheet** (pivot table source data)
- **Summary KPIs sheet** (3–4 key metrics as large cards)
- **Analysis Pivot** sheet (pivot table from Q5)
- **Trend Analysis** sheet (chart + supporting data showing reviews by year)
- **Top Products** sheet (static table of top 10 products ranked by review count)

---

## Grading Rubric

| Criteria | Weight | Full (90–100%) | Partial (70–89%) | Incomplete (<70%) |
|---|---|---|---|---|
| **Formulas Correct** | 25% | All COUNTIF, AVERAGEIF, COUNTIFS formulas calculate correct values; proper cell references; no hardcoded numbers | Most formulas correct; 1–2 calculation errors; generally good references | Multiple formula errors; hardcoded values; incorrect logic |
| **Data Accuracy** | 25% | All expected KPIs match verified outputs (avg rating, high-value count, product counts) | KPIs within 5% of expected; minor rounding errors | KPIs significantly off; major calculation errors |
| **Dashboard Design** | 20% | Professional layout; clear labels; consistent formatting; easy to read; appropriate chart types | Readable but basic; some formatting inconsistencies; charts present but not optimized | Poorly organized; hard to read; missing key visuals |
| **Pivot Table Quality** | 15% | Pivot table correctly structured; rows/values/filters logical; matches expected output | Pivot table present; mostly correct structure; minor issues | Pivot table missing or incorrect structure |
| **Documentation** | 15% | Clear sheet names; column labels; formula comments where needed; executive summary | Most sheets labeled; basic clarity | Missing labels; confusing structure |

---

## Timeline

**Week 1 (2 sessions = 4 hours)**
- Session 1 (Wed): Import data, create Analysis sheet, write COUNTIF & AVERAGEIF formulas (Q1–Q2)
- Session 2 (Thu): Complete COUNTIFS & SUMIFS formulas (Q3–Q4); prepare for pivot tables

**Week 2 (2 sessions = 4 hours)**
- Session 3 (Wed): Build pivot tables, create Summary KPIs sheet, design layouts
- Session 4 (Thu): Complete charts, assemble dashboard, polish & present

---

## Success Criteria

✅ All formulas working and producing verified KPIs  
✅ Dashboard is professional and clearly communicates insights  
✅ Pivot tables correctly summarize the data  
✅ Presentation: each group presents their 3 key findings in 5 minutes  

---

## Resources

- **Formula Cheatsheet:** `curriculum/phase-1-excel/resources/excel-formula-cheatsheet.md`
- **Keyboard Shortcuts:** `curriculum/phase-1-excel/resources/keyboard-shortcuts.md`
- **Teaching curriculum:** Weeks 1–6 contain verified examples of all techniques you'll use

---

## Notes

- The data is intentionally balanced: exactly 10,000 reviews per star rating. This makes it easier to spot trends.
- "Help Ratio" measures whether other reviewers found this review helpful. A review with HelpRatio = 1.0 means everyone who voted found it helpful; 0.0 means no one did.
- You are NOT expected to analyze the review text — only the structured metadata (ratings, dates, help ratio).
- Focus on insights, not volume: "Which products have the highest-quality reviews?" is more interesting than "Which products have the most reviews?"
