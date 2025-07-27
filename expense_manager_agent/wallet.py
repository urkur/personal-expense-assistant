from google_wallet_implementation import GoogleWalletPassManager
import sys
import os
import datetime

# Add the parent directory to sys.path to allow importing from the project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now we can import from the expense_manager_agent package
from expense_manager_agent.tools import get_receipt_data_by_image_id

def create_receipt_wallet_pass(receipt_id):
    """
    Create a Google Wallet pass for a receipt.
    
    Args:
        receipt_id (str): The ID of the receipt to create a pass for
        
    Returns:
        str: A shareable link to add the pass to Google Wallet
    """
    # Get receipt data
    receipt_data = get_receipt_data_by_image_id(receipt_id)
    
    if not receipt_data:
        print(f"Error: Receipt with ID {receipt_id} not found")
        return None
    
    # Extract receipt details
    store_name = receipt_data.get("store_name", "Unknown Store")
    transaction_time = receipt_data.get("transaction_time", "")
    total_amount = receipt_data.get("total_amount", 0.0)
    currency = receipt_data.get("currency", "USD")
    
    # Format date for display
    try:
        transaction_date = datetime.datetime.fromisoformat(transaction_time.replace("Z", "+00:00"))
        formatted_date = transaction_date.strftime("%B %d, %Y")
    except:
        formatted_date = transaction_time
    
    # Initialize with your credentials
    wallet_manager = GoogleWalletPassManager(
        service_account_file='hack2skill-raseed-7655fd0d36ad.json',
        issuer_id='3388000000022956210'
    )
    
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
    
    return share_link

# If run directly with a receipt ID argument
if __name__ == "__main__":
    if len(sys.argv) > 1:
        receipt_id = sys.argv[1]
        share_link = create_receipt_wallet_pass(receipt_id)
        if share_link:
            print(f"Share this link to add receipt to Google Wallet: {share_link}")
    else:
        # Demo with generic pass
        wallet_manager = GoogleWalletPassManager(
            service_account_file='hack2skill-raseed-7655fd0d36ad.json',
            issuer_id='3388000000022956210'
        )
        
        # Define demo pass content
        pass_data = {
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Demo Receipt'
                }
            },
            'textModulesData': [{
                'header': 'Store',
                'body': 'Grocery Store',
                'id': 'store'
            }, {
                'header': 'Amount',
                'body': '$45.67',
                'id': 'amount'
            }, {
                'header': 'Date',
                'body': 'July 27, 2025',
                'id': 'date'
            }],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'https://expense-assistant.example.com/demo'
            }
        }
        
        # Generate shareable link
        share_link = wallet_manager.create_jwt_new_pass(
            'receipt_class', 
            'demo_receipt', 
            pass_data
        )
        
        print(f"Demo wallet pass link: {share_link}")
