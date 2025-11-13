# File my_project/get_project.py

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
project_id = 123               # Change this to the project ID you want to retrieve

print(f"Retrieving project {project_id}...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Get Specific Project                         #
# ================================================================= #
response = Compute.project.read(token=token, pk=project_id)

if response.status_code == 200:
    project_data = response.json()
    print("Project Details:")
    print("-" * 40)
    pprint(project_data)
    
    # Extract and display key information
    if 'content' in project_data:
        project = project_data['content']
        print("\nProject Summary:")
        print("-" * 30)
        print(f"ID: {project.get('id', 'N/A')}")
        print(f"Name: {project.get('name', 'N/A')}")
        print(f"Note: {project.get('note', 'N/A')}")
        print(f"Address ID: {project.get('address_id', 'N/A')}")
        print(f"Region ID: {project.get('region_id', 'N/A')}")
        print(f"Manager ID: {project.get('manager_id', 'N/A')}")
        print(f"Reseller ID: {project.get('reseller_id', 'N/A')}")
        print(f"Closed: {project.get('closed', 'N/A')}")
        print(f"Created: {project.get('created', 'N/A')}")
        print(f"Updated: {project.get('updated', 'N/A')}")
        print(f"URI: {project.get('uri', 'N/A')}")
        
elif response.status_code == 404:
    print(f"Project with ID {project_id} not found.")
    print("Response:")
    pprint(response.json())
else:
    print(f"Error retrieving project: {response.status_code}")
    print("Response:")
    pprint(response.json())