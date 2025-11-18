import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token
from pprint import pprint

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      Get Firewalls by Project                     #
# ================================================================= #
project_id = 123  # Change this to your project ID

# Get list of firewalls for the project
params = {'search[project_id]': project_id}
response = Compute.network_firewalls.list(token=token, params=params)

if response.status_code == 200:
    data = response.json()
    firewalls = data['content']
    
    print(f"Firewalls for Project ID: {project_id}")
    print("=" * 50)
    
    if firewalls:
        print(f"Found {len(firewalls)} firewall(s):")
        print()
        
        for firewall in firewalls:
            firewall_id = firewall.get('id', 'N/A')
            firewall_name = firewall.get('name', 'N/A')
            firewall_state = firewall.get('state', 'N/A')
            created = firewall.get('created', 'N/A')
            
            print(f"Firewall: {firewall_name} (ID: {firewall_id})")
            print(f"  State: {firewall_state}")
            print(f"  Created: {created}")
            
            # Get rule count
            detail_response = Compute.network_firewalls.read(token=token, pk=firewall_id)
            if detail_response.status_code == 200:
                firewall_details = detail_response.json()['content']
                rules = firewall_details.get('rules', [])
                print(f"  Rules: {len(rules)} configured")
            
            print()
    else:
        print("No firewalls found for this project")
        
elif response.status_code == 403:
    print("Permission denied - you don't have access to this project")
else:
    print(f"Error {response.status_code}: {response.text}")