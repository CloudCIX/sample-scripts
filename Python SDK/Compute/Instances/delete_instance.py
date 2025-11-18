# File my_project/delete_instance.py

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
instance_id = 123             # Change this to your instance ID

# Data to delete instance
delete_data = {
    'state': 'delete'
}

print(f"Deleting instance {instance_id}...")
print("Setting state to 'delete' to initiate instance removal")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Delete Instance                              #
# ================================================================= #
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data=delete_data)

# Print out the json of the response data with beautiful formatting
pprint(response.json())