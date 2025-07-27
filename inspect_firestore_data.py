#!/usr/bin/env python
# Script to inspect the data in Firestore

import logging
from google.cloud import firestore
from settings import get_settings
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SETTINGS = get_settings()
DB_CLIENT = firestore.Client(project=SETTINGS.GCLOUD_PROJECT_ID)
COLLECTION = DB_CLIENT.collection(SETTINGS.DB_COLLECTION_NAME)

def inspect_firestore_data():
    """Examine the raw data in Firestore to understand what we're working with"""
    try:
        # Get all documents in the collection
        docs = list(COLLECTION.stream())
        doc_count = len(docs)
        
        logger.info(f"Found {doc_count} documents in collection {SETTINGS.DB_COLLECTION_NAME}")
        
        if doc_count == 0:
            logger.info("No documents found in the collection. Add some data first.")
            return "No data found in Firestore"
        
        # Print information about each document
        for i, doc in enumerate(docs):
            data = doc.to_dict()
            logger.info(f"\nDocument {i+1}/{doc_count} (ID: {doc.id}):")
            
            # Basic document info
            logger.info(f"  Receipt ID: {data.get('receipt_id')}")
            logger.info(f"  Store Name: {data.get('store_name')}")
            logger.info(f"  Transaction Time: {data.get('transaction_time')}")
            logger.info(f"  Total Amount: {data.get('total_amount')}")
            
            # Check purchased items
            purchased_items = data.get('purchased_items', [])
            logger.info(f"  Number of items: {len(purchased_items)}")
            
            # Count items with categories
            items_with_category = [item for item in purchased_items if 'category' in item]
            logger.info(f"  Items with categories: {len(items_with_category)}/{len(purchased_items)}")
            
            # Print some details of the first few items
            max_items_to_show = min(5, len(purchased_items))
            if max_items_to_show > 0:
                logger.info("  First few items:")
                for j in range(max_items_to_show):
                    item = purchased_items[j]
                    item_info = {
                        "name": item.get("name", "N/A"),
                        "price": item.get("price", 0),
                        "quantity": item.get("quantity", 1),
                        "category": item.get("category", "No category")
                    }
                    logger.info(f"    Item {j+1}: {json.dumps(item_info)}")
        
        return f"Successfully inspected {doc_count} documents"
    except Exception as e:
        logger.error(f"Error inspecting Firestore data: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = inspect_firestore_data()
    print(result)
