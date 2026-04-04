# Week 04 — Thursday: Charts — Visualise Your Data
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** 04 of 6
**Session:** Thursday
**Topic:** Charts — Visualise Your Data

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-04-thu-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-04-thu-exercises.xlsx`
- [ ] Weekly assignment distributed or screen-shared at end of session
- [ ] Projector / screen sharing ready

---

## Learning Objectives

By the end of this session, students will be able to:

1. Create column, bar, and pie charts from pivot table summary data
2. Add and format chart elements (title, axis labels, data labels, legend)
3. Create a line chart showing revenue trend over time (monthly)
4. Choose the right chart type for different business questions

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00 – 0:10 | Recap Wednesday: Pivot tables (Rows, Columns, Values, Filters) | Quick-fire Q&A |
| 0:10 – 0:40 | Part 1 — Column & Bar Charts: Revenue by Country | Build from pivot summary |
| 0:40 – 1:05 | Part 2 — Pie Chart: Revenue Share by Country | When to use (and not use) pie |
| 1:05 – 1:35 | Part 3 — Line Chart: Monthly Revenue Trend | Time series visualisation |
| 1:35 – 2:00 | Group Exercise + debrief + assignment intro | |

---

## Concepts & Verified Outputs

### Setup: Summary Tables for Charts

Charts are built from summary data, not 541,909 raw rows. Students should either:
- Use the pivot tables from Wednesday's session, OR
- Build quick summary tables using SUMIFS (recap from Week 3)

The demo workbook includes pre-built summary tables as the chart source.

---

### Concept 1 — Column Chart: Revenue by Top 5 Countries

**Source data (full dataset verified):**

| Country | Revenue |
|---|---|
| United Kingdom | £8,187,806.36 |
| Netherlands | £284,661.54 |
| EIRE | £263,276.82 |
| Germany | £221,698.21 |
| France | £197,403.90 |

**Steps (demonstrate live):**
1. Select the summary table (2 columns × 5 rows + headers)
2. `Insert → Chart → Clustered Column`
3. Add chart title: "Revenue by Top 5 Countries"
4. Add data labels (Format Data Labels → Value)
5. Format Y-axis: currency `£#,##0`
6. Remove gridlines for cleaner look

**Teaching points:**
- Column charts compare categories — one bar per category
- The UK dominates (£8.2M vs next highest £285K) — this tells a story about market concentration
- Consider whether the chart needs the UK at all, or if a "Top 5 excluding UK" view is more useful

---

### Concept 2 — Bar Chart: Transaction Count by Country

**Source data (full dataset verified):**

| Country | Transactions |
|---|---|
| United Kingdom | 495,478 |
| Germany | 9,495 |
| France | 8,557 |
| EIRE | 8,196 |
| Spain | 2,533 |

**Steps:**
1. Select the transaction count summary
2. `Insert → Chart → Clustered Bar` (horizontal)
3. Add chart title: "Transaction Count by Top 5 Countries"
4. Format X-axis: number `#,##0`

**Teaching point:** Bar charts (horizontal) work better when category labels are long — country names read more easily on the left axis.

---

### Concept 3 — Pie Chart: Revenue Share

**Source data (full dataset verified — top 5 + "Other"):**

| Country | Revenue | Share |
|---|---|---|
| United Kingdom | £8,187,806.36 | 84.0% |
| Netherlands | £284,661.54 | 2.9% |
| EIRE | £263,276.82 | 2.7% |
| Germany | £221,698.21 | 2.3% |
| France | £197,403.90 | 2.0% |
| Other (33 countries) | £592,942.10 | 6.1% |

**Steps:**
1. Select the summary table with "Other" row
2. `Insert → Chart → Pie`
3. Add data labels: show Category Name + Percentage
4. Chart title: "Revenue Share by Country"

**Teaching points:**
- Pie charts work ONLY when: (a) values sum to a meaningful whole, (b) there are ≤ 6 segments
- The UK at 84% makes the other slices tiny — this is actually a valid insight (market concentration)
- **When NOT to use pie:** more than 6 categories, comparing values across time, negative values

---

### Concept 4 — Line Chart: Monthly Revenue Trend

**Source data (full dataset verified):**

| Month | Revenue |
|---|---|
| Dec 2010 | £748,957.02 |
| Jan 2011 | £560,000.26 |
| Feb 2011 | £498,062.65 |
| Mar 2011 | £683,267.08 |
| Apr 2011 | £493,207.12 |
| May 2011 | £723,333.51 |
| Jun 2011 | £691,123.12 |
| Jul 2011 | £681,300.11 |
| Aug 2011 | £682,680.51 |
| Sep 2011 | £1,019,687.62 |
| Oct 2011 | £1,070,704.67 |
| Nov 2011 | £1,461,756.25 |
| Dec 2011 | £433,668.01 |

