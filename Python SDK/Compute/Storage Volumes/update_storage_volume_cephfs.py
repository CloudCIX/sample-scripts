# File my_project/update_storage_volume_cephfs.py

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

# Volume ID and new size to update
volume_id = 123                   # Change this to your volume ID
new_size = 32                    # Change to 32GB

# Volume update data
volume_update_data = {
    'specs': [
        {'quantity': new_size, 'sku_name': 'CEPH_002'}    # New storage size
    ],
    'state': 'update_running',
}

# ================================================================= #
#                      Update Volume Size                           #
# ================================================================= #
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data=volume_update_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())