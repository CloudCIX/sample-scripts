# File my_project/create_storage_volume_cephfs.py

import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

# NOTE: environ variables must be set before importing cloudcix

from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# CephFS Storage Volume data to create
ceph_volume_data = {
    'project_id': 123,              # Change this to your project ID
    'name': 'my-shared-filesystem',  # Change this to your desired volume name
    'type': 'cephfs',              # CephFS shared storage type
    'specs': [
        {'quantity': 16, 'sku_name': 'CEPH_002'}      # 16GB CephFS storage using the CEPH_002 SKU (SSD)
    ]
}

# ================================================================= #
#                      Create CephFS Storage Volume                 #
# ================================================================= #
response = Compute.storage_volumes.create(token=token, data=ceph_volume_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())