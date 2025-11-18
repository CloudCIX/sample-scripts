# File my_project/list_snapshots.py

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
#                      List Project Snapshots                       #
# ================================================================= #
print(f"Listing Snapshots for Project {project_id}")
print("=" * 50)

response = Compute.compute_snapshots.list(token=token, params={'search[project_id]': project_id})

if response.status_code == 200:
    snapshots = response.json()['content']
    total = response.json()['total']
    
    print(f"Found {total} snapshot(s):")
    print()
    
    if snapshots:
        for snapshot in snapshots:
            snapshot_id = snapshot.get('id')
            snapshot_name = snapshot.get('name', 'N/A')
            snapshot_state = snapshot.get('state', 'N/A')
            snapshot_type = snapshot.get('type', 'N/A')
            instance_id = snapshot.get('instance_id', 'N/A')
            created = snapshot.get('created', 'N/A')
            
            print(f"Snapshot: {snapshot_name} (ID: {snapshot_id})")
            print(f"  State: {snapshot_state}")
            print(f"  Type: {snapshot_type}")
            print(f"  Instance ID: {instance_id}")
            print(f"  Created: {created}")
            print()
    else:
        print("No snapshots found for this project")
else:
    print(f"Failed to list snapshots: {response.status_code}")
    pprint(response.json())