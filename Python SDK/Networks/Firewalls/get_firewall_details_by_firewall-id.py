import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token
from pprint import pprint

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      Get Firewall Details                         #
# ================================================================= #
firewall_id = 170

response = Compute.network_firewalls.read(token=token, pk=firewall_id)

if response.status_code == 200:
    firewall = response.json()['content']
    
    print(f"Firewall: {firewall.get('name', 'N/A')} (ID: {firewall_id})")
    print(f"State: {firewall.get('state', 'N/A')} | Project: {firewall.get('project_id', 'N/A')}")
    
    rules = firewall.get('rules', [])
    if rules:
        print(f"\nRules ({len(rules)}):")
        for i, rule in enumerate(rules, 1):
            direction = 'In' if rule.get('inbound') else 'Out'
            action = 'Allow' if rule.get('allow') else 'Block'
            source = rule.get('source', 'Any')
            destination = rule.get('destination', 'Any')
            protocol = rule.get('protocol', 'Any')
            port = rule.get('port', '')
            
            port_info = f":{port}" if port and port != '' else ""
            print(f"  {i}. {direction} {action} | {source} → {destination} | {protocol}{port_info}")
    else:
        print("\nRules: None")
    
elif response.status_code == 404:
    print(f"Firewall with ID {firewall_id} not found")
elif response.status_code == 403:
    print("Permission denied - you don't have access to this firewall")
else:
    print(f"Error {response.status_code}: {response.text}")