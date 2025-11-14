# File my_project/update_project.py

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
project_id = 123               # Change this to the project ID you want to update

# Project data to update (PATCH - only include fields you want to change)
update_data = {
    'name': 'Updated Project Name',        # New project name (optional)
    'note': 'Updated project description'  # New note/description (optional)
}

print(f"Updating project {project_id}...")
print("Data to update:")
pprint(update_data)
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Update Project                               #
# ================================================================= #
response = Compute.project.partial_update(token=token, pk=project_id, data=update_data)

if response.status_code == 200:
    print("Project updated successfully!")
    print("\nUpdated Project Details:")
    print("-" * 40)
    pprint(response.json())
else:
    print(f"Error updating project: {response.status_code}")
    print("Response:")
    pprint(response.json())