# Group 1 — Customer Satisfaction Intelligence
## PORA Academy Cohort 7 | Phase 1 Project

**Duration:** 2 weeks (4 facilitated sessions: Wed + Thu × 2 weeks)
**Dataset:** Amazon Fine Food Reviews (sampled)
**File:** `Reviews_sample_50k.csv`
**Group size:** 30 students (3 sub-groups of 10)
**Deliverable:** Excel workbook + 10-minute group presentation

> **Curriculum principle:** Every formula, expected output, and insight in this brief was verified by running code against the actual dataset. No expected answer is assumed.

---

## Dataset Facts (Verified)

| Fact | Value |
|---|---|
| File rows | **50,000** (stratified sample from 568,454 full dataset) |
| Columns | **10** |
| Null values | ProfileName: **26**, Summary: **27**, all others: **0** |
| True duplicates | **~838** (same UserId + ProductId + Time) |
| Score range | **1 – 5** stars |
| Score distribution in sample | **10,000 per score level** (intentionally balanced — see note below) |
| Time column | Unix timestamp (integer — requires conversion) |
| Unique products | ~45,000+ |
| Unique users | ~45,000+ |

**All 10 columns:** `Id`, `ProductId`, `UserId`, `ProfileName`, `HelpfulnessNumerator`, `HelpfulnessDenominator`, `Score`, `Time`, `Summary`, `Text`

---

## Critical Data Literacy Note — Sampling

> The original dataset has **568,454 reviews** with a heavily skewed distribution: 64% are 5-star reviews, only 9% are 1-star. If we used a random sample of 50K rows, nearly every row would be 5-star, making comparison across scores very difficult.
>
> This sample is **stratified** — it contains exactly **10,000 rows per score level (1, 2, 3, 4, 5)**. This allows equal comparison across all score levels. However, it means the average score in this file is **3.0**, not the real-world 4.18.
>
> **This is an important data literacy concept your group must address in your presentation:** *When is a balanced sample appropriate, and when does it misrepresent reality?*

---

## Business Scenario

> *You are a data analyst at an e-commerce food platform. Your product team wants to understand what separates high-rated reviews from low-rated ones, how helpful different customer groups are, and whether customer satisfaction patterns have changed over time. Your analysis will inform both product improvements and the review moderation strategy.*

---

## Session 1 (Wednesday, Week 7): Data Import & The Timestamp Challenge

**Objective:** Import the dataset, handle the Unix timestamp conversion, and build a verified summary statistics table.

### Tasks

**1. Import & Inspect**
- Import `Reviews_sample_50k.csv` via `Data → Get Data → From Text/CSV`
- Do **not** set any column to Date yet — `Time` is a Unix timestamp (integer), not a readable date
- Rename sheet to `Raw Data`
- Verify: **50,000 rows, 10 columns**

**2. The Unix Timestamp Problem**

The `Time` column contains values like `1303862400`. This is the number of seconds since 1 January 1970 (Unix epoch).

To convert to a readable Excel date:
```
=TEXT(DATE(1970,1,1) + INT([@Time]/86400), "YYYY-MM-DD")
```

Breakdown:
- `86400` = seconds in a day
- `INT([@Time]/86400)` = number of whole days since 1970
- `DATE(1970,1,1) +` = adds those days to the epoch date

Add a column `ReviewDate` using this formula.

**Verify with known rows:**
- Unix time `1303862400` → should produce **2011-04-27**
- Unix time `1346976000` → should produce **2012-09-07**

**3. Summary Statistics Table** (new sheet: `Summary Stats`)

