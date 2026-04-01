#!/usr/bin/env python3
"""
Generate UML diagram PNG from Mermaid markup using online rendering service.
"""

import requests
import base64
import sys

# Read the Mermaid diagram
with open('uml_final.mmd', 'r') as f:
    mermaid_code = f.read()

print("📊 Generating UML diagram PNG...")
print(f"Mermaid code length: {len(mermaid_code)} characters")

# Use Mermaid Live Editor API to render the diagram
# This is a reliable method that doesn't require local installation
try:
    # Encode the diagram for the API
    encoded = base64.urlsafe_b64encode(mermaid_code.encode()).decode()
    
    # Use Mermaid Live Editor's render endpoint
    url = f"https://mermaid.ink/img/{encoded}"
    
    print(f"Fetching from: {url[:80]}...")
    
    # Fetch the image
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        # Save as PNG
        with open('uml_final.png', 'wb') as f:
            f.write(response.content)
        print("✅ Successfully generated uml_final.png!")
        print(f"File size: {len(response.content)} bytes")
    else:
        print(f"❌ Error: API returned status {response.status_code}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error generating PNG: {e}")
    print("\n📝 Alternative: Try installing mermaid-cli locally:")
    print("   npm install -g @mermaid-js/mermaid-cli")
    print("   mmdc -i uml_final.mmd -o uml_final.png")
    sys.exit(1)
