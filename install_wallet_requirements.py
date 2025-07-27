#!/usr/bin/env python
# This script installs the required dependencies for the Google Wallet integration

import subprocess
import sys

def install_dependencies():
    """Install required dependencies for Google Wallet integration."""
    dependencies = [
        "pyjwt[crypto]",  # JWT for authentication with Google
        "requests",       # HTTP requests to Google APIs
    ]
    
    print("Installing dependencies for Google Wallet integration...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
        print("Successfully installed the following packages:")
        for package in dependencies:
            print(f"  - {package}")
        print("\nGoogle Wallet integration dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
