# Phase 1 Project: Publishing Market Intelligence
**Group 3 — Bestseller Genre Analysis**

## Project Overview

Your task: analyze **550 bestselling books** to understand publishing trends, identify which genres command premium prices, and uncover which authors dominate the market. You'll build a dashboard that helps a publishing house decide where to invest in new titles.

**Dataset:** Bestselling Books with Categories (550 books across 2 genres from 2009–2019)
**Duration:** 2 weeks
**Deliverable:** Excel dashboard analyzing genre trends, author influence, and pricing strategy

---

## Business Context

A publishing house needs to understand:
1. **Which genres are most popular?** (market demand)
2. **Can we price Non-Fiction higher?** (revenue strategy)
3. **Which authors drive sales?** (author strategy)
4. **Are highly-rated books priced differently?** (quality vs. price perception)

Your analysis will inform catalog decisions and pricing strategy.

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total books | 550 |
| Unique authors | 248 |
| Genres | 2 (Fiction, Non-Fiction) |
| **Average price** | **£13.10** |
| **Average rating** | **4.62 / 5.0** |
| **Highly-rated books** (4.5+) | **452 (82.2%)** |
| **Price range** | **£0.00 – £105.00** |
| Year range | 2009–2019 |

### Columns in your data
- **Name** — book title
- **Author** — author name
- **Genre** — Fiction or Non-Fiction
- **Price** — selling price (£)
- **User Rating** — average rating (0–5.0 stars)
- **Reviews** — number of reviews (popularity indicator)
- **Year** — publication year

---

## Key Questions to Answer

### Week 1: Genre & Author Analysis

**Q1: How many books are in each genre?**
- Use COUNTIF to count books by genre
- **Expected answers:**
  - Non-Fiction: 310 books
  - Fiction: 240 books

**Q2: What's the average price and rating by genre?**
- Use AVERAGEIF to calculate average price and rating per genre
- **Expected answers:**
  - Non-Fiction: avg price £14.84, avg rating 4.60
  - Fiction: avg price £10.85, avg rating 4.65 (slightly higher rated, cheaper)

**Q3: Which authors have the most bestsellers?**
- Use COUNTIF to count books per author
- Find the top 5 authors by book count
- **Expected top 5:**
  - Jeff Kinney: 12 books
  - Suzanne Collins: 11 books
  - Rick Riordan: 11 books
  - Gary Chapman: 11 books
  - American Psychological Association: 10 books

**Q4: What's the average price of highly-rated books (4.5+ stars)?**
- Use AVERAGEIF to filter by rating ≥ 4.5
- Compare to books with lower ratings
- **Expected answer:** 452 books rated 4.5+, avg price £13.25

### Week 2: Pricing Strategy & Dashboard

**Q5: Create a pivot table:**
- Rows: Genre
- Columns: Rating tier (e.g., 4.5–5.0, 4.0–4.5, <4.0)
- Values: Average Price, Count
- **Expected output:** Shows Non-Fiction commands higher prices across most rating tiers

**Q6: Build a dashboard showing:**
- KPI cards: total books, average rating, average price
- Genre comparison (book count, avg price, avg rating)
- Top 10 authors (ranked by number of bestsellers)
- Price distribution chart
- Insight: Which genre should we expand?

---

## Deliverables

### Week 1: Analysis Workbook
- **Raw Data sheet** (1,000-row sample, or full 550-row dataset)
- **Genre Analysis sheet** with formulas:
  - Columns: Genre, Book Count, Avg Price, Avg Rating, Total Revenue (Price × Count)
  - All COUNTIF and AVERAGEIF formulas
  - **Expected:** 2 rows (Fiction, Non-Fiction)

- **Author Ranking sheet**:
  - Columns: Author, Book Count, Avg Price, Max Rating
  - Top 10 authors by book count
  - All COUNTIF formulas for each author (or use advanced filtering)
  - **Expected:** 10 rows with Jeff Kinney at the top (12 books)

### Week 2: Dashboard Workbook
- **Summary KPIs sheet** with cards:
  - Total Books (550)
  - Average Rating (4.62)
  - Average Price (£13.10)
  - High-Quality Books (4.5+): 452

