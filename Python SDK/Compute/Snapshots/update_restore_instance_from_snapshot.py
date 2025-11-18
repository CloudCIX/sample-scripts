# File my_project/update_restore_instance_from_snapshot.py

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
snapshot_id = 123             # Change this to your snapshot ID

# ================================================================= #
#                      Revert Instance to Snapshot                  #
# ================================================================= #
response = Compute.compute_snapshots.partial_update(
    token=token,
    pk=snapshot_id,
    data={'state': 'update_running'}
)

# Print out the json of the response data with beautiful formatting
pprint(response.json())