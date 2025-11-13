# File my_project/get_router_by_id.py

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
router_id = 123                 # Change this to the router ID you want to retrieve

print(f"Retrieving router {router_id}...")
print("\n" + "="*50 + "\n")

# ================================================================= #
#                      Get Router by ID                             #
# ================================================================= #
response = Compute.network_routers.read(token=token, pk=router_id)

if response.status_code == 200:
    router_data = response.json()
    
    # Print full response first
    print("Complete router response:")
    pprint(router_data)
    print("\n" + "="*50 + "\n")
    
    # Extract and display router details
    if 'content' in router_data:
        router = router_data['content']
        
        print("Router Details:")
        print("-" * 40)
        print(f"ID: {router.get('id', 'N/A')}")
        print(f"Name: {router.get('name', 'N/A')}")
        print(f"Type: {router.get('type', 'N/A')}")
        print(f"State: {router.get('state', 'N/A')}")
        print(f"Project ID: {router.get('project_id', 'N/A')}")
        print(f"Grace Period: {router.get('grace_period', 'N/A')}")
        print(f"Created: {router.get('created', 'N/A')}")
        print(f"Updated: {router.get('updated', 'N/A')}")
        print(f"URI: {router.get('uri', 'N/A')}")
        
        # Display metadata if available
        metadata = router.get('metadata', {})
        if metadata:
            print(f"\nMetadata:")
            print("-" * 20)
            
            # IPv4 Address details
            ipv4_address = metadata.get('ipv4_address')
            ipv4_address_id = metadata.get('ipv4_address_id')
            if ipv4_address or ipv4_address_id:
                print("IPv4 Configuration:")
                if ipv4_address_id:
                    print(f"  IPv4 Address ID: {ipv4_address_id}")
                if ipv4_address:
                    print(f"  IPv4 Address Details:")
                    print(f"    ID: {ipv4_address.get('id', 'N/A')}")
                    print(f"    Address: {ipv4_address.get('address', 'N/A')}")
                    print(f"    Name: {ipv4_address.get('name', 'N/A')}")
                    print(f"    Notes: {ipv4_address.get('notes', 'N/A')}")
                    print(f"    Subnet ID: {ipv4_address.get('subnet_id', 'N/A')}")
                    print(f"    Public IP ID: {ipv4_address.get('public_ip_id', 'N/A')}")
                    
                    public_ip = ipv4_address.get('public_ip')
                    if public_ip:
                        print(f"    Public IP:")
                        print(f"      ID: {public_ip.get('id', 'N/A')}")
                        print(f"      Address: {public_ip.get('address', 'N/A')}")
                    
                    print(f"    Created: {ipv4_address.get('created', 'N/A')}")
                    print(f"    Updated: {ipv4_address.get('updated', 'N/A')}")
                print()
            
            # IPv6 Address details
            ipv6_address = metadata.get('ipv6_address')
            ipv6_address_id = metadata.get('ipv6_address_id')
            if ipv6_address or ipv6_address_id:
                print("IPv6 Configuration:")
                if ipv6_address_id:
                    print(f"  IPv6 Address ID: {ipv6_address_id}")
                if ipv6_address:
                    print(f"  IPv6 Address Details:")
                    print(f"    ID: {ipv6_address.get('id', 'N/A')}")
                    print(f"    Address: {ipv6_address.get('address', 'N/A')}")
                    print(f"    Name: {ipv6_address.get('name', 'N/A')}")
                    print(f"    Notes: {ipv6_address.get('notes', 'N/A')}")
                    print(f"    Subnet ID: {ipv6_address.get('subnet_id', 'N/A')}")
                    print(f"    Public IP ID: {ipv6_address.get('public_ip_id', 'N/A')}")
                    
                    public_ip = ipv6_address.get('public_ip')
                    if public_ip:
                        print(f"    Public IP:")
                        print(f"      ID: {public_ip.get('id', 'N/A')}")
                        print(f"      Address: {public_ip.get('address', 'N/A')}")
                    
                    print(f"    Created: {ipv6_address.get('created', 'N/A')}")
                    print(f"    Updated: {ipv6_address.get('updated', 'N/A')}")
                print()
            
            # Show any other metadata fields
            other_metadata = {k: v for k, v in metadata.items() 
                            if k not in ['ipv4_address', 'ipv4_address_id', 'ipv6_address', 'ipv6_address_id']}
            if other_metadata:
                print("Other Metadata:")
                pprint(other_metadata)
                print()
        else:
            print(f"\nMetadata: None")
        
        # Display networks if available
        networks = router.get('networks', [])
        if networks:
            print(f"\nNetworks ({len(networks)}):")
            print("-" * 30)
            for i, network in enumerate(networks, 1):
                print(f"Network {i}:")
                print(f"  Name: {network.get('name', 'N/A')}")
                print(f"  IPv4: {network.get('ipv4', 'N/A')}")
                print(f"  IPv6: {network.get('ipv6', 'N/A')}")
                print(f"  Destination: {network.get('destination', 'N/A')}")
                print(f"  Next Hop: {network.get('nexthop', 'N/A')}")
                print(f"  VLAN: {network.get('vlan', 'N/A')}")
                print(f"  NAT: {network.get('nat', 'N/A')}")
                print()
        else:
            print(f"\nNetworks: No networks configured")
        
        # Display specs if available
        specs = router.get('specs', [])
        if specs:
            print(f"Specifications ({len(specs)}):")
            print("-" * 30)
            for i, spec in enumerate(specs, 1):
                print(f"Spec {i}:")
                print(f"  SKU Name: {spec.get('sku_name', 'N/A')}")
                print(f"  Quantity: {spec.get('quantity', 'N/A')}")
                print()
        else:
            print(f"Specifications: No specs defined")
            
elif response.status_code == 404:
    print(f"Router with ID {router_id} not found.")
    print("Please check the router ID and try again.")
    
elif response.status_code == 403:
    print(f"Permission denied for router {router_id}.")
    print("You may not have access to this router or it may belong to a different project.")
    
else:
    print(f"Error retrieving router: {response.status_code}")
    print("Response:")
    try:
        pprint(response.json())
    except:
        print(response.text)