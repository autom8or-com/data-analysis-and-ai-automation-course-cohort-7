"""
Standard Olist Data Loading for Google Colab

Use this code snippet in every notebook from Week 3 onwards.
"""

import pandas as pd
from google.colab import drive
import os

# Mount Google Drive
drive.mount('/content/drive')

# Define paths
olist_path = '/content/drive/MyDrive/olist-data'

# Load all datasets
orders = pd.read_csv(os.path.join(olist_path, 'olist_orders_dataset.csv'))
customers = pd.read_csv(os.path.join(olist_path, 'olist_customers_dataset.csv'))
order_items = pd.read_csv(os.path.join(olist_path, 'olist_order_items_dataset.csv'))
products = pd.read_csv(os.path.join(olist_path, 'olist_products_dataset.csv'))
reviews = pd.read_csv(os.path.join(olist_path, 'olist_order_reviews_dataset.csv'))
payments = pd.read_csv(os.path.join(olist_path, 'olist_order_payments_dataset.csv'))
sellers = pd.read_csv(os.path.join(olist_path, 'olist_sellers_dataset.csv'))
product_translations = pd.read_csv(os.path.join(olist_path, 'olist_product_category_name_translation.csv'))

# Verify datasets loaded
print(f"✓ Loaded {len(orders):,} orders")
print(f"✓ Loaded {len(customers):,} customers")
print(f"✓ Loaded {len(order_items):,} order items")
print(f"✓ Loaded {len(products):,} products")
print(f"✓ Loaded {len(reviews):,} reviews")
print(f"✓ Loaded {len(payments):,} payments")
print(f"✓ Loaded {len(sellers):,} sellers")
print(f"✓ Loaded {len(product_translations):,} product translations")

# Quick data checks
print(f"\nOrders shape: {orders.shape}")
print(f"Orders columns: {orders.columns.tolist()}")
print(f"Date range: {orders['order_purchase_timestamp'].min()} to {orders['order_purchase_timestamp'].max()}")
