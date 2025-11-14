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
#                      Update Firewall                              #
# ================================================================= #
firewall_id = 123  # Change this to the firewall ID you want to update

# First, get the current firewall details
response = Compute.network_firewalls.read(token=token, pk=firewall_id)

if response.status_code == 200:
    current_firewall = response.json()['content']
    print("Current firewall details:")
    print(f"Name: {current_firewall.get('name')}")
    print(f"Type: {current_firewall.get('type')}")
    print(f"Current rules: {len(current_firewall.get('rules', []))}")
    print("-" * 40)
    
    # Updated firewall data
    update_data = {
        'name': 'Updated Test Firewall',  # Change this to your new name
        'rules': [                        # Updated security rules NOTE: This will replace existing rules.
            {
                'allow': True,
                'description': 'Allow SSH from CIX OFFICE',
                'destination': '*',
                'inbound': True,
                'port': '22',
                'protocol': 'tcp',
                'source': '91.100.5.55'
            },
            {
                'allow': True,
                'description': 'Allow HTTP traffic',
                'destination': '10.0.1.0/24',
                'inbound': True,
                'port': '80',
                'protocol': 'tcp',
                'source': '*'
            },
            {
                'allow': True,
                'description': 'Allow HTTPS traffic',
                'destination': '10.0.1.0/24',
                'inbound': True,
                'port': '443',
                'protocol': 'tcp',
                'source': '*'
            }
        ],
        'state': 'update_running'  # Required for updates
    }
    
    # Update the firewall
    update_response = Compute.network_firewalls.partial_update(
        token=token, 
        pk=firewall_id, 
        data=update_data
    )
    
    if update_response.status_code == 202:
        print("Firewall update initiated successfully!")
        print("Response:")
        pprint(update_response.json())
    else:
        print(f"Error updating firewall: {update_response.status_code}")
        pprint(update_response.json())
        
elif response.status_code == 404:
    print(f"Firewall with ID {firewall_id} not found")
elif response.status_code == 403:
    print("Permission denied - you don't have access to this firewall")
else:
    print(f"Error getting firewall details: {response.status_code}")
    print(response.text)