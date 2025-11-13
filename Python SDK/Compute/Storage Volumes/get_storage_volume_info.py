# File my_project/get_storage_volume_info.py

import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

# NOTE: environ variables must be set before importing cloudcix

from cloudcix.api.membership import Membership
from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# Volume ID to get information for
volume_id = 123                    # Change this to your volume ID

# ================================================================= #
#                      Get Volume Information                       #
# ================================================================= #
response = Compute.storage_volumes.read(token=token, pk=volume_id)

# Print out the json of the response data with beautiful formatting
pprint (response.json())