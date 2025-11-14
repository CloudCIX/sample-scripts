# File my_project/list_firewalls.py

import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      List All Firewalls                           #
# ================================================================= #
response = Compute.network_firewalls.list(token=token)

if response.status_code == 200:
    data = response.json()
    firewalls = data['content']
    
    print(f"Total firewalls: {data['total']}")
    print("=" * 50)
    
    if firewalls:
        for fw in firewalls:
            print(f"ID: {fw['id']}")
            print(f"Name: {fw.get('name', 'N/A')}")
            print(f"Project ID: {fw.get('project_id', 'N/A')}")
            print(f"Type: {fw.get('type', 'N/A')}")
            print(f"State: {fw.get('state', 'N/A')}")
            print(f"Created: {fw.get('created', 'N/A')}")
            print(f"Updated: {fw.get('updated', 'N/A')}")
            print("-" * 40)
        
        print("\nComplete JSON Response:")
        print("-" * 50)
        pprint(data)
    else:
        print("No firewalls found")
        
else:
    print(f"Error {response.status_code}: {response.text}")