"""
Olist Data Loading Utility

Loads all 11 CSVs from either:
  - olist-data.zip (local file, legacy)
  - a directory of extracted CSVs (Routine environment, downloaded from Drive)

Used by validate_notebooks.py during code cell execution.
"""

import os
import zipfile
import pandas as pd


CSV_FILES = {
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


def load_olist_from_folder(folder_path: str) -> dict:
    """
    Load Olist datasets from a directory of extracted CSVs.

    Args:
        folder_path: Path to directory containing the Olist CSV files

    Returns:
        Dictionary of DataFrames keyed by table name

    Raises:
        FileNotFoundError: If folder does not exist
    """
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Olist data folder not found at {folder_path}")

    data = {}
    for key, filename in CSV_FILES.items():
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            try:
                data[key] = pd.read_csv(filepath)
            except Exception as e:
                print(f"  ⚠ Could not load {filename}: {e}")
        # Missing files skipped gracefully

    if not data:
        raise FileNotFoundError(
            f"No Olist CSV files found in {folder_path}. "
            "Expected files like olist_orders_dataset.csv"
        )

    return data


def load_olist_data(zip_path: str) -> dict:
    """
    Load Olist datasets from a zip file (legacy / local use).

    Args:
        zip_path: Path to olist-data.zip or phase-2-python-sql.zip

    Returns:
        Dictionary of DataFrames keyed by table name

    Raises:
        FileNotFoundError: If zip file not found
    """
    try:
        data = {}
        with zipfile.ZipFile(zip_path) as z:
            for key, filename in CSV_FILES.items():
                try:
                    with z.open(filename) as f:
                        data[key] = pd.read_csv(f)
                except KeyError:
                    continue
        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset zip not found at {zip_path}")
    except Exception as e:
        raise Exception(f"Error loading Olist data: {str(e)}")
