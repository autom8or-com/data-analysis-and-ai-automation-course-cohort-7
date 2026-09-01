# Week 6 — Multi-table Joins and Complex Aggregations: Thursday Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: `week-06-thu-demo.ipynb`
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share: `week-06-thu-exercises.ipynb`
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. Combine customer geography, payments, and delivery timing into a single full-pipeline query.
2. Extend three- and four-table join patterns to answer geographic and seller-level business questions, applying fan-out-safe aggregation throughout.

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run `sql_setup.py`; recap Wednesday's category and review-score joins |
| 0:10–0:45 | Full pipeline: customer state + payment + delivery | `orders → customers → order_payments`; demo + mini-challenge |
| 0:45–1:15 | Going Deeper — SUM vs AVG under fan-out, delivery variance by state | Demo walkthrough |
| 1:15–1:45 | Group Exercise / Exercises | 4-table joins: freight by state, SP vs RJ categories, GMV per seller state, high-price categories |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview Week 7 (CTEs and Advanced Analytics) |

---

## Key Concepts

### Full pipeline: customer state + payment + delivery

```sql
SELECT c.customer_state,
       COUNT(DISTINCT o.order_id) AS order_count,
       ROUND(SUM(op.payment_value), 2) AS total_payment_value,
       ROUND(AVG(op.payment_value), 2) AS avg_order_value,
       ROUND(AVG(
           julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)
       ), 1) AS avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments op ON o.order_id = op.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_payment_value DESC
LIMIT 8
```

Expected top 8 states (verified against the Olist dataset):

| customer_state | order_count | total_payment_value | avg_order_value | avg_delivery_days |
|---|---|---|---|---|
| SP | 40,500 | 5,770,266.19 | 136.39 | 8.8 |
| RJ | 12,350 | 2,055,690.45 | 158.08 | 15.4 |
| MG | 11,354 | 1,819,277.61 | 154.12 | 12.0 |
| RS | 5,345 | 861,802.40 | 155.45 | 15.3 |
| PR | 4,923 | 781,919.55 | 152.45 | 12.0 |
| SC | 3,546 | 595,208.40 | 162.58 | 14.9 |
| BA | 3,256 | 591,270.60 | 169.76 | 19.3 |
| DF | 2,080 | 346,146.17 | 161.60 | 12.9 |

Common mistake to watch for: `AVG(op.payment_value)` here averages per *payment row*, not per *order* — an order split across several installments/vouchers contributes multiple rows. `SUM` survives this because totals don't care about row count, but `AVG` and `avg_delivery_days` shift once `order_payments` is pre-aggregated to one row per order in a CTE first. See the notebook's "Going Deeper" section for the side-by-side comparison.

---

## Group Exercise

The four Thursday exercises (worked in the separate `week-06-thu-exercises.ipynb` notebook):

1. Build a 4-table join: orders → customers → order_items → sellers. Find average freight value paid by customers in each state when ordering from sellers in SP.
2. Which product categories are most popular in SP vs RJ? (orders → customers → order_items → products → translation). Show top 5 categories per state.
3. What is the total GMV (price + freight) per seller state? Join order_items with sellers.
4. Find categories where the average item price is above R$150. Show category name, count, avg price.

Expected outputs (verified against the Olist dataset, see `week-06-thu-solutions.ipynb` for full detail):
- Q1: 27 states; PB tops the list at 349 orders / R$42.78 avg freight; SP lowest at 31,502 orders / R$13.20.
- Q2: 10 rows (top 5 per state); RJ top category `bed_bath_table` (1,393 orders); SP top category `bed_bath_table` (4,416 orders).
- Q3: 23 seller states; SP leads with 70,188 orders / R$10,235,883.88 GMV (64.6% of total GMV).
- Q4: 17 categories above R$150 avg price; `computers` highest at R$1,098.34; cross-checks against Wednesday's verified table (`watches_gifts` R$201.14, `cool_stuff` R$167.36).

---

## Weekly Assignment

1. Build a complete category performance table: category name (English), order count, seller count, total revenue, avg price, avg review score. *(This requires a 4-table join: order_items + products + translation + order_reviews via orders)*
2. Which seller state has the highest average review score from their customers?
3. Find the 3 categories with the highest freight-to-price ratio (freight / price).
4. How many distinct products has each seller sold? Show top 10 sellers by product variety.
5. Challenge: Find orders where the delivery took longer than 30 days AND the review score was 1. How many are there?

---
