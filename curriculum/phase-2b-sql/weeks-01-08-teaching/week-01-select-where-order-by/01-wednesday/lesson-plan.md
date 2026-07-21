# Week 1 — SELECT, WHERE & ORDER BY: Wednesday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-01-wed-demo.ipynb`
- [ ] `sql_setup.py` first cell runs and loads all 8 tables into `/content/olist.db`
- [ ] Student exercise link ready to share: `week-01-wed-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Write SELECT with WHERE, ORDER BY, and LIMIT from memory

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py` |
| 0:10–0:30 | SELECT — choosing columns | Demo `SELECT *` vs named columns; discuss why `SELECT *` is a bad habit in production |
| 0:30–0:55 | WHERE — filtering rows | Demo filtering on `order_status`; verify counts live |
| 0:55–1:20 | AND / OR in WHERE | Demo combining conditions; verify combined count |
| 1:20–1:45 | ORDER BY and LIMIT | Demo sorting ascending/descending with LIMIT |
| 1:45–2:00 | Mini-challenge & wrap-up | Individual practice, debrief, preview Thursday's group exercise |

---

## Key Concepts

### SELECT — choosing columns
Retrieve all columns with `SELECT *` or name specific columns explicitly. No verified numeric output for this concept — it's a syntax/behavior demonstration.

### WHERE — filtering rows
Filter rows with a boolean predicate (equality, inequality).

Expected outputs (verified against the Olist dataset):
- `SELECT COUNT(*) FROM orders WHERE order_status = 'delivered'` → **96,478**
- `SELECT COUNT(*) FROM orders WHERE order_status = 'canceled'` → **625**
- `SELECT COUNT(*) FROM orders WHERE order_status != 'delivered'` → **2,963**

Common mistake to watch for: using `= NULL` instead of `IS NULL` — `=` never matches NULL in SQL.

### AND / OR in WHERE
Combine multiple conditions with AND / OR.

Expected outputs (verified against the Olist dataset):
- `SELECT COUNT(*) FROM orders WHERE order_status = 'canceled' OR order_status = 'unavailable'` → **1,234** (625 canceled + 609 unavailable)

### ORDER BY and LIMIT
Sort result rows ascending/descending and cap the number returned.

Common mistake to watch for: integer division truncates in SQLite — force REAL division with `* 1.0` when computing a percentage/ratio.

---

## Group Exercise

Wednesday has no separate group exercise — it is an individual/paired practice session (mini-challenge in the demo notebook) building toward Thursday's group exercise.

---
