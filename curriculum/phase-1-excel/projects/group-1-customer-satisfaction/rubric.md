# Group 1 — Customer Satisfaction Intelligence — Grading Rubric

## Overview
This rubric assesses the Group 1 project across 5 dimensions. Each dimension has a full score (90–100%), partial credit range (70–89%), and incomplete (<70%). Total weight across all dimensions = 100%.

**Total Points:** 100  
**Passing Grade:** 70 (D) | **Good Grade:** 80 (B) | **Excellent Grade:** 90+ (A)

---

## Rubric Dimensions

### 1. Formula Accuracy (25 points)

**What we're assessing:** Do your COUNTIF, AVERAGEIF, and COUNTIFS formulas produce correct values? Are cell references proper?

| Score | Criteria |
|---|---|
| **23–25** (Full) | ✅ All formulas working correctly and producing verified outputs (see project spec for expected values). Cell references are absolute/mixed where appropriate. No hardcoded values. All COUNTIF, AVERAGEIF, COUNTIFS formulas present and correct. |
| **17–22** (Partial) | ⚠️ Most formulas correct (85–95% accuracy). 1–2 minor calculation errors or reference issues. Some formulas may use hardcoded values instead of cell references. Deduction for incomplete formula sets. |
| **<17** (Incomplete) | ❌ Multiple formula errors (>2) OR hardcoded values replacing formulas OR incorrect logic (e.g., COUNTIF pointing to wrong range). Missing expected formulas. |

**Specific checks:**
- [ ] COUNTIF for product review counts — does it match expected (Product B006MONQMC = 92)?
- [ ] AVERAGEIF for rating by product — values between 1–5?
- [ ] COUNTIFS for high-value reviews (HelpRatio ≥ 0.75) — total = 15,968?
- [ ] Cell references are dynamic (e.g., `=COUNTIF($A$2:$A$50001, A2)` not hardcoded range)?

---

### 2. Data Accuracy (25 points)

**What we're assessing:** Do your calculated KPIs match the verified expected values?

| Score | Criteria |
|---|---|
| **23–25** (Full) | ✅ All KPIs match verified outputs within rounding error (<0.5% variance). Average rating = 3.0. High-value count = 15,968. Product ranking correct. |
| **17–22** (Partial) | ⚠️ KPIs within 5% of expected values. 1–2 calculations off (e.g., average rating calculated as 3.05 instead of 3.0). Ranking mostly correct but 1–2 products out of order. |
| **<17** (Incomplete) | ❌ KPIs significantly off (>5% variance) OR multiple calculations incorrect OR major ranking errors. |

**Specific checks:**
- [ ] Average rating = 3.0 ± 0.05?
- [ ] High-value review count = 15,968 ± 500?
- [ ] Product B006MONQMC ranked in top 3?
- [ ] HelpRatio values all between 0–1?

---

### 3. Dashboard Design (20 points)

**What we're assessing:** Is your dashboard professional, clear, and easy to navigate?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Professional layout with clear visual hierarchy. Headers bold and centered. Consistent formatting (fonts, colors, alignment). Easy to read and understand at a glance. Appropriate use of whitespace. |
| **14–17** (Partial) | ⚠️ Readable but basic layout. Some formatting inconsistencies (e.g., mixed fonts or alignment). Dashboard structure is logical but not polished. Minor alignment or spacing issues. |
| **<14** (Incomplete) | ❌ Cluttered or hard to read layout. Inconsistent formatting. Unclear structure makes it difficult to find information. |

**Specific checks:**
- [ ] Title/header clearly identifies the analysis (Customer Satisfaction Intelligence)?
- [ ] KPI cards are prominent and easy to read (large font, clear values)?
- [ ] Charts have titles and axis labels?
- [ ] Column headers are bold and readable?
- [ ] No misaligned text or broken formatting?

---

### 4. Pivot Table Quality (15 points)

**What we're assessing:** Does your pivot table correctly structure the data and answer Q5?

