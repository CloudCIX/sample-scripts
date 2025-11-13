# File my_project/update_router_network_names.py

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
router_id = 123               # Change this to your router ID

# Update network names - modify as needed for your networks
update_data = {
    'networks': [
        {
            'name': 'management-network',   # Change to your desired name
            'vlan': 1111                    # Change to your VLAN ID
        },
        {
            'name': 'frontend-servers',     # Change to your desired name
            'vlan': 2222                    # Change to your VLAN ID
        },
        {
            'name': 'backend-database',     # Change to your desired name
            'vlan': 3333                    # Change to your VLAN ID
        }
    ]
}

print(f"Renaming networks on router {router_id}...")
print("Network updates:")
for network in update_data['networks']:
    print(f"  - VLAN {network['vlan']} → '{network['name']}'")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Rename Router Networks                       #
# ================================================================= #
response = Compute.network_routers.partial_update(token=token, pk=router_id, data=update_data)

if response.status_code == 200:
    router_data = response.json()
    print("Router networks renamed successfully!")
    print("\nUpdated Router Details:")
    print("-" * 40)
    pprint(router_data)
    print("\n" + "="*50 + "\n")
    
    if 'content' in router_data:
        router = router_data['content']
        
        print("Router Summary:")
        print("-" * 30)
        print(f"Router ID: {router.get('id', 'N/A')}")
        print(f"Name: {router.get('name', 'N/A')}")
        print(f"Updated: {router.get('updated', 'N/A')}")
        
        # Show all networks with their new names
        networks = router.get('networks', [])
        if networks:
            print(f"\nRenamed Networks ({len(networks)}):")
            print("-" * 40)
            for i, network in enumerate(networks, 1):
                print(f"Network {i}:")
                print(f"  Name: {network.get('name', 'N/A')}")
                print(f"  IPv4: {network.get('ipv4', 'N/A')}")
                print(f"  IPv6: {network.get('ipv6', 'N/A')}")
                print(f"  VLAN: {network.get('vlan', 'N/A')}")
                
                # Show rename confirmation
                vlan = network.get('vlan')
                print(f"  └─ Network successfully renamed")
                print()
        else:
            print("No networks found in response.")
    
elif response.status_code == 400:
    print("Bad Request - Invalid network configuration")
    print("Response:")
    pprint(response.json())
elif response.status_code == 404:
    print(f"Router with ID {router_id} not found.")
elif response.status_code == 403:
    print(f"Permission denied for router {router_id}.")
else:
    print(f"Error renaming networks: {response.status_code}")
    print("Response:")
    try:
        pprint(response.json())
    except:
        print(response.text)