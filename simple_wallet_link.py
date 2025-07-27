#!/usr/bin/env python
# Simple wallet link generator

import json
import urllib.parse

def main():
    print("Creating simple Google Wallet link test")
    
    # Create a minimal wallet object
    wallet_object = {
        "id": "3388000000022956210.test-receipt-123",
        "classId": "3388000000022956210.receipt-class",
        "genericType": "GENERIC_TYPE_UNSPECIFIED",
        "cardTitle": {
            "defaultValue": {
                "language": "en-US",
                "value": "Test Receipt"
            }
        }
    }
    
    # Create the wallet link
    json_data = json.dumps({"genericObjects": [wallet_object]})
    encoded_data = urllib.parse.quote(json_data)
    wallet_link = f"https://pay.google.com/gp/v/save/{encoded_data}"
    
    print("\nGenerated Google Wallet link:")
    print(wallet_link)
    print("\nLink length:", len(wallet_link))
    
    print("\nCopy this link and try it in your browser to see if it works!")

if __name__ == "__main__":
    main()
