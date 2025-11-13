# File my_project/list_projects.py

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

params = {'limit': 50, 'page': 0}

# ================================================================= #
#                      List Compute Projects                        #
# ================================================================= #
response = Compute.project.list(token=token, params=params)

# Print out the json of the response data with beautiful formatting
pprint (response.json())