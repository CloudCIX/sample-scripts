# File my_project/update_ip_group.py

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

# Update data for IP group
update_data = {
    'name': 'Test_IP_Group',
    'description': 'Update Group Description',
    'cidrs': [
        '91.123.4.56/24',         # Office network 1
        '91.456.7.89/24',         # Office network 2
        '91.789.0.1/24',         # Add a new CIDR NOTE: When updating, you must provide the full list of CIDRs or it will remove any not included.
    ]
}

# Configuration
ip_group_id = 123              # Change this to your IP Group ID

# ================================================================= #
#                      Update IP Group                              #
# ================================================================= #
response = Compute.network_ip_groups.partial_update(token=token, pk=ip_group_id, data=update_data)

# Print out the json of the response data with beautiful formatting
pprint(response.json())