**Steps:**
1. Select month + revenue columns
2. `Insert → Chart → Line`
3. Add chart title: "Monthly Revenue Trend (Dec 2010 – Dec 2011)"
4. Format Y-axis: currency `£#,##0`
5. Add data labels for peak month (Nov 2011)

**Teaching points:**
- Line charts show trends over time — the X-axis must be sequential
- Clear seasonal pattern: revenue climbs Sep–Nov (pre-Christmas rush), drops in Dec 2011 (incomplete month — data ends 9 Dec 2011)
- Nov 2011 peak (£1,461,756) is nearly 3× the Feb 2011 trough (£498,063)

---

### Chart Type Selection Guide

| Question type | Best chart | Why |
|---|---|---|
| Compare categories | Column / Bar | Easy to compare bar heights |
| Show composition (parts of whole) | Pie (≤6 slices) | Shows proportions at a glance |
| Show trend over time | Line | Connects sequential data points |
| Compare two measures | Combo (column + line) | Two Y-axes for different scales |

---

## Group Exercise

**Questions (25 min):**

1. From your pivot table (or SUMIFS summary), create a **column chart** showing Revenue by Country for all countries in your sample. Add a chart title and data labels.

2. Create a **pie chart** showing the revenue share by country. Add percentage labels. Which country dominates? What business insight does this give?
   *(Full dataset: UK = 84% of revenue — extreme market concentration)*

3. Build a summary table of monthly revenue using SUMIFS with date criteria, then create a **line chart**. Can you spot the seasonal trend?
   *(Full dataset: revenue peaks in Nov 2011 at £1,461,756.25)*

4. Create a **bar chart** (horizontal) comparing Sales revenue vs Cancellation revenue for the top 3 countries. What does the cancellation pattern tell you?
   *(Full dataset: UK cancellations = -£815,291.60 — about 9% of gross sales)*

**Debrief points:**
- Chart choice matters — a pie chart with 38 countries would be unreadable
- The UK dominance is a real business insight: this retailer is heavily UK-dependent
- Nov peak → Christmas ordering; Dec drop → incomplete data, not a real decline
- Formatting makes charts professional: titles, labels, clean axes

---

## Weekly Assignment

*Set at the end of this session — students complete before next Wednesday.*

1. Create a pivot table showing **Revenue by Country and OrderType** (Country in Rows, OrderType in Columns, Revenue in Values). Take a screenshot of the result.

2. From the pivot table, create a **clustered column chart** comparing Sale and Cancellation revenue for the top 5 countries. Add a chart title, axis labels, and data labels. Format revenue as currency.

3. Using SUMIFS, build a monthly revenue summary table. Create a **line chart** showing the monthly trend. In a text cell below the chart, write one sentence describing the trend you observe.

4. Create a **pie chart** showing the percentage of transactions (not revenue) by country. Add percentage labels. In a text cell, explain whether pie is the right chart type for this data and why.

---

## Files

| File | Purpose |
|---|---|
| `lecture-materials/week-04-thu-demo.xlsx` | Instructor demo — summary tables and chart data (charts must be created live) |
| `exercises/week-04-thu-exercises.xlsx` | Distributed to students — raw data + instructions, blank workspace |
| `solutions/week-04-thu-solutions.xlsx` | Instructor reference — completed summary tables and chart source data |

---

## Instructor Notes

- **Charts cannot be created programmatically:** The demo and solution workbooks contain the source summary tables but NOT the actual charts. You must **create all charts live** in class. The workbooks serve as your data reference.
- **Pivot → Chart shortcut:** After creating a pivot table, clicking `Insert → PivotChart` creates a chart directly tied to the pivot. This is faster but harder to format — show it as a bonus, not the primary method.
- **Dec 2011 gotcha:** The dataset ends on 9 Dec 2011, so December 2011 revenue (£433,668) looks like a sharp decline. It's actually incomplete data. **Always mention this** — it's a great lesson about data quality.
- **Total revenue = £9,747,747.93:** This includes cancellations (negative values). Gross sales revenue is £10,644,560.42. The difference (£896,812.49) is total cancellation value.
- **Pie chart rule of thumb:** Never more than 6 slices. If students have more countries in their sample, teach them to group small ones into "Other".
- **Sample limitations:** The 1,000-row sample has only 4 countries and no monthly variation (all rows are from a few invoices). The monthly line chart works much better on the full dataset — consider having a pre-built full-dataset chart to show.
- **Formatting checklist for charts:** Title (descriptive, not "Chart 1"), axis labels (with units), data labels (where space allows), legend (only if multiple series), no gridlines (unless comparing precise values).