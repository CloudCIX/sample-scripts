# File my_project/get_image_details.py

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

# Image ID to get detailed information for
image_id = 1                       # Change this to your desired image ID
                                   # Available IDs from your list:
                                   # 1 = UBUNTU2404, 2 = UBUNTU2004LTS, 3 = MSServer2022
                                   # 4 = MSServer2019, 5 = RockyLinux9, 6 = RockyLinux8
                                   # 7 = UBUNTU2404-A100, 8 = UBUNTU2404-H100

# ================================================================= #
#                      Get Image Details                            #
# ================================================================= #
response = Compute.compute_images.read(token=token, pk=image_id)

# Print out the json of the response data with beautiful formatting
pprint (response.json())