# File my_project/list_images.py

import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      List Available OS Images                     #
# ================================================================= #
# Query parameters for listing images
params = {
    'limit': 50,         # Number of images per page (0-100)
    'page': 0,           # Page number (0-based)
    'order': 'sku_name', # Order by sku_name (default), id, or -sku_name for descending
}

# Optional filtering examples:
# params['search[os_variant__icontains]'] = 'ubuntu'  # Search for Ubuntu variants
# params['search[sku_name__icontains]'] = 'server'    # Search for server images
# params['search[region_id]'] = 1                     # Filter by specific region
# params['exclude[os_variant__icontains]'] = 'windows' # Exclude Windows images

response = Compute.compute_images.list(token=token, params=params)

if response.status_code == 200:
    data = response.json()
    images = data.get('content', [])
    metadata = data.get('_metadata', {})
    
    print(f"Available OS Images (Page {metadata.get('page', 0) + 1})")
    print(f"Showing {len(images)} of {metadata.get('total_records', 0)} total images")
    print("=" * 60)
    
    if images:
        for image in images:
            print(f"ID: {image.get('id', 'N/A')}")
            print(f"SKU Name: {image.get('sku_name', 'N/A')}")
            print(f"OS Variant: {image.get('os_variant', 'N/A')}")
            print(f"Filename: {image.get('filename', 'N/A')}")
            print("-" * 40)
    else:
        print("No images found matching the criteria")
        
else:
    print(f"Error {response.status_code}: {response.text}")