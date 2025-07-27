#!/usr/bin/env python
# Test script for generating Google Wallet links

import json
from expense_manager_agent.tools import create_google_wallet_pass_link

def test_wallet_link():
    """Test generating a Google Wallet link with simplified data."""
    test_receipt = {
        "receipt_id": "test-receipt-123",
        "store_name": "Test Store",
        "transaction_time": "2024-06-30T16:26:26",
        "total_amount": 42.99,
        "currency": "USD",
        "purchased_items": [
            {
                "name": "Test Item 1",
                "price": 12.99,
                "quantity": 1,
                "tax": 1.04,
                "category": "Other"
            },
            {
                "name": "Test Item 2",
                "price": 29.99,
                "quantity": 1,
                "tax": 2.40,
                "category": "Other"
            }
        ]
    }
    
    # Generate the wallet link
    wallet_link = create_google_wallet_pass_link(test_receipt)
    
    print("\nGenerated Google Wallet Link:")
    print(wallet_link)
    print("\nLink length:", len(wallet_link))
    
    # Check if the link is valid
    if len(wallet_link) > 2000:
        print("\nWARNING: Link is too long! Google URLs might have length limitations.")
    else:
        print("\nLink length is acceptable.")
    
    # Extract the parameters to verify
    if "save/" in wallet_link:
        encoded_data = wallet_link.split("save/")[1]
        try:
            # Decode and parse the data
            import urllib.parse
            decoded_data = urllib.parse.unquote(encoded_data)
            json_data = json.loads(decoded_data)
            
            print("\nWallet Object Details:")
            generic_objects = json_data.get("genericObjects", [])
            if generic_objects:
                obj = generic_objects[0]
                print(f"ID: {obj.get('id')}")
                print(f"Class ID: {obj.get('classId')}")
                
                # Get card title
                card_title = obj.get("cardTitle", {}).get("defaultValue", {}).get("value", "")
                print(f"Card Title: {card_title}")
                
                # Get header
                header = obj.get("header", {}).get("defaultValue", {}).get("value", "")
                print(f"Header: {header}")
                
                # Check number of text modules
                text_modules = obj.get("textModulesData", [])
                print(f"Text Modules: {len(text_modules)}")
                
                print("\nLink appears to be correctly formatted.")
            else:
                print("No generic objects found in the wallet data.")
        except Exception as e:
            print(f"\nError parsing wallet data: {e}")
    else:
        print("\nUnexpected link format - could not extract wallet data.")

if __name__ == "__main__":
    test_wallet_link()
