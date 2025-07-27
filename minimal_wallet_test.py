#!/usr/bin/env python
# Minimal test for wallet link generation

import urllib.parse
import json

def create_simplified_wallet_link():
    """Create a simplified Google Wallet pass link."""
    store_name = "Test Store"
    receipt_id = "test-receipt-123"
    formatted_date = "July 27, 2024"
    total_amount = 42.99
    currency = "USD"
    
    # Create a simplified wallet object with minimal fields
    simplified_object = {
        "id": "3388000000022956210.receipt-" + receipt_id,
        "classId": "3388000000022956210.receipt-class",
        "state": "ACTIVE",
        "genericType": "GENERIC_TYPE_UNSPECIFIED",
        "cardTitle": {
            "defaultValue": {
                "language": "en-US",
                "value": f"{store_name} Receipt"
            }
        },
        "header": {
            "defaultValue": {
                "language": "en-US",
                "value": f"RECEIPT: {formatted_date}"
            }
        },
        "barcode": {
            "type": "QR_CODE",
            "value": receipt_id
        },
        "textModulesData": [
            {
                "header": "TOTAL",
                "body": f"{currency} {total_amount:.2f}",
                "id": "total_amount"
            }
        ]
    }
    
    # Create the wallet link
    json_data = json.dumps({"genericObjects": [simplified_object]})
    encoded_data = urllib.parse.quote(json_data)
    wallet_link = f"https://pay.google.com/gp/v/save/{encoded_data}"
    
    return wallet_link

if __name__ == "__main__":
    # Generate and print the wallet link
    wallet_link = create_simplified_wallet_link()
    
    print("\nGenerated Google Wallet Link:")
    print(wallet_link)
    print("\nLink length:", len(wallet_link))
    
    # Check if the link is valid
    if len(wallet_link) > 2000:
        print("\nWARNING: Link is too long! Google URLs might have length limitations.")
    else:
        print("\nLink length is acceptable.")
