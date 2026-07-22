# Olist Schema — Phase 2b SQL

8 tables loaded into a **file-based** SQLite DB by `sql_setup.py` (`/content/olist.db` on Colab, a local temp `.db` otherwise).
All names/rows verified against `curriculum/phase-2b-sql/teaching-curriculum.md`.
Table names below are the **SQLite table names** students query (not the CSV filenames).

## Tables, columns, and join keys

### orders — 99,441 rows (Week 1+)
| Column | Notes |
|---|---|
| order_id | PK (36-char UUID) |
| customer_id | FK → customers.customer_id (1:1 with orders) |
| order_status | delivered, shipped, canceled, unavailable, invoiced, processing, created, approved |
| order_purchase_timestamp | TEXT, `YYYY-MM-DD HH:MM:SS`, 2016–2018 |
| order_delivered_customer_date | TEXT, nullable (NULL when not delivered) |
| order_estimated_delivery_date | TEXT |

### customers — 99,441 rows (Week 3+ joins)
| Column | Notes |
|---|---|
| customer_id | PK; FK target from orders |
| customer_state | 2-letter code (SP, RJ, MG, …) |
| customer_city | lowercase, accented |

### order_items — 112,650 rows (Week 2+)
| Column | Notes |
|---|---|
| order_id | FK → orders.order_id (1:many) |
| product_id | FK → products.product_id |
| seller_id | FK → sellers.seller_id |
| price | REAL, item price (BRL) |
| freight_value | REAL, shipping (BRL) |

### order_payments — 103,886 rows (Week 2+)
| Column | Notes |
|---|---|
| order_id | FK → orders.order_id |
| payment_type | credit_card, boleto, voucher, debit_card |
| payment_value | REAL (BRL) |
| payment_installments | INT (0–24) |

### order_reviews — 99,224 rows (Week 2+)
| Column | Notes |
|---|---|
| order_id | FK → orders.order_id |
| review_score | INT 1–5 |
| review_comment_message | TEXT, nullable |

### products — 32,951 rows (Week 6+)
| Column | Notes |
|---|---|
| product_id | PK |
| product_category_name | Portuguese category name (nullable — 610 NULL) |
| product_name_lenght* | **misspelled** (missing 'g') — real data-quality teaching moment |
| product_description_lenght* | **misspelled** too |

### sellers — 3,095 rows (Week 6+)
| Column | Notes |
|---|---|
| seller_id | PK |
| seller_state | 2-letter code |

### product_category_translation — 71 rows (Week 6+)
| Column | Notes |
|---|---|
| product_category_name | Portuguese (join key → products) |
| product_category_name_english | English translation |

## Canonical join paths
- Orders by customer geography: `orders JOIN customers ON orders.customer_id = customers.customer_id`
- Order revenue: `orders JOIN order_items ON orders.order_id = order_items.order_id`
- Category (English): `order_items JOIN products ON order_items.product_id = products.product_id JOIN product_category_translation USING (product_category_name)`
- Reviews / payments: join to `orders` on `order_id`

## Join cardinality & fan-out ⚠ (READ BEFORE WRITING ANY AGGREGATE-OVER-JOIN)

`order_id` is **not unique** in three tables. Joining any two of them (or joining one
to a fact column you then `SUM`/`AVG`/`COUNT(*)`) multiplies rows and silently inflates
the result. This is the single most common way an "expected value" ends up wrong.

| Table | Rows | Distinct `order_id` | Orders with >1 row | Grain |
|---|---|---|---|---|
| `orders` | 99,441 | 99,441 | 0 | **1 row per order** (safe base) |
| `customers` | 99,441 | — (keyed on `customer_id`, 1:1) | 0 | 1 row per order |
| `order_items` | 112,650 | 98,666 | 9,803 | **many rows per order** (one per line item) |
| `order_payments` | 103,886 | 99,440 | 2,961 | **many rows per order** |
| `order_reviews` | 99,224 | 98,673 | 547 | **many rows per order** |

**The rule:** never `SUM`/`AVG` a column, or `COUNT(*)`, across a query that directly
joins **two or more** of `order_items` / `order_payments` / `order_reviews`. Collapse
the non-base tables to **one row per `order_id` in a CTE first**, then join. (A bare
`COUNT(*)` after such a join counts fanned-out rows; use `COUNT(DISTINCT order_id)`.)

**Worked example — revenue + avg review per category (the correct pattern):**
```sql
WITH rev AS (                       -- collapse reviews to 1 row per order FIRST
  SELECT order_id, AVG(review_score) AS review_score
  FROM order_reviews
  GROUP BY order_id
)
SELECT t.product_category_name_english,
       SUM(oi.price)               AS total_revenue,   -- item grain, not fanned out
       AVG(r.review_score)         AS avg_review,
       COUNT(DISTINCT oi.order_id) AS order_count
FROM order_items oi
JOIN products p            ON oi.product_id = p.product_id
JOIN product_category_translation t USING (product_category_name)
LEFT JOIN rev r            ON oi.order_id = r.order_id   -- 1:1, no fan-out
GROUP BY t.product_category_name_english
ORDER BY total_revenue DESC;
-- health_beauty total_revenue = R$1,258,681.34  (matches the verified stat)
```
Joining raw `order_reviews` here instead of `rev` inflates `health_beauty` to
R$1,263,138.54 — a real defect that shipped in Phase 2a Week 7. The verified stats
below are all computed at correct grain; a query that reproduces them must be too.

## Verified stats (single source of truth for check-cell assertions)
| Fact | Value |
|---|---|
| Total orders | 99,441 |
| Delivered orders | 96,478 |
| Canceled orders | 625 |
| Orders with NULL delivery date | 2,965 |
| Top customer state | SP = 41,746 |
| Avg payment value | R$154.10 |
| Credit-card share (count) | 73.9% (76,795 / 103,886) |
| Overall avg review score | 4.09 |
| 5-star reviews | 57,328 (57.8%) |
| Total GMV (price + freight) | R$15,843,553.24 |
| Product revenue only | R$13,591,643.70 |
| Avg delivery days | 12.6 |
| Late deliveries | 7,826 (8.1% of delivered) |
| Products with null category | 610 |
| 2016 / 2017 / 2018 orders | 329 / 45,101 / 54,011 |
| November 2017 orders | 7,544 (Black Friday) |
| Top seller revenue | R$229,472.63 |
| Top category (English) | health_beauty = R$1,258,681.34 |

## SQLite gotchas to teach (and to respect when generating)
- Dates are TEXT. Use `strftime('%Y', order_purchase_timestamp)` etc., not date types.
- Integer division: `COUNT(...)*100 / total` truncates — use `* 1.0` to force REAL.
- `!=` and `<>` both work; NULLs need `IS NULL` / `IS NOT NULL` (never `= NULL`).
- No `FULL OUTER JOIN` in older SQLite — emulate with `LEFT JOIN ... UNION ...` (relevant Week 6+).
