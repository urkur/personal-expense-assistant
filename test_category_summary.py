#!/usr/bin/env python
# Test script for category summary

import logging
from expense_manager_agent.tools import get_category_summary, categorize_existing_receipts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_category_summary():
    """Test the category summary functionality"""
    try:
        # First, make sure all existing receipts are categorized
        logger.info("Running categorize_existing_receipts to ensure all items have categories")
        categorize_result = categorize_existing_receipts()
        logger.info(f"Categorization result: {categorize_result}")
        
        # Now get the category summary for current month (default)
        logger.info("Getting category summary for current month (default)")
        summary = get_category_summary()
        logger.info(f"Category summary result: {summary}")
        
        # Try for all time
        logger.info("Getting category summary for all time")
        all_time_summary = get_category_summary(start_time="2020-01-01T00:00:00Z", end_time="2030-01-01T00:00:00Z")
        logger.info(f"All-time category summary result: {all_time_summary}")
        
        return "Tests completed successfully"
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        return f"Test failed: {str(e)}"

if __name__ == "__main__":
    result = test_category_summary()
    print(result)
