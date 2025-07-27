# Google Wallet Integration Guide

This guide will help you set up Google Wallet integration for your Personal Expense Assistant, allowing users to save their receipt information to Google Wallet.

## Prerequisites

1. A Google Cloud Platform account
2. Access to the Google Pay & Wallet APIs
3. A service account with appropriate permissions

## Step 1: Set Up Google Pay & Wallet API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your project or create a new one
3. Enable the "Google Pay & Wallet API"
4. Create a new service account with the "Google Pay & Wallet API" role
5. Generate and download a JSON key file for this service account

## Step 2: Configure Your Application

There are two ways to set up your service account credentials:

### Option 1: Reference the JSON file directly (Recommended)

1. Copy the `settings.yaml.example` file to `settings.yaml`
2. Update the Google Wallet settings in `settings.yaml` to reference your service account file:
   ```yaml
   # Google Wallet Settings
   WALLET_ISSUER_ID: "your_wallet_issuer_id"  # Get this from Google Pay API for Passes
   SERVICE_ACCOUNT_FILE: "/path/to/your-service-account-file.json"
   ```

3. Place your downloaded service account JSON file in a secure location and update the path above

### Option 2: Include service account details directly in settings

Alternatively, you can copy the service account details directly into the settings file:

```yaml
# Google Wallet Settings
WALLET_ISSUER_ID: "your_wallet_issuer_id"  # Get this from Google Pay API for Passes
SERVICE_ACCOUNT_INFO:
  type: "service_account"
  project_id: "your_project_id"
  private_key_id: "your_private_key_id"
  private_key: "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
  client_email: "your-service-account@your-project.iam.gserviceaccount.com"
  client_id: "your_client_id"
  auth_uri: "https://accounts.google.com/o/oauth2/auth"
  token_uri: "https://oauth2.googleapis.com/token"
  auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs"
  client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

## Step 3: Get an Issuer ID

1. Go to the [Google Pay and Wallet Console](https://pay.google.com/business/console/)
2. Sign in with your Google account
3. Create a new account if needed
4. Go to "Settings" > "Issuer settings"
5. Copy your Issuer ID and update it in the `settings.yaml` file

## Step 4: Test the Integration

1. Start your application
2. Upload a receipt image
3. Verify that the response includes a Google Wallet pass link
4. Click the link to test saving the receipt to Google Wallet

## How It Works

When a user uploads a receipt image:

1. The receipt data is extracted and stored in Firestore
2. A Google Wallet pass is created with the receipt details
3. A link to save the pass is included in the response
4. The user can click this link to save the receipt to their Google Wallet

## JSON Response Format

When a receipt is processed, the system returns a JSON response in this format:

```json
{
  "receipt_id": "unique_receipt_id",
  "store_name": "Store Name",
  "transaction_time": "2023-07-25T12:34:56",
  "total_amount": 45.67,
  "currency": "USD",
  "purchased_items": [
    {
      "name": "Item Name",
      "price": 12.34,
      "quantity": 1,
      "category": "Category",
      "tax": 1.23
    }
  ],
  "status": "success",
  "message": "Receipt stored successfully with ID: unique_receipt_id",
  "google_wallet_link": "https://pay.google.com/gp/v/save/..."
}
```

## Troubleshooting

If you encounter issues:

1. Check that your service account has the correct permissions
2. Verify that your `WALLET_ISSUER_ID` is correct
3. Make sure your service account key information is properly formatted in settings.yaml
4. Check the application logs for detailed error messages

## Resources

- [Google Pay & Wallet API Documentation](https://developers.google.com/pay/passes/reference/web/overview)
- [Google Pay Pass Class Reference](https://developers.google.com/pay/passes/reference/web/v1/genericclass)
- [Google Pay Pass Object Reference](https://developers.google.com/pay/passes/reference/web/v1/genericobject)
