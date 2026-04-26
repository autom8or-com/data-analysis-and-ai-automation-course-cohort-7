# Group 2 — Product Category Performance Analysis — Grading Rubric

## Overview
This rubric assesses Group 2's Superstore project across 5 dimensions. Each dimension has a full score (90–100%), partial credit range (70–89%), and incomplete (<70%). Total weight = 100%.

**Total Points:** 100 | **Passing:** 70 | **Good:** 80 | **Excellent:** 90+

---

## Rubric Dimensions

### 1. Formulas Accurate (25 points)

**What we're assessing:** Do your SUMIF, SUMIFS, AVERAGEIF, and COUNTIF formulas produce correct values?

| Score | Criteria |
|---|---|
| **23–25** (Full) | ✅ All formulas working and producing verified outputs. Furniture: £742k sales, £18.5k profit; Office Supplies: £719k sales, £122.5k profit; Technology: £836k sales, £145.5k profit. SUMIFS correctly filters by category and segment. AVERAGEIF calculates profit per transaction. Cell references proper (no hardcoding). |
| **17–22** (Partial) | ⚠️ Most formulas correct (85–95% accuracy). 1–2 minor calculation errors. Some category/segment values off by <5%. Reference issues present but minor. Deductions for missing COUNTIF or incomplete formula set. |
| **<17** (Incomplete) | ❌ Multiple formula errors OR hardcoded values instead of formulas OR incorrect SUMIFS logic (missing filter condition). Expected KPIs significantly off. |

**Specific checks:**
- [ ] SUMIF for Furniture sales = £742,000?
- [ ] SUMIF for Furniture profit = £18,451?
- [ ] SUMIFS for Consumer segment profit = £134,119?
- [ ] COUNTIF for unprofitable transactions (~1000+)?
- [ ] AVERAGEIF for average profit per transaction by category?

---

### 2. Category Analysis (20 points)

**What we're assessing:** Do you correctly identify which categories are profitable vs. unprofitable?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Clearly identifies Furniture as the profit problem (only £18.5k profit on £742k sales = 2.5% margin). Shows all three categories with accurate metrics. Recognizes Office Supplies and Technology are healthy (17–17.4% margins). Analysis is complete and correct. |
| **14–17** (Partial) | ⚠️ Identifies Furniture as lower-profit but doesn't emphasize the crisis. Some category metrics correct; 1–2 margin calculations off. Analysis present but incomplete. |
| **<14** (Incomplete) | ❌ Fails to identify Furniture problem OR category analysis missing/incorrect OR major calculation errors. |

**Specific checks:**
- [ ] Furniture identified as unprofitable (2.5% vs. 17% for others)?
- [ ] All three categories analyzed?
- [ ] Profit margin % calculated and compared?

---

### 3. Segment Breakdown (15 points)

**What we're assessing:** Do you correctly segment profit by Customer Segment and identify which drives most profit?

| Score | Criteria |
|---|---|
| **14–15** (Full) | ✅ Correctly segments profit: Consumer (£134k, 47%), Corporate (£92k, 32%), Home Office (£60k, 21%). Shows Consumer drives most profit. All calculations verified. |
| **11–13** (Partial) | ⚠️ Segments identified; 1–2 calculations off by <5%. Consumer recognized as top segment but not emphasized. Basic segment analysis present. |
| **<11** (Incomplete) | ❌ Segment analysis missing or significantly incorrect. |

**Specific checks:**
- [ ] Consumer profit = £134,119?
- [ ] Corporate profit = £91,979?
- [ ] Home Office profit = £60,299?
- [ ] Percentages calculated?

---

### 4. Dashboard Design (20 points)

**What we're assessing:** Is your dashboard professional, clear, and highlighting the profit problem?

| Score | Criteria |
|---|---|
| **18–20** (Full) | ✅ Professional layout. KPI cards prominent. Category comparison chart clearly shows Furniture's low profit. Regional analysis shows South as negative. Easy to spot the problems. Consistent formatting. |
| **14–17** (Partial) | ⚠️ Good layout but not polished. Charts present; Furniture problem visible but not emphasized. Minor formatting issues. |
| **<14** (Incomplete) | ❌ Cluttered layout. Profit problem hard to see. Poor formatting or unclear structure. |

**Specific checks:**
- [ ] KPI cards show Total Sales, Total Profit, Profit Margin %?
- [ ] Chart clearly compares profit by category?
- [ ] South region shown as unprofitable (negative profit)?
- [ ] Professional formatting (bold headers, aligned columns)?

---

### 5. Regional Insight (10 points)

**What we're assessing:** Do you correctly analyze regional profitability?

| Score | Criteria |
|---|---|
| **9–10** (Full) | ✅ Correctly identifies South region as unprofitable (negative total profit or lowest profit). Regional ranking accurate (West > East > Central > South). Highlights regional disparity. |
| **7–8** (Partial) | ⚠️ Regional data present; ranking mostly correct. South identified as problematic but not emphasized. Analysis basic. |
| **<7** (Incomplete) | ❌ Regional analysis missing or incorrect. |

**Specific checks:**
- [ ] West region profit calculated (~£268k)?
- [ ] South region profit calculated (negative or lowest)?
- [ ] Regional comparison chart present?

---

## Scoring Summary

| Dimension | Weight | Your Score | Weighted |
|---|---|---|---|
| Formulas Accurate | 25% | __/25 | __/25 |
| Category Analysis | 20% | __/20 | __/20 |
| Segment Breakdown | 15% | __/15 | __/15 |
| Dashboard Design | 20% | __/20 | __/20 |
| Regional Insight | 10% | __/10 | __/10 |
| **TOTAL** | 100% | | **__/100** |

---

## Common Mistakes

1. **Forgetting to calculate revenue:** Revenue = Quantity × (Unit Price). Ensure you have this column before SUMIF.
2. **SUMIFS syntax:** `=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2)` — order matters.
3. **Hardcoded profit margin:** Calculate Profit Margin % as a formula, not a typed value.
4. **Missing negative profit:** South region has negative total profit. Include this in your analysis — it's the insight.
5. **Unclear chart labels:** Axis labels should say "Category" and "Profit (£)", not just "X" and "Y".

---

## Bonus (Optional, +5 points max)

- **Drill-down analysis:** Sub-category breakdown within Furniture showing which furniture items are unprofitable (+3 points)
- **Discount analysis:** Examine whether discounts are driving Furniture's low profit (+3 points)
- **Executive summary:** 1-paragraph finding at top of dashboard (+2 points)

---

## Grade Scale

| Score | Grade | Interpretation |
|---|---|---|
| 90–100 | A | Excellent — identifies and highlights Furniture problem; professional dashboard |
| 80–89 | B | Good — correct analysis; dashboard readable |
| 70–79 | C | Acceptable — analysis mostly correct; minor issues |
| 60–69 | D | Below standard — multiple criteria not met |
| <60 | F | Incomplete or missing substantial work |
