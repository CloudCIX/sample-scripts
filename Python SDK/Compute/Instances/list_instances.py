# File my_project/list_instances.py

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
project_id = 123  # Change this to your project ID

# ================================================================= #
#                      List Project Instances                       #
# ================================================================= #
print(f"Listing Instances for Project {project_id}")
print("=" * 50)

response = Compute.compute_instances.list(token=token, params={'search[project_id]': project_id})

if response.status_code == 200:
    instances = response.json()['content']
    total = response.json()['total']
    
    print(f"Found {total} instance(s):")
    print()
    
    if instances:
        for instance in instances:
            instance_id = instance.get('id')
            instance_name = instance.get('name', 'N/A')
            instance_state = instance.get('state', 'N/A')
            created = instance.get('created', 'N/A')
            
            print(f"Instance: {instance_name} (ID: {instance_id})")
            print(f"  State: {instance_state}")
            print(f"  Created: {created}")
            print()
    else:
        print("No instances found for this project")
else:
    print(f"Failed to list instances: {response.status_code}")
    pprint(response.json())