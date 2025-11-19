# File my_project/get_ip_group.py

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
ip_group_id = 469              # Change this to your IP Group ID

# ================================================================= #
#                      Get IP Group Details                         #
# ================================================================= #
response = Compute.network_ip_groups.read(token=token, pk=ip_group_id)

# Print out the json of the response data with beautiful formatting
pprint(response.json())