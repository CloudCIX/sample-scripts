# File my_project/create_ip_group.py

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

# IP Group data to create
ip_group_data = {
    'project_id': 123,              # Change this to your project ID
    'name': 'office_locations',     # Descriptive name
    'description': 'IP addresses for office locations',
    'cidrs': [
        '91.123.4.56/24',         # Office network 1
        '91.456.7.89/24',         # Office network 2
    ]
}

# ================================================================= #
#                      Create IP Group                              #
# ================================================================= #
response = Compute.network_ip_groups.create(token=token, data=ip_group_data)

# Print out the json of the response data with beautiful formatting
pprint(response.json())