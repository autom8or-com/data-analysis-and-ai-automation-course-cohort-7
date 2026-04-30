"""
Olist Data Loading Utility

Loads all 11 CSVs from olist-data.zip and returns a dict of DataFrames.
Used by validate_notebooks.py during code cell execution.
"""

import zipfile
import pandas as pd


def load_olist_data(zip_path: str) -> dict:
    """
    Load all Olist datasets from zip file.

    Args:
        zip_path: Path to olist-data.zip

    Returns:
        Dictionary of DataFrames: {
            'customers': df, 'orders': df, 'order_items': df,
            'order_reviews': df, 'order_payments': df, 'products': df,
            'sellers': df, 'product_category_name_translation': df, ...
        }

    Raises:
        FileNotFoundError: If zip file not found
        Exception: If error during CSV parsing
    """

    csv_files = {
        'customers': 'olist_customers_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'order_reviews': 'olist_order_reviews_dataset.csv',
        'order_payments': 'olist_order_payments_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'product_category_name_translation': 'olist_product_category_name_translation.csv',
        'geolocation': 'olist_geolocation_dataset.csv',
        'marketing_qualified_leads': 'olist_marketing_qualified_leads_dataset.csv',
    }

    data = {}

    try:
        with zipfile.ZipFile(zip_path) as z:
            for key, filename in csv_files.items():
                try:
                    with z.open(filename) as f:
                        data[key] = pd.read_csv(f)
                except KeyError:
                    # File not in zip — skip gracefully
                    continue

    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset zip not found at {zip_path}")
    except Exception as e:
        raise Exception(f"Error loading Olist data: {str(e)}")

    return data
