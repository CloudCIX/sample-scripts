# File my_project/get_routers_by_project.py

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
project_id = 45               # Change this to your project ID

print(f"Getting routers for project {project_id}...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Get Routers by Project                       #
# ================================================================= #
response = Compute.network_routers.list(token=token)

if response.status_code == 200:
    routers_data = response.json()
    
    # Filter routers for the specified project only
    if 'content' in routers_data and routers_data['content']:
        project_routers = [router for router in routers_data['content'] if router.get('project_id') == project_id]
        
        print(f"Project {project_id} Router Summary:")
        print(f"Found: {len(project_routers)} routers")
        print("-" * 50)
        
        if project_routers:
            print("Router Details:")
            print("-" * 30)
            
            for router in project_routers:
                router_id = router.get('id', 'N/A')
                
                # Fetch complete router details including networks
                print(f"Fetching details for Router ID: {router_id}...")
                detail_response = Compute.network_routers.read(token=token, pk=router_id)
                
                if detail_response.status_code == 200:
                    router_details = detail_response.json().get('content', {})
                    
                    print("-" * 60)
                    print("Router Details:")
                    print("-" * 40)
                    print(f"ID: {router_details.get('id', 'N/A')}")
                    print(f"Name: {router_details.get('name', 'N/A')}")
                    print(f"Type: {router_details.get('type', 'N/A')}")
                    print(f"State: {router_details.get('state', 'N/A')}")
                    print(f"Project ID: {router_details.get('project_id', 'N/A')}")
                    print(f"Grace Period: {router_details.get('grace_period', 'N/A')} hours")
                    print(f"Created: {router_details.get('created', 'N/A')}")
                    print(f"Updated: {router_details.get('updated', 'N/A')}")
                    print(f"URI: {router_details.get('uri', 'N/A')}")
                    
                    # Display metadata with clean formatting
                    metadata = router_details.get('metadata', {})
                    if metadata:
                        print(f"\nExternal IP Configuration:")
                        print("-" * 30)
                        
                        # IPv4 Address details
                        ipv4_address = metadata.get('ipv4_address')
                        if ipv4_address:
                            print("IPv4 External Address:")
                            print(f"  Address: {ipv4_address.get('address', 'N/A')}")
                            print(f"  ID: {ipv4_address.get('id', 'N/A')}")
                            print(f"  Subnet ID: {ipv4_address.get('subnet_id', 'N/A')}")
                            print(f"  Created: {ipv4_address.get('created', 'N/A')}")
                        
                        # IPv6 Address details
                        ipv6_address = metadata.get('ipv6_address')
                        if ipv6_address:
                            print("\nIPv6 External Address:")
                            print(f"  Address: {ipv6_address.get('address', 'N/A')}")
                            print(f"  ID: {ipv6_address.get('id', 'N/A')}")
                            print(f"  Subnet ID: {ipv6_address.get('subnet_id', 'N/A')}")
                            print(f"  Created: {ipv6_address.get('created', 'N/A')}")
                    
                    # Show networks with clean formatting
                    networks = router_details.get('networks', [])
                    if networks:
                        print(f"\nInternal Networks ({len(networks)}):")
                        print("-" * 30)
                        for i, network in enumerate(networks, 1):
                            print(f"Network {i}:")
                            print(f"  Name: {network.get('name', 'N/A')}")
                            print(f"  IPv4 Gateway: {network.get('ipv4', 'N/A')}")
                            print(f"  IPv6 Gateway: {network.get('ipv6', 'N/A')}")
                            print(f"  VLAN: {network.get('vlan', 'N/A')}")
                            if i < len(networks):
                                print()
                    else:
                        print(f"\nInternal Networks: No networks configured")
                    
                    # Show specs if available
                    specs = router_details.get('specs', [])
                    if specs:
                        print(f"\nSpecifications ({len(specs)}):")
                        print("-" * 30)
                        for i, spec in enumerate(specs, 1):
                            print(f"  {spec.get('sku_name', 'N/A')}: {spec.get('quantity', 'N/A')}")
                    else:
                        print(f"\nSpecifications: Default router configuration")
                else:
                    print(f"Error fetching details for router {router_id}: {detail_response.status_code}")
                
                print("\n" + "="*70 + "\n")
        else:
            print(f"No routers found for project {project_id}")
            print("This project may not have any routers configured.")
    else:
        print("No router data found in the API response.")
        
else:
    print(f"Error: {response.status_code}")
    print(response.text)