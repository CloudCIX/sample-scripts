# File my_project/create_geofilter.py

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

# Geofilter data to create
geofilter_data = {
    'project_id': 123,              # Change this to your project ID
    'type': 'geo',                 # 'geo' for geographic/country-based filtering
    'name': 'My First Geofilter',   # Change this to your desired geofilter name
    'rules': [                     # Geographic filtering rules
        {
            'allow': True,         # Allow traffic from Ireland (IPv4)
            'group_name': '@IE_v4',
            'inbound': True
        },
        {
            'allow': True,         # Allow traffic from Ireland (IPv6)
            'group_name': '@IE_v6',
            'inbound': True
        },
    ]
}

# ================================================================= #
#                      Create Geo Firewall                          #
# ================================================================= #
response = Compute.network_firewalls.create(token=token, data=geofilter_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())
