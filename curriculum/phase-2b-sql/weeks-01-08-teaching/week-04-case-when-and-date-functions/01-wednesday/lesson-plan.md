# Week 4 — CASE WHEN & Date Functions: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-04-wed-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-04-wed-exercises.ipynb`
- [ ] Projector connected, Colab running
- [ ] DeepSeek access confirmed for all students — this is the first AI-assisted session

---

## Learning Objectives

By the end of this session, students will be able to:
1. Classify and group data using conditional SQL — write a `CASE WHEN` expression that maps raw column values into higher-level business categories.
2. Build business categories directly in SQL — bucket a continuous number (payment value) into named bands, then aggregate per band.
3. Use `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` to count a subset inside a single pass over the table, and turn that count into a correct percentage using `* 1.0`.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py` |
| 0:10–0:45 | CASE WHEN — status classification | Demo: `order_status` → `status_group`; discuss `ELSE` and branch order |
| 0:45–1:15 | CASE WHEN — payment value bands | Demo: bucket `payment_value` into Low/Mid/High/Premium; DeepSeek prompt-then-verify intro |
| 1:15–1:30 | Going deeper — conditional counting & integer-division trap | `SUM(CASE WHEN...)`, `* 1.0` fix |
| 1:30–1:45 | Mini-challenge + exercises | Students work `week-04-wed-exercises.ipynb` |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Thursday's date functions |

---

## Key Concepts

### CASE WHEN — classify order statuses into business categories

Use `CASE WHEN` to map raw `order_status` values into higher-level business groups (Completed / In Progress / Canceled / Other), then aggregate.

Expected outputs (verified against the Olist dataset):
| order_status | status_group | count |
|---|---|---|
| delivered | Completed | 96,478 |
| shipped | In Progress | 1,107 |
| canceled | Canceled | 625 |
| unavailable | Other | 609 |
| invoiced | In Progress | 314 |
| processing | In Progress | 301 |

Common mistake to watch for: omitting `ELSE` (unmatched rows silently become `NULL` and form an unnoticed bucket), comparing to `NULL` with `=` instead of `IS NULL`, and writing wide bands before narrow ones (the first true branch wins, so a wide band placed first swallows a narrower one).

### CASE WHEN — classify payment values into bands

Bucket `order_payments.payment_value` into Low (<R$50) / Mid (R$50–200) / High (R$200–500) / Premium (R$500+) bands and aggregate count + avg value per band. No expected output is documented in the curriculum for this query — treat it as an open teaching example, not a locked assertion. Note the grain: `order_payments` has 103,886 rows for 99,441 orders, so `COUNT(*)` here counts payment records, not orders.

Common mistake to watch for: the integer-division trap — `625 * 100 / 99441` returns `0` in SQLite because both operands are integers; `* 1.0` forces REAL division.

---

## Group Exercise

This week's group exercise runs at the end of the Thursday session, combining both days' material (CASE WHEN + date functions):

1. Classify customers into geographic regions using CASE WHEN (Southeast: SP, RJ, MG, ES; South: RS, SC, PR; Northeast: BA, CE, PE, MA, RN, PB, AL, SE, PI; Other: everything else).
2. How many orders were placed on weekends vs weekdays? (Hint: `strftime('%w', ...)` returns 0=Sunday, 6=Saturday.)
3. What is the average delivery time by customer state? Show the 5 fastest and 5 slowest states.
4. For each month of 2018: order count, total revenue from `order_payments`, and a CASE WHEN flag for whether it was a "peak month" (≥6,000 orders).

**Expected outputs**: not documented in the curriculum for these four questions — do not assert specific numbers; treat as open-ended analytical practice.

---