- **Genre Strategy sheet** (pivot or summary):
  - Book count by genre
  - Average price by genre (Non-Fiction premium: £14.84 vs £10.85)
  - Average rating by genre
  - Recommendation: Non-Fiction commands 37% premium; high demand

- **Author Intelligence sheet**:
  - Top 10 authors with book counts
  - Bar chart showing author dominance

- **Price Distribution sheet**:
  - Chart showing how many books at each price point
  - Highlights the concentration around £10–£15

---

## Grading Rubric

| Criteria | Weight | Full (90–100%) | Partial (70–89%) | Incomplete (<70%) |
|---|---|---|---|---|
| **Formulas Correct** | 25% | All COUNTIF and AVERAGEIF formulas calculate correctly; proper genre/rating filters; cell references accurate | Most formulas correct; 1–2 minor calculation errors; generally good logic | Multiple formula errors; hardcoded values; missing filters |
| **Genre Analysis** | 20% | Correctly identifies Non-Fiction premium (£14.84 vs £10.85); all genre metrics accurate | Genre comparison present; most calculations correct; minor discrepancies | Incomplete or inaccurate genre analysis |
| **Author Ranking** | 20% | Top 10 authors correctly ranked; Jeff Kinney leads (12 books); all counts verified | Author ranking mostly correct; 1–2 ranking errors | Incomplete or incorrect author analysis |
| **Dashboard Quality** | 20% | Professional layout; clear comparisons; easy to see Non-Fiction premium; charts support findings | Good layout; charts present; comparisons visible but not highlighted | Poor organization; unclear visuals; findings hard to extract |
| **Pricing Insight** | 15% | Dashboard clearly shows Non-Fiction pricing strategy; comparison between genres obvious | Pricing data present; insight partially clear | Pricing analysis missing or unclear |

---

## Timeline

**Week 1 (2 sessions = 4 hours)**
- Session 1 (Wed): Import data, create Genre Analysis sheet, write COUNTIF & AVERAGEIF (Q1–Q2)
- Session 2 (Thu): Complete Author Ranking, analyze highly-rated books (Q3–Q4)

**Week 2 (2 sessions = 4 hours)**
- Session 3 (Wed): Build pivot tables for rating/genre breakdown; create KPI sheet
- Session 4 (Thu): Build charts, assemble dashboard, present strategy

---

## Success Criteria

✅ All formulas producing verified KPIs (genre counts, author rankings, prices)  
✅ Dashboard clearly shows Non-Fiction pricing premium (37% higher)  
✅ Author analysis identifies Jeff Kinney and other prolific authors  
✅ Presentation: recommend where to invest in new titles based on genre/author trends (5 min)  

---

## Key Insights to Highlight

**Non-Fiction Pricing Premium:** Non-Fiction books average £14.84 vs £10.85 for Fiction — a 37% premium. This suggests buyers perceive Non-Fiction as higher-value (educational, practical).

**Author Dominance:** Jeff Kinney (Diary of a Wimpy Kid series) has 12 bestsellers — nearly 5× the average author. Serial authors drive catalog value.

**High Quality Across the Board:** 82.2% of bestsellers have ratings ≥ 4.5. This is a filtered dataset (bestsellers only), so of course quality is high — it's what makes them bestsellers.

---

## Resources

- **Formula Cheatsheet:** Covers COUNTIF and AVERAGEIF with examples
- **Pivot Table Guide:** Week 4 teaching curriculum
- **Keyboard Shortcuts:** Available in resources folder

---

## Notes

- Some books have £0.00 price (likely free promotional editions). Include them in analysis but note in your dashboard.
- "Reviews" column indicates popularity / social proof, not quality. A book with 50,000 reviews is more visible than one with 1,000 reviews, even if ratings are similar.
- This dataset is *bestsellers only*. It's a biased sample: low-quality books don't become bestsellers. For a full market analysis, you'd need all published books, including the 99% that never chart.
- Focus on actionable insights: "Should we expand our Non-Fiction catalog?" is better than "Non-Fiction is more expensive."
