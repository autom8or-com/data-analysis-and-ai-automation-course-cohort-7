# Olist Dataset — Phases 2a Python, 2b SQL, 2c Capstone

**File:** `olist-data.zip`
**Contains:** All 11 Olist CSVs

| File | Rows | Notes |
|---|---|---|
| `olist_orders_dataset.csv` | 99,441 | Core order facts |
| `olist_customers_dataset.csv` | 99,441 | Customer city/state |
| `olist_order_items_dataset.csv` | 112,650 | Revenue, products per order |
| `olist_products_dataset.csv` | 32,951 | Category (has nulls; column name typo: `product_name_lenght`) |
| `olist_order_reviews_dataset.csv` | 99,224 | Review scores |
| `olist_order_payments_dataset.csv` | 103,886 | Payment type, instalments |
| `olist_sellers_dataset.csv` | 3,095 | Seller state |
| `product_category_name_translation.csv` | 71 | English category names |
| `olist_geolocation_dataset.csv` | 1,000,163 | Lat/lon (optional use) |
| `olist_closed_deals_dataset.csv` | 842 | Sales funnel |
| `olist_marketing_qualified_leads_dataset.csv` | 8,000 | MQL data |

**Source:** [Kaggle — Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Setup (Google Colab)

Upload the unzipped folder to Google Drive, then mount in every Colab session:

```python
from google.colab import drive
drive.mount('/content/drive')
DATA_DIR = "/content/drive/MyDrive/olist/"
```
