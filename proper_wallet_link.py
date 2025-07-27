#!/usr/bin/env python
# Updated wallet link generator with proper format

import json
import urllib.parse
import time

def create_proper_wallet_link():
    """
    Create a Google Wallet link with the proper format following Google's specifications.
    Uses the minimal required fields to ensure compatibility.
    """
    # Use a timestamp to make the object ID unique
    object_id = f"receipt-test-{int(time.time())}"
    issuer_id = "3388000000022956210"
    
    # Create a wallet object with only the required fields
    wallet_object = {
        "id": f"{issuer_id}.{object_id}",
        "classId": f"{issuer_id}.receipt-class",
        "logo": {
            "sourceUri": {
                "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
            }
        },
        "cardTitle": {
            "defaultValue": {
                "language": "en-US",
                "value": "Test Receipt"
            }
        },
        "header": {
            "defaultValue": {
                "language": "en-US",
                "value": "RECEIPT"
            }
        },
        "barcode": {
            "type": "QR_CODE",
            "value": "test-receipt-123"
        },
        "textModulesData": [
            {
                "header": "TOTAL",
                "body": "USD 42.99",
                "id": "total_amount"
            },
            {
                "header": "DATE",
                "body": "July 27, 2025",
                "id": "date"
            }
        ]
    }
    
    # Create the wallet link in the correct format
    json_data = json.dumps({"genericObjects": [wallet_object]})
    encoded_data = urllib.parse.quote(json_data)
    wallet_link = f"https://pay.google.com/gp/v/save/{encoded_data}"
    
    return wallet_link

if __name__ == "__main__":
    # Generate and print the wallet link
    wallet_link = create_proper_wallet_link()
    
    print("\nGenerated Google Wallet Link:")
    print(wallet_link)
    print("\nLink length:", len(wallet_link))
    
    print("\nCopy this link and try it in your browser!")
    print("Make sure to paste the entire URL without line breaks.")
