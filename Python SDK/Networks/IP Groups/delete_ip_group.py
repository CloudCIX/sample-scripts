# File my_project/delete_ip_group.py

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
ip_group_id = 123              # Change this to your IP Group ID

# ================================================================= #
#                      Delete IP Group                              #
# ================================================================= #
response = Compute.network_ip_groups.delete(token=token, pk=ip_group_id)

# Print out the json of the response data with beautiful formatting
if response.status_code == 204:
    print("IP Group deleted successfully!")
    print(f"Deleted IP Group ID: {ip_group_id}")
else:
    print(f"Error deleting IP Group (Status: {response.status_code})")
    try:
        pprint(response.json())
    except:
        print("Response text:", response.text)