# Olist Dataset Schema

11 CSVs, 99,441 primary orders. All verified against teaching-curriculum.

## Core Tables (used in curriculum)

### olist_orders_dataset.csv
**Rows**: 99,441 | **Used from**: Week 3

| Column | Type | Notes |
|---|---|---|
| order_id | string (36 chars) | Primary key, UUID format |
| customer_id | string | Foreign key to customers |
| order_status | categorical | delivered, cancelled, unavailable, processing, shipped, invoiced, created |
| order_purchase_timestamp | datetime | ISO format, 2016–2018 |

**Verified stats:**
- Total rows: 99,441
- `delivered` orders: ~96,482
- `cancelled` orders: ~625
- Date range: 2016-09-04 to 2018-10-17

### olist_customers_dataset.csv
**Rows**: 99,441 | **Used from**: Week 5

| Column | Type | Notes |
|---|---|---|
| customer_id | string (36 chars) | Foreign key (1:1 with orders) |
| customer_city | string | City name (lowercase, with accents) |
| customer_state | string | Two-letter state code (SP, MG, RJ, etc) |

**Verified stats:**
- Top state: SP (41,746 orders)
- Top city: sao paulo (15,540 orders)

### olist_order_items_dataset.csv
**Rows**: 112,650 | **Used from**: Week 5

| Column | Type | Notes |
|---|---|---|
| order_id | string | Foreign key to orders |
| product_id | string (36 chars) | Foreign key to products |
| seller_id | string (36 chars) | Foreign key to sellers |
| price | float | Item price in BRL |
| freight_value | float | Shipping cost in BRL |

### olist_products_dataset.csv
**Rows**: 32,951 | **Used from**: Week 6

| Column | Type | Notes |
|---|---|---|
| product_id | string (36 chars) | Foreign key |
| product_category_name | string | Portuguese category name |

**Note**: Typo in column `product_name_lenght` (missing 'n')

### olist_order_reviews_dataset.csv
**Rows**: 99,224 | **Used from**: Week 7

| Column | Type | Notes |
|---|---|---|
| review_id | string (36 chars) | Primary key |
| order_id | string | Foreign key |
| review_score | int | 1–5 stars |

**Verified stats:**
- 5★: ~48,800 | 1★: ~23,500

### olist_order_payments_dataset.csv
**Rows**: 103,886 | **Used from**: Week 7

| Column | Type | Notes |
|---|---|---|
| order_id | string | Foreign key |
| payment_type | categorical | credit_card, boleto, voucher, debit_card |
| payment_installments | int | 0–24 installments |
| payment_value | float | Amount in BRL |

### olist_sellers_dataset.csv
**Rows**: 3,095 | **Used from**: Week 7

| Column | Type | Notes |
|---|---|---|
| seller_id | string (36 chars) | Foreign key |
| seller_state | string | Two-letter state code |

### olist_product_category_name_translation.csv
**Rows**: 71 | **Used from**: Week 7

| Column | Type | Notes |
|---|---|---|
| product_category_name | string | Portuguese name |
| product_category_name_english | string | English translation |
