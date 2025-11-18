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
firewall_id = 123

response = Compute.network_firewalls.read(token=token, pk=firewall_id)

if response.status_code == 200:
    firewall = response.json()['content']
    
    print(f"Firewall Details for ID: {firewall_id}")
    print("=" * 50)
    print(f"Name: {firewall.get('name', 'N/A')}")
    print(f"Type: {firewall.get('type', 'N/A')}")
    print(f"Project ID: {firewall.get('project_id', 'N/A')}")
    print(f"State: {firewall.get('state', 'N/A')}")
    print(f"Created: {firewall.get('created', 'N/A')}")
    print(f"Updated: {firewall.get('updated', 'N/A')}")
    
    print("\nRules:")
    print("-" * 30)
    rules = firewall.get('rules', [])
    if rules:
        for i, rule in enumerate(rules, 1):
            print(f"Rule {i}:")
            print(f"  Description: {rule.get('description', 'N/A')}")
            print(f"  Allow: {rule.get('allow', 'N/A')}")
            print(f"  Direction: {'Inbound' if rule.get('inbound') else 'Outbound'}")
            print(f"  Protocol: {rule.get('protocol', 'N/A')}")
            print(f"  Port: {rule.get('port', 'N/A')}")
            print(f"  Source: {rule.get('source', 'N/A')}")
            print(f"  Destination: {rule.get('destination', 'N/A')}")
            print()
    else:
        print("  No rules configured")
    
    print("\nComplete JSON Response:")
    print("-" * 50)
    pprint(firewall)
    
elif response.status_code == 404:
    print(f"Firewall with ID {firewall_id} not found")
elif response.status_code == 403:
    print("Permission denied - you don't have access to this firewall")
else:
    print(f"Error {response.status_code}: {response.text}")