| Score | Criteria |
|---|---|
| **14–15** (Full) | ✅ Pivot table correctly groups by star rating (1–5). Values show count and average HelpRatio. Expected output matches: 10,000 reviews per rating, HelpRatio ranges 0.35–0.45. Pivot is easy to read and formatted well. |
| **11–13** (Partial) | ⚠️ Pivot table present and mostly correct structure. 1–2 calculation errors in the pivot values. Formatting acceptable but basic. Minor issues with layout. |
| **<11** (Incomplete) | ❌ Pivot table missing OR incorrect structure (e.g., wrong rows/columns) OR significant calculation errors in pivot values. |

**Specific checks:**
- [ ] Rows: 5 star rating groups (1–5)?
- [ ] Columns: Count of reviews, Average HelpRatio?
- [ ] Values correct: 10,000 per rating?
- [ ] HelpRatio values between 0.30–0.50?

---

### 5. Documentation & Clarity (15 points)

**What we're assessing:** Can someone else (or a grader) understand your analysis? Are labels clear?

| Score | Criteria |
|---|---|
| **14–15** (Full) | ✅ Clear sheet names (e.g., "Summary KPIs", "Analysis", "Pivot Results"). Column headers self-explanatory. Key findings documented or summarized. Formula comments where needed (e.g., above COUNTIFS explaining the logic). Easy for someone else to follow your work. |
| **11–13** (Partial) | ⚠️ Most sheets labeled; some labels unclear. Column headers present but not fully descriptive. Limited documentation of findings. Minor confusion in following the analysis. |
| **<11** (Incomplete) | ❌ Missing labels on key sheets. Column headers vague or missing. No documentation of findings. Hard to follow the analysis logic. |

**Specific checks:**
- [ ] Sheet names: clear (Analysis, Summary, Pivot, Trend)?
- [ ] Column headers: describe what the column contains (e.g., "Avg Rating", "Product ID")?
- [ ] A summary row or text explaining top findings?
- [ ] Formulas are readable (not obscured by hard-to-read cell references)?

---

## Scoring Summary

| Dimension | Weight | Your Score | Weighted Score |
|---|---|---|---|
| Formula Accuracy | 25% | __/25 | __/25 |
| Data Accuracy | 25% | __/25 | __/25 |
| Dashboard Design | 20% | __/20 | __/20 |
| Pivot Table Quality | 15% | __/15 | __/15 |
| Documentation | 15% | __/15 | __/15 |
| **TOTAL** | 100% | | **__/100** |

---

## Feedback Template

**Strengths:**
- [What did they do well?]

**Areas for Improvement:**
- [What could be clearer or more accurate?]

**Grade:** __/100 → Letter Grade: ___

---

## Common Mistakes to Avoid

1. **Hardcoded values instead of formulas:** Every COUNTIF, AVERAGEIF, COUNTIFS should be a formula, not a typed number.
2. **Wrong cell range:** Ensure COUNTIF ranges include all data (e.g., `A2:A50001` for 50k rows, not `A2:A1000`).
3. **Missing HelpRatio filter:** Q3 asks for "high-value reviews" — make sure your COUNTIFS includes the HelpRatio ≥ 0.75 condition.
4. **Pivot table layout:** Rows should be star rating (1–5), not products. Values should be count and average HelpRatio.
5. **Unclear labels:** "Sheet1" or "Data" are not descriptive. Use names like "Analysis", "Pivot Results", "Summary KPIs".

---

## Bonus (Optional, +5 points max)

- **Trend visualization:** A chart showing how HelpRatio changes year-over-year (+3 points)
- **Advanced pivot:** Multiple pivot tables exploring different groupings (e.g., by year or reviewer type) (+3 points)
- **Executive summary:** A 1-paragraph summary of top 3 findings written at the top of the dashboard (+2 points)

(Bonus is capped at +5 total, so your final score maxes at 105. This gets reported as 100 if you don't have other deductions.)

---

## Grade Scale

| Score | Grade | Interpretation |
|---|---|---|
| 90–100 | A | Excellent — fully meets all criteria, professional quality |
| 80–89 | B | Good — meets most criteria, minor issues |
| 70–79 | C | Acceptable — meets core criteria, notable issues |
| 60–69 | D | Below standard — multiple criteria not met |
| <60 | F | Incomplete or missing substantial work |