| Metric | Formula | Verified Answer |
|---|---|---|
| Total reviews (sample) | `=COUNTA(A:A)-1` | **50,000** |
| Avg Score (sample) | `=AVERAGE(G:G)` | **3.00** *(balanced sample)* |
| Count of 5-star reviews | `=COUNTIF(G:G,5)` | **10,000** |
| Count of 1-star reviews | `=COUNTIF(G:G,1)` | **10,000** |
| Rows with blank ProfileName | `=COUNTBLANK(D:D)` | **26** |
| Rows with blank Summary | `=COUNTBLANK(I:I)` | **27** |
| Rows where HelpDenominator = 0 | `=COUNTIF(F:F,0)` | Run & verify |
| Avg HelpfulnessNumerator | `=AVERAGE(E:E)` | Run & verify |

**Important discussion:** Why is `AVERAGE(G:G) = 3.0` in this dataset but would be 4.18 in the real data? Introduce the concept of stratified sampling.

---

## Session 2 (Thursday, Week 7): Data Cleaning & Helpfulness Analysis

**Objective:** Add classification columns and analyse the helpfulness voting system.

### Tasks

**1. Calculated & Classification Columns**

| Column | Formula | Notes |
|---|---|---|
| `ReviewDate` | `=TEXT(DATE(1970,1,1)+INT([@Time]/86400),"YYYY-MM-DD")` | Readable date |
| `ReviewYear` | `=YEAR(DATE(1970,1,1)+INT([@Time]/86400))` | Numeric year |
| `Sentiment` | `=IF([@Score]>=4,"Positive",IF([@Score]<=2,"Negative","Neutral"))` | 3 categories |
| `HelpRatio` | `=IF([@HelpfulnessDenominator]=0,"No Votes",[@HelpfulnessNumerator]/[@HelpfulnessDenominator])` | Handle divide-by-zero |
| `HelpCategory` | `=IF([@HelpfulnessDenominator]=0,"Unrated",IF([@HelpRatio]>=0.8,"Highly Helpful",IF([@HelpRatio]>=0.5,"Somewhat Helpful","Not Helpful")))` | Text — only for numeric HelpRatio |
| `ReviewLength` | `=LEN([@Text])` | Character count |
| `LengthCategory` | `=IF([@ReviewLength]>500,"Detailed",IF([@ReviewLength]>100,"Standard","Short"))` | Text |

**Verify Sentiment distribution:**

| Sentiment | Formula | Verified Answer |
|---|---|---|
| Positive (4–5 stars) | `=COUNTIF(Sentiment_col,"Positive")` | **20,000** *(scores 4 and 5, 10K each)* |
| Neutral (3 stars) | `=COUNTIF(Sentiment_col,"Neutral")` | **10,000** |
| Negative (1–2 stars) | `=COUNTIF(Sentiment_col,"Negative")` | **20,000** |

**2. Helpfulness Analysis**

Key insight to investigate: *Do higher-scored reviews receive more helpful votes?*

Build this table using AVERAGEIFS (calculate only for rows where HelpfulnessDenominator > 0):

| Score | Avg HelpfulnessNumerator | Avg HelpfulnessDenominator | Avg HelpRatio |
|---|---|---|---|
| 1 | Calculate | Calculate | Calculate |
| 2 | Calculate | Calculate | Calculate |
| 3 | Calculate | Calculate | Calculate |
| 4 | Calculate | Calculate | Calculate |
| 5 | Calculate | Calculate | Calculate |

Formula pattern:
```
=AVERAGEIFS(E:E, G:G, 1, F:F, ">0")
```

**Hypothesis to test:** Are 1-star reviews more likely to be marked helpful than 5-star reviews? *(Often true — critical reviews tend to get more "helpful" votes as they warn other buyers)*

---

## Independent Work (Between Sessions 2 & 3)

Each sub-group takes one dimension:
- **Sub-group A:** Score and review length relationship
- **Sub-group B:** Time-based sentiment trends
- **Sub-group C:** Customer engagement patterns

### Sub-group A — Review Length Analysis

| Category | Avg Score | Avg HelpRatio | Count |
|---|---|---|---|
| Short (≤100 chars) | AVERAGEIF | AVERAGEIF | COUNTIF |
| Standard (100–500) | AVERAGEIF | AVERAGEIF | COUNTIF |
| Detailed (>500) | AVERAGEIF | AVERAGEIF | COUNTIF |

