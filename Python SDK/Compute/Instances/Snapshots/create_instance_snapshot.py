# File my_project/create_instance_snapshot.py

import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.membership import Membership
from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# Snapshot data to create
snapshot_data = {
    'project_id': 29,              # Change this to your project ID
    'instance_id': 141,            # The instance ID to create a snapshot of (must be running)
    'type': 'lxd',                 # "lxd" for LXD instances, "hyperv" for Hyper-V
    'name': 'test-snapshot-141'  # Descriptive name for the snapshot
}

# ================================================================= #
#                      Create Instance Snapshot                     #
# ================================================================= #
response = Compute.compute_snapshots.create(token=token, data=snapshot_data)

# Print out the json of the response data with beautiful formatting
pprint(response.json())