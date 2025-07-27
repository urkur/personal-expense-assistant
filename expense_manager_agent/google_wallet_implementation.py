"""
Google Wallet Implementation for Personal Expense Assistant
"""

import json
import time
import jwt
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleWalletPassManager:
    """
    A class to manage Google Wallet passes for the Personal Expense Assistant.
    
    This class handles the creation of JWT tokens that can be used to generate
    shareable links for adding passes to Google Wallet.
    """
    
    def __init__(self, service_account_file, issuer_id):
        """
        Initialize the GoogleWalletPassManager with the required credentials.
        
        Args:
            service_account_file (str): Path to the service account JSON file
            issuer_id (str): The Google Wallet issuer ID
        """
        self.service_account_file = service_account_file
        self.issuer_id = issuer_id
        self._load_service_account()
        
    def _load_service_account(self):
        """Load the service account credentials from the JSON file."""
        try:
            # Check if file exists
            if not Path(self.service_account_file).exists():
                logger.error(f"Service account file not found: {self.service_account_file}")
                raise FileNotFoundError(f"Service account file not found: {self.service_account_file}")
                
            with open(self.service_account_file, 'r') as f:
                self.service_account_info = json.load(f)
                
            # Extract necessary fields
            self.client_email = self.service_account_info.get('client_email')
            self.private_key = self.service_account_info.get('private_key')
            
            if not self.client_email or not self.private_key:
                raise ValueError("Invalid service account file: missing required fields")
                
            logger.info(f"Successfully loaded service account for {self.client_email}")
        except Exception as e:
            logger.error(f"Error loading service account: {str(e)}")
            # For demo purposes, use mock data if file not found
            logger.warning("Using mock credentials for demonstration purposes")
            self.client_email = "demo-account@example.iam.gserviceaccount.com"
            self.private_key = "MOCK_PRIVATE_KEY"
    
    def create_jwt_new_pass(self, class_id, object_id, pass_data):
        """
        Create a JWT token for a new Google Wallet pass.
        
        Args:
            class_id (str): The class ID for the pass (e.g., 'membership_class')
            object_id (str): The unique object ID for this pass (e.g., 'member_12345')
            pass_data (dict): The pass data to include in the JWT
            
        Returns:
            str: A shareable link that can be used to add the pass to Google Wallet
        """
        try:
            # For demonstration, we'll create a mock JWT
            # In a real implementation, this would use the actual Google Wallet API
            
            # Define the JWT payload
            payload = {
                "iss": self.client_email,
                "aud": "google",
                "typ": "savetowallet",
                "iat": int(time.time()),
                "origins": ["https://expense-assistant.example.com"],
                "payload": {
                    "genericObjects": [{
                        "id": f"{self.issuer_id}.{object_id}",
                        "classId": f"{self.issuer_id}.{class_id}",
                        "genericType": "GENERIC_TYPE_UNSPECIFIED",
                        "logo": {
                            "sourceUri": {
                                "uri": "https://example.com/logo.png"
                            }
                        },
                        "cardTitle": pass_data.get("cardTitle", {}),
                        "header": {
                            "defaultValue": {
                                "language": "en-US",
                                "value": "Personal Expense Receipt"
                            }
                        },
                        "textModulesData": pass_data.get("textModulesData", []),
                        "barcode": pass_data.get("barcode", {})
                    }]
                }
            }
            
            # Sign the JWT
            # For demonstration purposes, we'll generate a mock token if using mock credentials
            if self.private_key == "MOCK_PRIVATE_KEY":
                logger.warning("Using mock JWT for demonstration")
                token = f"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.MOCK_JWT_FOR_{object_id}.signature"
            else:
                # Actually sign the JWT with the private key
                token = jwt.encode(
                    payload,
                    self.private_key,
                    algorithm="RS256"
                )
            
            # Create the shareable link
            share_link = f"https://pay.google.com/gp/v/save/{token}"
            logger.info(f"Generated shareable link for {object_id}")
            
            return share_link
            
        except Exception as e:
            logger.error(f"Error creating JWT: {str(e)}")
            return f"ERROR: Failed to create pass link: {str(e)}"
