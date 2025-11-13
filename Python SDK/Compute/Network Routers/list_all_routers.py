# File my_project/list_all_routers.py

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

print("Listing all routers across all projects...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      List All Routers                             #
# ================================================================= #
response = Compute.network_routers.list(token=token)

if response.status_code == 200:
    routers_data = response.json()
    
    # Print full response
    print("Complete router response:")
    pprint(routers_data)
    print("\n" + "="*50 + "\n")
    
    # Display summary of all routers
    if 'content' in routers_data and routers_data['content']:
        print(f"All Routers Summary (Total: {routers_data.get('total', 0)}):")
        print("-" * 60)
        
        # Group routers by project for better overview
        projects = {}
        for router in routers_data['content']:
            project_id = router.get('project_id', 'Unknown')
            if project_id not in projects:
                projects[project_id] = []
            projects[project_id].append(router)
        
        # Display grouped by project
        for project_id, project_routers in projects.items():
            print(f"\nProject {project_id} ({len(project_routers)} routers):")
            print("-" * 40)
            
            for router in project_routers:
                router_id = router.get('id', 'N/A')
                router_name = router.get('name', 'N/A')
                router_state = router.get('state', 'N/A')
                router_type = router.get('type', 'N/A')
                router_created = router.get('created', 'N/A')
                
                print(f"  Router ID: {router_id} | Name: {router_name}")
                print(f"    └─ Type: {router_type} | State: {router_state}")
                print(f"    └─ Created: {router_created}")
                
                # Show networks if available
                networks = router.get('networks', [])
                if networks:
                    print(f"    └─ Networks ({len(networks)}):")
                    for network in networks:
                        network_name = network.get('name', 'N/A')
                        network_ipv4 = network.get('ipv4', 'N/A')
                        network_id = network.get('id', 'N/A')
                        print(f"        └─ ID: {network_id} | {network_name}: {network_ipv4}")
                else:
                    print(f"    └─ No networks configured")
                print()
    else:
        print("No routers found.")
        
else:
    print(f"Error: {response.status_code}")
    print(response.text)