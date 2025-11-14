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
project_id = 123               # Change this to your project ID

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
            # Print only the filtered project data
            print("Project routers data:")
            pprint({'project_id': project_id, 'routers': project_routers})
            print("\n" + "-"*50 + "\n")
            
            print("Router Details:")
            print("-" * 30)
            for router in project_routers:
                router_id = router.get('id', 'N/A')
                router_name = router.get('name', 'N/A')
                router_state = router.get('state', 'N/A')
                router_type = router.get('type', 'N/A')
                router_created = router.get('created', 'N/A')
                router_updated = router.get('updated', 'N/A')
                
                print(f"Router ID: {router_id}")
                print(f"Name: {router_name}")
                print(f"Type: {router_type}")
                print(f"State: {router_state}")
                print(f"Project ID: {router.get('project_id', 'N/A')}")
                print(f"Created: {router_created}")
                print(f"Updated: {router_updated}")
                print(f"URI: {router.get('uri', 'N/A')}")
                
                # Show networks if available
                networks = router.get('networks', [])
                if networks:
                    print(f"Networks ({len(networks)}):")
                    for network in networks:
                        network_name = network.get('name', 'N/A')
                        network_ipv4 = network.get('ipv4', 'N/A')
                        network_id = network.get('id', 'N/A')
                        print(f"  - ID: {network_id}")
                        print(f"    Name: {network_name}")
                        print(f"    IPv4: {network_ipv4}")
                        print(f"    URI: {network.get('uri', 'N/A')}")
                else:
                    print("Networks: No networks configured")
                
                print("\n" + "="*30 + "\n")
        else:
            print(f"No routers found for project {project_id}")
            print("This project may not have any routers configured.")
    else:
        print("No router data found in the API response.")
        
else:
    print(f"Error: {response.status_code}")
    print(response.text)