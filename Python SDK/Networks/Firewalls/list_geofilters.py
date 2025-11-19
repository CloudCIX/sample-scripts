# File my_project/list_geofilters.py

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

# Configuration - set to None to list all projects, or specific project ID
project_id = None                  # Change this to your project ID, or set to None for all projects

if project_id:
    print(f"Listing geofilters for project {project_id}...")
else:
    print("Listing all geofilters...")

print("\n" + "="*60 + "\n")

# ================================================================= #
#                      List Geo Firewalls                           #
# ================================================================= #

# Set up filter parameters
params = {
    'limit': 50,
    'page': 0,
    'order': '-created',           # Sort by newest first
    'search[type]': 'geo',         # Only geo firewalls
}

# Add project filter if specified
if project_id:
    params['search[project_id]'] = project_id

response = Compute.network_firewalls.list(token=token, params=params)

if response.status_code == 200:
    firewalls_data = response.json()
    
    if 'content' in firewalls_data and firewalls_data['content']:
        geofilters = firewalls_data['content']
        
        print(f"Geofilter Summary: {len(geofilters)} geo firewalls found")
        print("=" * 60)
        
        for i, firewall in enumerate(geofilters, 1):
            print(f"{i}. ID: {firewall.get('id', 'N/A')} | Name: {firewall.get('name', 'N/A')}")
            print(f"   Project: {firewall.get('project_id', 'N/A')} | State: {firewall.get('state', 'N/A')}")
            
            # Show rule summary
            rules = firewall.get('rules', [])
            if rules:
                allow_rules = sum(1 for rule in rules if rule.get('allow', False))
                block_rules = len(rules) - allow_rules
                print(f"   Rules: {len(rules)} total ({allow_rules} allow, {block_rules} block)")
                
                # Show countries being filtered
                countries = set()
                for rule in rules:
                    group_name = rule.get('group_name', '')
                    if '@' in group_name:
                        country = group_name.replace('@', '').replace('_v4', '').replace('_v6', '')
                        countries.add(country)
                
                if countries:
                    country_list = ', '.join(sorted(countries))
                    print(f"   Countries: {country_list}")
            else:
                print(f"   Rules: No rules configured")
            
            print(f"   Created: {firewall.get('created', 'N/A')}")
            print(f"   URI: {firewall.get('uri', 'N/A')}")
            print("-" * 60)
    else:
        if project_id:
            print(f"No geo firewalls found for project {project_id}")
            print("This project may not have any geo firewalls configured.")
        else:
            print("No geo firewalls found in your account.")
            print("You may want to create one using the create_geofilter.py script.")
        
else:
    print(f"Error listing geofilters: {response.status_code}")
    print("Response:")
    try:
        pprint(response.json())
    except:
        print(response.text)