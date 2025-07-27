#!/usr/bin/env python
# Very basic test

print("Hello, this is a basic test!")

try:
    import json
    import urllib.parse
    
    # Simple test of JSON and URL encoding
    data = {"test": "value"}
    json_data = json.dumps(data)
    encoded = urllib.parse.quote(json_data)
    
    print(f"Original data: {data}")
    print(f"JSON data: {json_data}")
    print(f"URL encoded: {encoded}")
    
except Exception as e:
    print(f"Error: {e}")