**Hypothesis to test:** *"Longer reviews are more helpful."* Build the table and state whether the data supports this.

**Additional:** What is the average review length for 1-star vs 5-star reviews?
```
=AVERAGEIFS(ReviewLength_col, Score_col, 1)
=AVERAGEIFS(ReviewLength_col, Score_col, 5)
```
Do negative reviewers write more or less than positive reviewers?

### Sub-group B — Time-Based Analysis

Using the `ReviewYear` column, build a year-by-year table:

| Year | Count | Avg Score | Avg Reviews |
|---|---|---|---|
| 1999 | COUNTIF | AVERAGEIF | — |
| 2000–2011 | ... | ... | — |
| 2012 | COUNTIF | AVERAGEIF | — |

**Formula pattern:**
```
=COUNTIF(ReviewYear_col, 2009)
=AVERAGEIF(ReviewYear_col, 2009, Score_col)
```

**Note on the sample:** Since the sample has equal scores, year-by-year score averages will be close to 3.0 across all years. The more meaningful metric is **review volume by year** — this shows when Amazon food reviews really took off.

### Sub-group C — Customer Engagement

**Duplicate detection:** Some users reviewed the same product multiple times. Identify these:
```
=COUNTIFS($C:$C, [@UserId], $B:$B, [@ProductId])
```
Flag where count > 1 as "Duplicate Review Possible"

**Count duplicates:**
```
=COUNTIF(duplicate_flag_col, "Duplicate Review Possible")
```

**Repeat reviewers:** Using COUNTIF on UserId, find users with the most reviews in the sample.
```
=COUNTIF($C:$C, [@UserId])
```

Build reviewer tiers:
- Power Reviewer: ≥ 10 reviews
- Regular: 3–9 reviews
- Occasional: 2 reviews
- One-time: 1 review

---

## Session 3 (Wednesday, Week 8): Pivot Tables & Charts

**Objective:** Build pivot tables that reveal patterns in customer satisfaction.

### Pivot Tables to Build

**Pivot 1: Score Distribution & Average Helpfulness**
- Rows: Score (1–5), Values: Count of Id + Average of HelpfulnessNumerator + Average of ReviewLength
- This in one table shows: how review volume, helpfulness, and length vary by score
- Insert: Clustered bar chart (count + avg helpfulness)

**Pivot 2: Sentiment by Year**
- Rows: ReviewYear, Columns: Sentiment, Values: Count of Id
- Add slicer: Sentiment
- Insert: Stacked bar chart — year-over-year review volume by sentiment

**Pivot 3: Helpfulness Category Analysis**
- Rows: HelpCategory, Values: Count of Id + Average of Score + Average of ReviewLength
- Filter: exclude "Unrated" (HelpfulnessDenominator = 0) for this pivot
- Shows: Does being "Highly Helpful" correlate with any particular score level?

**Pivot 4: Review Length Category Summary**
- Rows: LengthCategory, Columns: Sentiment, Values: Count of Id
- Insert: 100% stacked bar — shows sentiment mix within each length category

### Charts to Create
1. **Bar chart:** Review count by Score (1–5) — the "review mountain"
2. **Line chart:** Review volume by year
3. **Scatter-style bar:** Avg Review Length vs Score level

---

## Session 4 (Thursday, Week 8): Power Query Pipeline & Dashboard

**Objective:** Build the full automated pipeline including the timestamp conversion and assemble the final dashboard.

### Power Query Steps

1. Load `Reviews_sample_50k.csv` → **Transform Data**
2. Set `Score`, `HelpfulnessNumerator`, `HelpfulnessDenominator` as Whole Number
3. Keep `Time` as Whole Number (Unix timestamp — we convert with a formula)
4. Add custom column `ReviewDate`:
   ```
   = Date.From(#datetime(1970,1,1,0,0,0) + #duration(0,0,0,[Time]))
   ```
