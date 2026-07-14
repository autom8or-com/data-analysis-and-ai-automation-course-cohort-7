# Week 8 — Visualisation & Putting It Together: Wednesday Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-08-wed-demo.ipynb`
- [ ] Student exercise link ready to share: `week-08-wed-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek access confirmed for all students (Week 4+ requirement)

---

## Learning Objectives

By the end of this session, students will be able to:
1. Create bar charts, line charts, and histograms with matplotlib
2. Format charts (title, labels, figsize, colours)
3. Use seaborn for cleaner charts
4. Save charts to file

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, load Olist data via the standard Drive-mount snippet |
| 0:10–0:40 | matplotlib Foundations | Line chart (monthly orders 2017) + bar chart (order status distribution) |
| 0:40–1:10 | seaborn | `sns.countplot` for review scores, matplotlib pie chart for payment methods |
| 1:10–1:50 | Group Exercise | Each group builds 3 charts: monthly volume, top-10 states, review scores |
| 1:50–2:00 | Debrief & preview | Share expected chart values, preview Thursday's Streamlit dashboard |

---

## Key Concepts

### matplotlib Foundations
Build line and bar charts directly from the Olist `orders` DataFrame using `plt.plot`/`plt.bar`, with titles, axis labels, a `figsize`, and rotated x-tick labels for readability.

Expected outputs:
- November 2017 is the visual peak month at 7,544 orders (Black Friday) — should stand out clearly on the line chart
- Order status bar chart: `delivered` dominates all other statuses by a wide margin

Common mistake to watch for: forgetting `plt.figure(figsize=(...))` before plotting — charts default to a small, hard-to-read size when several are drawn in the same notebook without resetting the figure.

### seaborn Charts
`sns.countplot` renders the review-score distribution in one line; a matplotlib pie chart shows the payment-type split.

Expected outputs:
- Review scores: 5-star = 57,328 (dominant), 1-star = 11,424 (second most common)
- Payment split: credit_card 73.9%, boleto 19.0%, voucher 5.6%, debit_card 1.5%

Common mistake to watch for: calling `plt.show()` before `plt.tight_layout()` clips axis labels — always call `tight_layout()` first.

---

## Group Exercise

Each group builds 3 charts using verified data:
- Chart 1: Monthly order volume for 2017 (line chart) — peak should show November 2017 = 7,544 orders
- Chart 2: Top 10 states by total orders (horizontal bar chart) — SP should be far ahead at 41,746
- Chart 3: Review score distribution (bar chart) — scores 1-5, expected counts [11424, 3151, 8179, 19142, 57328]

**Expected outputs**: November 2017 peak = 7,544 orders; SP state total = 41,746 orders; review score counts [11424, 3151, 8179, 19142, 57328].

---
