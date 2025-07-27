# Google Wallet Integration Updates

This document summarizes the changes made to implement Google Wallet integration with service account JSON file support.

## Updated Files

### 1. `settings.py`
- Added `SERVICE_ACCOUNT_FILE` to support direct JSON file configuration
- This allows users to either specify the file path or include the service account details directly

### 2. `settings.yaml.example`
- Added two configuration options for service account authentication:
  - Option 1: Using a service account JSON file (recommended)
  - Option 2: Including service account details directly in settings

### 3. `expense_manager_agent/tools.py`
- Updated imports to include JWT and requests libraries for authentication
- Modified `create_google_wallet_pass_link` function to:
  - Support both service account file and direct service account info
  - Add JWT authentication with Google's APIs
  - Create wallet classes and objects via Google's APIs
  - Implement proper error handling and fallback mechanisms

### 4. Added New Files
- `install_wallet_requirements.py`: Script to install the required dependencies (PyJWT, requests)
- `test_wallet.py`: Script to test the Google Wallet integration

### 5. `README.md`
- Added Google Wallet integration to features list
- Updated tech stack to include Google Wallet API

## How to Use the New Functionality

1. Configure your Google Wallet integration by:
   - Setting up a service account in Google Cloud Platform
   - Enabling Google Pay API for Passes
   - Getting your Issuer ID

2. Update your `settings.yaml` file with either:
   - Your service account JSON file path (recommended), or
   - Your service account details directly

3. Install the required dependencies:
   ```bash
   python install_wallet_requirements.py
   ```

4. Test the integration:
   ```bash
   python test_wallet.py
   ```

5. Once configured, any receipt uploaded to the system will automatically generate a Google Wallet pass link in the response.

## Authentication Flow

The Google Wallet integration uses JWT (JSON Web Tokens) for authentication:

1. The system reads the service account credentials (either from file or settings)
2. A JWT token is generated and signed with the private key
3. The token is exchanged for a Google API access token
4. The access token is used to create/update Google Wallet passes

## Error Handling

The implementation includes robust error handling:
- Falls back to a basic wallet link if JWT authentication fails
- Logs detailed error messages for troubleshooting
- Gracefully handles missing credentials

## Security Considerations

- Service account JSON files contain sensitive credentials and should be kept secure
- The SERVICE_ACCOUNT_FILE path should point to a location not accessible via the web
- Consider using environment variables or a secret management solution for production
