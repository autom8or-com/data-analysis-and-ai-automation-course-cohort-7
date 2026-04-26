# Group 3 — Publishing Market Intelligence — Grading Rubric

## Overview
This rubric assesses Group 3's Bestseller project across 5 dimensions. Each dimension has a full score (90–100%), partial credit range (70–89%), and incomplete (<70%). Total weight = 100%.

**Total Points:** 100 | **Passing:** 70 | **Good:** 80 | **Excellent:** 90+

---

## Rubric Dimensions

### 1. Formulas Correct (25 points)

**What we're assessing:** Do your COUNTIF, AVERAGEIF, and analysis formulas produce correct values?

| Score | Criteria |
|---|---|
| **23–25** (Full) | ✅ All formulas working correctly. Non-Fiction: 310 books, £14.84 avg price; Fiction: 240 books, £10.85 avg price. COUNTIF for author book counts correct. AVERAGEIF for genre ratings correct (4.60 vs 4.65). All cell references proper, no hardcoding. |
| **17–22** (Partial) | ⚠️ Most formulas correct (85–95%). 1–2 minor calculation errors (e.g., genre count off by 5 books). Book counts or prices within 5% of expected. Some reference issues. |
| **<17** (Incomplete) | ❌ Multiple formula errors OR hardcoded values instead of formulas OR incorrect COUNTIF/AVERAGEIF logic. Expected KPIs significantly off. |

**Specific checks:**
- [ ] Non-Fiction book count = 310?
- [ ] Fiction book count = 240?
- [ ] Non-Fiction avg price = £14.84?
- [ ] Fiction avg price = £10.85?
- [ ] Top author (Jeff Kinney) = 12 books?

---

### 2. Genre Analysis (20 points)

**What we're assessing:** Do you correctly identify and communicate the Non-Fiction pricing premium?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Clearly identifies Non-Fiction commands 37% price premium (£14.84 vs £10.85). Shows breakdown by genre: book count, avg price, avg rating. Recognizes Non-Fiction is more expensive but slightly lower-rated. Analysis is complete and actionable (e.g., "expand Non-Fiction for higher margins"). |
| **14–17** (Partial) | ⚠️ Identifies price difference but doesn't emphasize the premium. Genre data present; some calculations correct but 1–2 off. Analysis present but not strategic. |
| **<14** (Incomplete) | ❌ Fails to identify pricing premium OR genre analysis missing/incorrect. |

**Specific checks:**
- [ ] Non-Fiction premium highlighted (37% higher price)?
- [ ] Both genres analyzed?
- [ ] Rating comparison included (4.60 vs 4.65)?

---

### 3. Author Ranking (20 points)

**What we're assessing:** Do you correctly rank authors and identify top performers?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Correctly ranks top 10 authors. Jeff Kinney at #1 (12 books), Suzanne Collins #2 (11), Rick Riordan #3 (11). COUNTIF for each author correct. Rankings verified. Recognizes serial authors drive catalog value. |
| **14–17** (Partial) | ⚠️ Top authors identified; Jeff Kinney recognized as #1. 1–2 ranking errors or book counts off by 1–2. Top 10 mostly correct. |
| **<14** (Incomplete) | ❌ Author analysis missing or significantly incorrect. Top author not identified. |

**Specific checks:**
- [ ] Jeff Kinney = 12 books (top)?
- [ ] Suzanne Collins, Rick Riordan, Gary Chapman all ~11 books?
- [ ] Top 10 authors ranked by book count?

---

### 4. Dashboard Design (20 points)

**What we're assessing:** Is your dashboard professional and clearly communicates the genre strategy?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Professional layout. Genre comparison chart clearly shows Non-Fiction premium. Author chart highlights Jeff Kinney dominance. KPI cards prominent. Consistent formatting. Easy to extract insights. |
| **14–17** (Partial) | ⚠️ Good layout; charts present. Genre premium visible but not emphasized. Author ranking present but basic visualization. Minor formatting issues. |
| **<14** (Incomplete) | ❌ Cluttered layout. Charts hard to read. Formatting inconsistent. Insights hard to extract. |

**Specific checks:**
- [ ] KPI cards: Total Books (550), Avg Rating (4.62), Avg Price (£13.10)?
- [ ] Genre comparison chart (side-by-side price bars)?
- [ ] Author ranking chart (top 10)?
- [ ] Professional formatting (bold headers, aligned)?

---

### 5. Pricing Insight (15 points)

**What we're assessing:** Does your analysis provide actionable insights about pricing strategy?

| Score | Criteria |
|---|---|
| **14–15** (Full) | ✅ Dashboard clearly answers: "Which genre should we expand?" Recommendation: Expand Non-Fiction (higher price point, strong demand). Shows how pricing strategy differs by genre. Actionable and data-driven. |
| **11–13** (Partial) | ⚠️ Pricing data present; some insight into genre differences. Recommendation vague or not fully supported by data. Analysis present but not strategic. |
| **<11** (Incomplete) | ❌ Pricing analysis missing or unclear. No strategic recommendation. |

**Specific checks:**
- [ ] Non-Fiction premium clearly communicated?
- [ ] Author concentration (Jeff Kinney) noted?
- [ ] High-quality books analysis (82.2% rated 4.5+)?

---

## Scoring Summary

| Dimension | Weight | Your Score | Weighted |
|---|---|---|---|
| Formulas Correct | 25% | __/25 | __/25 |
| Genre Analysis | 20% | __/20 | __/20 |
| Author Ranking | 20% | __/20 | __/20 |
| Dashboard Design | 20% | __/20 | __/20 |
| Pricing Insight | 15% | __/15 | __/15 |
| **TOTAL** | 100% | | **__/100** |

---

## Common Mistakes

1. **Miscounting books per genre:** COUNTIF should count books where Genre = "Non-Fiction", not include header. Ensure range is A2:A551 (550 books, not 551).
2. **Author COUNTIF syntax:** `=COUNTIF($D$2:$D$551, "Jeff Kinney")` — quote the name or reference the cell.
3. **Forgetting average calculations:** Don't just count; calculate average price and rating per genre for comparison.
4. **Missing top author:** Jeff Kinney must appear in your top 10 and be visually prominent (chart, bold, annotation).
5. **Vague language:** Instead of "Non-Fiction is more expensive," say "Non-Fiction averages £14.84 vs £10.85 — a 37% premium."

---

## Bonus (Optional, +5 points max)

- **Price distribution chart:** Histogram showing book prices at £0–5, £5–10, £10–20, £20+ (+3 points)
- **Rating vs. Price analysis:** Correlation chart showing whether highly-rated books are priced higher (+3 points)
- **Strategic memo:** 1-page recommendation memo (genre expansion, author strategy, pricing) (+3 points)

---

## Grade Scale

| Score | Grade | Interpretation |
|---|---|---|
| 90–100 | A | Excellent — identifies Non-Fiction premium; professional dashboard; strategic insights |
| 80–89 | B | Good — correct analysis; clear communication of pricing strategy |
| 70–79 | C | Acceptable — analysis mostly correct; insights present but not fully developed |
| 60–69 | D | Below standard — multiple criteria not met |
| <60 | F | Incomplete or missing substantial work |
