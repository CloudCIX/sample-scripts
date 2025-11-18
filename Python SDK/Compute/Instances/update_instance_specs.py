# File my_project/update_instance_specs.py

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

# Instance ID and new specifications
instance_id = 123                  # Change this to your instance ID

# Updated instance specifications
instance_update_data = {
    'specs': [
        {'quantity': 8, 'sku_name': 'RAM_001'},        # Updates the RAM to 8GB
        {'quantity': 32, 'sku_name': 'SSD_001'},       # Updates the SSD to 32GB
        {'quantity': 4, 'sku_name': 'vCPU_001'}        # Updates the vCPU to 4 cores NOTE: Use vCPU_002 for type=hyperv
    ],
        'state': 'update_running',
}

# ================================================================= #
#                      Update Instance Specifications               #
# ================================================================= #
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data=instance_update_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())