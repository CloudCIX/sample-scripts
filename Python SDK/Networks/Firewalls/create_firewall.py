# File my_project/create_firewall.py

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

# Firewall data to create
firewall_data = {
    'project_id': 123,              # Change this to your project ID
    'type': 'project',             # 'project' for fine-grained rules, 'geo' for country-based
    'name': 'My First Firewall',    # Change this to your desired firewall name
    'rules': [                     # Security rules
        {
            'allow': True,
            'description': 'Allow SSH to Project from Cork Office',
            'destination': '*',
            'inbound': True,
            'port': '22',
            'protocol': 'tcp',
            'source': '91.100.5.55'
        },      
    ]
}

# ================================================================= #
#                      Create Project Firewall                      #
# ================================================================= #
response = Compute.network_firewalls.create(token=token, data=firewall_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())