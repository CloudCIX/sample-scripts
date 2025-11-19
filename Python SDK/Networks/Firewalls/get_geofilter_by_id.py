# File my_project/get_geofilter.py

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
geofilter_id = 123               # Change this to your geofilter ID

print(f"Retrieving geofilter {geofilter_id}...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Get Geo Firewall Details                     #
# ================================================================= #
response = Compute.network_firewalls.read(token=token, pk=geofilter_id)

if response.status_code == 200:
    firewall_data = response.json()
    
    if 'content' in firewall_data:
        firewall = firewall_data['content']
        
        print("Geofilter Details:")
        print("-" * 40)
        print(f"ID: {firewall.get('id', 'N/A')}")
        print(f"Name: {firewall.get('name', 'N/A')}")
        print(f"Type: {firewall.get('type', 'N/A')}")
        print(f"State: {firewall.get('state', 'N/A')}")
        print(f"Project ID: {firewall.get('project_id', 'N/A')}")
        print(f"Created: {firewall.get('created', 'N/A')}")
        print(f"Updated: {firewall.get('updated', 'N/A')}")
        print(f"URI: {firewall.get('uri', 'N/A')}")
        
        # Display geo filtering rules
        rules = firewall.get('rules', [])
        if rules:
            print(f"\nGeo Filtering Rules ({len(rules)}):")
            print("-" * 30)
            for i, rule in enumerate(rules, 1):
                action = "ALLOW" if rule.get('allow', False) else "BLOCK"
                direction = "INBOUND" if rule.get('inbound', True) else "OUTBOUND"
                group_name = rule.get('group_name', 'N/A')
                
                print(f"Rule {i}:")
                print(f"  Action: {action}")
                print(f"  Direction: {direction}")
                print(f"  Geo Group: {group_name}")
                
                # Parse country from group name
                if '@' in group_name:
                    country_code = group_name.replace('@', '').replace('_v4', '').replace('_v6', '')
                    ip_version = 'IPv6' if '_v6' in group_name else 'IPv4'
                    print(f"  Country: {country_code} ({ip_version})")
                
                if i < len(rules):
                    print()
        else:
            print(f"\nGeo Filtering Rules: No rules configured")
        
        # Display specs if available
        specs = firewall.get('specs', [])
        if specs:
            print(f"\nSpecifications ({len(specs)}):")
            print("-" * 30)
            for i, spec in enumerate(specs, 1):
                print(f"  {spec.get('sku_name', 'N/A')}: {spec.get('quantity', 'N/A')}")
        else:
            print(f"\nSpecifications: Default firewall configuration")
            
elif response.status_code == 404:
    print(f"Geofilter with ID {geofilter_id} not found.")
    print("Please check the firewall ID and try again.")
    
elif response.status_code == 403:
    print(f"Permission denied for geofilter {geofilter_id}.")
    print("You may not have access to this firewall or it may belong to a different project.")
    
else:
    print(f"Error retrieving geofilter: {response.status_code}")
    print("Response:")
    try:
        pprint(response.json())
    except:
        print(response.text)