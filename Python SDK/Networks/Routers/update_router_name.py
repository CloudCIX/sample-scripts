# File my_project/rename_router.py

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

# Configuration
router_id = 123               # Change this to the router ID you want to rename
new_name = 'My Updated Router Name'  # Change this to the new router name

# Update data - rename only
update_data = {
    'name': new_name
}

print(f"Renaming router {router_id} to '{new_name}'...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Rename Router                                #
# ================================================================= #
response = Compute.network_routers.partial_update(token=token, pk=router_id, data=update_data)

if response.status_code == 200:
    router_data = response.json()
    print("Router renamed successfully!")
    print("\nUpdated Router Details:")
    print("-" * 40)
    
    if 'content' in router_data:
        router = router_data['content']
        print(f"Router ID: {router.get('id', 'N/A')}")
        print(f"New Name: {router.get('name', 'N/A')}")
        print(f"Type: {router.get('type', 'N/A')}")
        print(f"State: {router.get('state', 'N/A')}")
        print(f"Project ID: {router.get('project_id', 'N/A')}")
        print(f"Updated: {router.get('updated', 'N/A')}")
        
elif response.status_code == 404:
    print(f"Router with ID {router_id} not found.")
elif response.status_code == 403:
    print(f"Permission denied for router {router_id}.")
else:
    print(f"Error renaming router: {response.status_code}")
    print("Response:")
    try:
        pprint(response.json())
    except:
        print(response.text)