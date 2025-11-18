# File my_project/get_compute_instance.py

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

# VM ID to check status
vm_id = 123            # Change this to your VM ID

# ================================================================= #
#                      Get VM Status                                #
# ================================================================= #
response = Compute.compute_instances.read(token=token, pk=vm_id)

# Print out the json of the response data with beautiful formatting
pprint (response.json())