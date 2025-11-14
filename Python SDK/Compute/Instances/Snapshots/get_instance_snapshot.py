# File my_project/get_instance_snapshot.py

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
snapshot_id = 144             # Change this to your snapshot ID

# ================================================================= #
#                      Get Snapshot Details                         #
# ================================================================= #
response = Compute.compute_snapshots.read(token=token, pk=snapshot_id)

# Print out the json of the response data with beautiful formatting
pprint(response.json())