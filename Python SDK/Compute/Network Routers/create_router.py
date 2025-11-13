# File my_project/create_vrf.py

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

# VRF (Router) data to create
vrf_data = {
    'project_id': 123,          # Change this to your project ID
    'type': 'router',
    'name': 'My Test Router',         # Change this to your desired Router name
    'networks': [                  # Private networks for this Router
        {
            'name': 'my-network-1',
            'ipv4': '10.0.1.0/24'
        },
        {
            'name': 'my-network-2', 
            'ipv4': '10.0.2.0/24'
        }
    ]
}

# ================================================================= #
#                      Create VRF (Router)                          #
# ================================================================= #
response = Compute.network_routers.create(token=token, data=vrf_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())