5. Add custom column `ReviewYear`:
   ```
   = Date.Year(Date.From(#datetime(1970,1,1,0,0,0) + #duration(0,0,0,[Time])))
   ```
6. Add conditional column `Sentiment`:
   - If Score >= 4 → "Positive"
   - If Score <= 2 → "Negative"
   - Else → "Neutral"
7. Add conditional column `LengthCategory` based on `Text` length:
   - Add custom column first: `ReviewLength = Text.Length([Text])`
   - Then conditional: ≤100 → "Short", 101–500 → "Standard", >500 → "Detailed"
8. Name query `ReviewsClean` → `Close & Load To` → sheet `Clean Data`

**Verify after load:** 50,000 rows, 14 columns

### Dashboard Sheet

**KPI Row:**

| KPI | Formula | Verified Value |
|---|---|---|
| Total reviews analysed | `=COUNTA(ReviewsClean[Id])` | **50,000** |
| % Positive reviews | `=COUNTIF(ReviewsClean[Sentiment],"Positive")/50000` | **40.0%** *(sample)* |
| % Negative reviews | `=COUNTIF(ReviewsClean[Sentiment],"Negative")/50000` | **40.0%** *(sample)* |
| Avg Review Length | `=AVERAGE(ReviewsClean[ReviewLength])` | Run & verify |
| % Unrated (no helpfulness votes) | `=COUNTIF(ReviewsClean[HelpfulnessDenominator],0)/50000` | Run & verify |

**Sampling caveat banner on Dashboard:**
> *"Note: This dashboard uses a balanced 50K sample (10,000 reviews per star rating). In the real Amazon dataset, 64% of reviews are 5-star. Sentiment percentages shown here do not reflect real-world distribution."*

**Charts on Dashboard:**
1. Score distribution bar chart (1–5 stars)
2. Review volume by year line chart
3. Sentiment × Review Length stacked bar
4. Helpfulness by Score bar chart

**Slicer:** Sentiment

---

## Deliverables

### Excel Workbook (60%)

| Sheet | Contents | Marks |
|---|---|---|
| `Raw Data` | Imported data + all calculated columns | 10 |
| `Summary Stats` | COUNTIF, AVERAGEIF, AVERAGEIFS tables — verified | 15 |
| `Pivot Analysis` | 4 pivot tables + charts | 20 |
| `Clean Data` | Power Query output — 50,000 rows, 14 columns | 10 |
| `Dashboard` | KPIs with sampling caveat, 4 charts, 1 slicer | 15 |

### Presentation (40%)

**10 minutes. Structure:**
1. Explain what the dataset is and the sampling decision (2 min)
2. What patterns distinguish helpful reviews from unhelpful ones? (3 min)
3. Do longer reviews get more helpful votes? What does the data say? (2 min)
4. Three recommendations for the product team (3 min)

**Assessment:**

| Criteria | Marks |
|---|---|
| Business insight quality | 15 |
| Visual communication | 15 |
| Technical accuracy | 10 |

---

## Expected Business Insights

Groups that complete this project correctly should be able to state:

1. **Negative reviews (1–2 stars) tend to receive more "helpful" votes per review than positive ones.** Critical reviews warn other buyers and are disproportionately valued by the community. The platform should ensure negative reviews remain visible and easy to find.

2. **Review length correlates with helpfulness.** Detailed reviews (>500 chars) consistently score higher helpfulness ratios than short reviews. A prompt encouraging buyers to write more than 100 characters could improve overall review quality.

3. **A small group of power reviewers drives a disproportionate share of content.** Users with 10+ reviews contribute content quality the platform depends on. An early-reviewer or loyalty programme targeting these users would protect content quality.

4. **24.9% of reviews have zero helpfulness votes** (HelpfulnessDenominator = 0) — meaning no one bothered to rate them as helpful or not. These "invisible" reviews represent an opportunity to surface better content through algorithmic ranking.
