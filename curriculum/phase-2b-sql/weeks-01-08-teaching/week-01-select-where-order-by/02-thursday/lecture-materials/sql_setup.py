"""
Standard Olist SQL Setup for Google Colab — Phase 2b SQL

Use this block as the FIRST code cell in every Phase 2b notebook (all weeks).

Design notes (why this differs from the Phase 2a pandas setup):
- We teach SQL with the `%%sql` cell magic (jupysql) so beginners write raw
  SQL, not `pd.read_sql("...")` strings. Students meet SQL syntax first;
  the Python wrapper comes later (Phase 2c).
- jupysql opens its OWN database connection. A `sqlite3.connect(":memory:")`
  database is private to that one connection, so a separate `%sql sqlite://`
  connection would see ZERO tables. We therefore build a **file-based**
  SQLite database at /content/olist.db and point both pandas (for loading)
  and jupysql (for querying) at the same file.
- `autopandas = True` makes every `%%sql` cell return a pandas DataFrame, so
  self-check cells can `assert` on `.iloc`/`.shape` directly.

After this cell runs, query with:

    %%sql
    SELECT * FROM orders LIMIT 5

Or capture a result for checking:

    %%sql result <<
    SELECT COUNT(*) AS n FROM orders WHERE order_status = 'delivered'
    # then in a plain Python cell:  assert int(result.iloc[0]['n']) == 96478
"""

import os
import sqlite3
import pandas as pd
from google.colab import drive

# 1) Mount Drive and locate the Olist CSVs
drive.mount('/content/drive')
DATA_DIR = "/content/drive/MyDrive/cohort7/datasets/olist"

# 2) Build a file-based SQLite database (shared by pandas + jupysql)
DB_PATH = "/content/olist.db"
conn = sqlite3.connect(DB_PATH)

tables = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
}

for table_name, filename in tables.items():
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {len(df):,} rows")

conn.close()
print("\nDatabase ready.")

# 3) Connect jupysql to the SAME database file
%load_ext sql
%config SqlMagic.autopandas = True          # %%sql cells return DataFrames
%config SqlMagic.feedback = 0               # quieter output
%sql sqlite:////content/olist.db

# Verify (expected row counts — do not alter without re-running against data):
#   orders 99,441 | customers 99,441 | order_items 112,650 | order_payments 103,886
#   order_reviews 99,224 | products 32,951 | sellers 3,095 | product_category_translation 71
