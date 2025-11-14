# File my_project/create_project.py

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

# Project data to create
project_data = {
    'name': 'My Project 2',  # Change this to your desired project name
    'region_id': 1234,             # Change this to your desired region ID
    'note': 'Test project created via SDK'  # Optional note
}

# ================================================================= #
#                      Create Compute Project                       #
# ================================================================= #
response = Compute.project.create(token=token, data=project_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())