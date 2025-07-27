"""
Test script for Google Wallet pass generation
"""

from google_wallet_implementation import GoogleWalletPassManager

def test_wallet_pass():
    """Test the Google Wallet pass generation with a sample receipt"""
    
    # Initialize with credentials
    wallet_manager = GoogleWalletPassManager(
        service_account_file='hack2skill-raseed-7655fd0d36ad.json',
        issuer_id='3388000000022956210'
    )
    
    # Create sample receipt data
    receipt_id = "test123"
    store_name = "Grocery Store"
    total_amount = 45.67
    formatted_date = "July 27, 2025"
    currency = "USD"
    
    # Define pass content for a receipt
    pass_data = {
        'cardTitle': {
            'defaultValue': {
                'language': 'en-US',
                'value': f'Receipt: {store_name}'
            }
        },
        'textModulesData': [
            {
                'header': 'Store',
                'body': store_name,
                'id': 'store_name'
            },
            {
                'header': 'Date',
                'body': formatted_date,
                'id': 'date'
            },
            {
                'header': 'Amount',
                'body': f'{currency} {total_amount:.2f}',
                'id': 'amount'
            },
            {
                'header': 'Receipt ID',
                'body': receipt_id,
                'id': 'receipt_id'
            }
        ],
        'barcode': {
            'type': 'QR_CODE',
            'value': f'https://expense-assistant.example.com/receipt/{receipt_id}'
        }
    }
    
    # Generate shareable link
    pass_object_id = f'receipt_{receipt_id}'
    share_link = wallet_manager.create_jwt_new_pass(
        'receipt_class', 
        pass_object_id, 
        pass_data
    )
    
    print(f"Sample receipt wallet pass link: {share_link}")
    print(f"Store: {store_name}")
    print(f"Date: {formatted_date}")
    print(f"Amount: {currency} {total_amount:.2f}")
    print(f"Receipt ID: {receipt_id}")
    
    # Test with different receipt format
    print("\n--- Alternative Receipt Format ---")
    
    # Business expense receipt
    business_pass_data = {
        'cardTitle': {
            'defaultValue': {
                'language': 'en-US',
                'value': 'Business Expense'
            }
        },
        'textModulesData': [
            {
                'header': 'Vendor',
                'body': 'Office Supplies Inc.',
                'id': 'vendor'
            },
            {
                'header': 'Date',
                'body': 'July 26, 2025',
                'id': 'date'
            },
            {
                'header': 'Amount',
                'body': 'USD 120.50',
                'id': 'amount'
            },
            {
                'header': 'Category',
                'body': 'Office Supplies',
                'id': 'category'
            }
        ],
        'barcode': {
            'type': 'QR_CODE',
            'value': 'https://expense-assistant.example.com/business/B789'
        }
    }
    
    business_link = wallet_manager.create_jwt_new_pass(
        'business_receipt', 
        'business_B789', 
        business_pass_data
    )
    
    print(f"Business expense wallet pass link: {business_link}")

if __name__ == "__main__":
    test_wallet_pass()
