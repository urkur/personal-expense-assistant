#!/usr/bin/env python
# Test script for the improved categorization function

import logging
from expense_manager_agent.tools import categorize_item

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample items from your list
test_items = [
    "MONO CHX DUSTER SEL",
    "IW POLPAT NO 10 [MBR",
    "WOODEN PUNJABI BELA",
    "DOORMAT TURKEY 3858",
    "DOORMAT LILY 4060 [",
    "SL PROMO THALI -nos",
    "SL CB TOPE 12-nos",
    "SL MUKTA WATI 5.5 [",
    "SL APPLE HATI NO.6",
    "SL PARI GLASS WITH",
    "SS NEDA CHALNI -nos",
    "SL HEAVY WIRE T-nos",
    "SL GRATER 9 PL HND",
    "PL IRIS CLOTH CLIP",
    "PL DHOMES PET JAR C",
    "PL DHOMES PET JAR C",
    "HD SCOTCH SL SCRUB",
    "HOOD KNIFE WUK4",
    "SL RICE SPOON 4",
    "SL SPOON SET 20 PCS",
    "SL ANJALI GAS LIGHT",
    "HO SCOTCH SPONGE WI",
    "GREY RECYCLED SHOPP"
]

def test_categorization():
    """Test the AI-based categorization on our sample items"""
    logger.info("Testing AI-based categorization on sample items")
    
    results = {}
    for item in test_items:
        category = categorize_item(item)
        if category not in results:
            results[category] = []
        results[category].append(item)
    
    # Print summary by category
    logger.info("Categorization Results Summary:")
    for category, items in results.items():
        logger.info(f"{category} ({len(items)} items):")
        for item in items:
            logger.info(f"  - {item}")
    
    # Calculate percentage categorized as "Other"
    other_count = len(results.get("Other", []))
    total_count = len(test_items)
    other_percentage = (other_count / total_count) * 100 if total_count > 0 else 0
    
    logger.info(f"Items categorized as 'Other': {other_count}/{total_count} ({other_percentage:.1f}%)")

if __name__ == "__main__":
    test_categorization()
