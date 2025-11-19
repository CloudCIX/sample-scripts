import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      Update Geofilter                             #
# ================================================================= #
geofilter_id = 123  # Change this to the geofilter ID you want to update

# First, get the current geofilter details
response = Compute.network_firewalls.read(token=token, pk=geofilter_id)

if response.status_code == 200:
    current_geofilter = response.json()['content']
    print("Current geofilter details:")
    print(f"Name: {current_geofilter.get('name')}")
    print(f"Type: {current_geofilter.get('type')}")
    print(f"Current rules: {len(current_geofilter.get('rules', []))}")
    print("-" * 40)
    
    # Updated geofilter data NOTE: When this will replace existing rules, so include all desired rules here.
    update_data = {
        'name': 'Updated Geo Firewall',  # Change this to your new name
        'rules': [                       # Updated geographic filtering rules
        {
            'allow': False,        # Block traffic from US (IPv4)
            'group_name': '@US_v4',
            'inbound': True
        },
        {
            'allow': False,        # Block traffic from US (IPv6)
            'group_name': '@US_v6',
            'inbound': True
        }
        ],
        'state': 'update_running'  # Required for updates
    }
    
    # Update the geofilter
    update_response = Compute.network_firewalls.partial_update(
        token=token, 
        pk=geofilter_id, 
        data=update_data
    )
    
    if update_response.status_code == 202:
        print("Geofilter update initiated successfully!")
        print("Response:")
        pprint(update_response.json())
    else:
        print(f"Error updating geofilter: {update_response.status_code}")
        pprint(update_response.json())
        
elif response.status_code == 404:
    print(f"Geofilter with ID {geofilter_id} not found")
elif response.status_code == 403:
    print("Permission denied - you don't have access to this geofilter")
else:
    print(f"Error getting geofilter details: {response.status_code}")
    print(response.text)