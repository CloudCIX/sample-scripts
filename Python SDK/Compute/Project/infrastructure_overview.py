# File my_project/infrastructure_overview.py

import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# Configuration
project_id = 123  # Your project ID to filter resources

print(f"Complete Infrastructure Overview for Project {project_id}")
print("=" * 70)

# ================================================================= #
#                      Project Information                          #
# ================================================================= #
print("\n🏢 PROJECT DETAILS")
print("-" * 30)
project_response = Compute.project.read(token=token, pk=project_id)
if project_response.status_code == 200:
    project = project_response.json()['content']
    print(f"Name: {project.get('name', 'N/A')}")
    print(f"Region ID: {project.get('region_id', 'N/A')}")
    print(f"Address ID: {project.get('address_id', 'N/A')}")
    print(f"Manager ID: {project.get('manager_id', 'N/A')}")
    print(f"Reseller ID: {project.get('reseller_id', 'N/A')}")
    print(f"Created: {project.get('created', 'N/A')}")
    print(f"Updated: {project.get('updated', 'N/A')}")
    print(f"Status: {'Closed' if project.get('closed', False) else 'Active'}")
    print(f"Notes: {project.get('note', 'N/A')}")
else:
    print(f"❌ Failed to retrieve project: {project_response.status_code}")

# ================================================================= #
#                      Network Infrastructure                       #
# ================================================================= #
print("\n🌐 NETWORK INFRASTRUCTURE")
print("-" * 40)

# Get Network Routers (both router and static_route types)
print("📡 Network Routers:")
router_response = Compute.network_routers.list(token=token, params={'search[project_id]': project_id})
if router_response.status_code == 200:
    routers = router_response.json()['content']
    if routers:
        for router in routers:
            # Get detailed router info
            detailed_response = Compute.network_routers.read(token=token, pk=router.get('id'))
            if detailed_response.status_code == 200:
                detailed_router = detailed_response.json()['content']
                
                print(f"  └─ {router.get('name', 'N/A')} (ID: {router.get('id')})")
                print(f"     Type: {detailed_router.get('type', 'Unknown')}")
                print(f"     State: {router.get('state', 'N/A')}")
                print(f"     Grace Period: {detailed_router.get('grace_period', 'N/A')} days")
                
                # Show router metadata (public IPs)
                metadata = detailed_router.get('metadata', {})
                if metadata:
                    ipv4_addr = metadata.get('ipv4_address', {})
                    ipv6_addr = metadata.get('ipv6_address', {})
                    if ipv4_addr:
                        print(f"     Public IPv4: {ipv4_addr.get('address', 'N/A')}")
                    if ipv6_addr:
                        print(f"     Public IPv6: {ipv6_addr.get('address', 'N/A')}")
                
                # Show networks for router type
                if detailed_router.get('type') == 'router':
                    networks = detailed_router.get('networks', [])
                    if networks:
                        print(f"     Networks ({len(networks)}):")
                        for net in networks:
                            print(f"       • {net.get('name', 'N/A')}: {net.get('ipv4', 'N/A')} (VLAN: {net.get('vlan', 'N/A')})")
                            if net.get('ipv6'):
                                print(f"         IPv6: {net.get('ipv6')}")
                    else:
                        print("       No networks configured")
                
                # Show static route details
                elif detailed_router.get('type') == 'static_route':
                    static_metadata = detailed_router.get('metadata', {})
                    print(f"     Destination: {static_metadata.get('destination', 'N/A')}")
                    print(f"     Next Hop: {static_metadata.get('nexthop', 'N/A')}")
                    print(f"     NAT Enabled: {static_metadata.get('nat', False)}")
            else:
                # Fallback
                print(f"  └─ {router.get('name', 'N/A')} (ID: {router.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {router.get('state', 'N/A')}")
    else:
        print("  ❌ No routers found")
else:
    print(f"  ❌ Failed to get routers: {router_response.status_code}")

# Get Network Firewalls
print("\n🔥 Network Firewalls:")
firewall_response = Compute.network_firewalls.list(token=token, params={'search[project_id]': project_id})
if firewall_response.status_code == 200:
    firewalls = firewall_response.json()['content']
    if firewalls:
        for firewall in firewalls:
            # Get detailed firewall info
            detailed_response = Compute.network_firewalls.read(token=token, pk=firewall.get('id'))
            if detailed_response.status_code == 200:
                detailed_firewall = detailed_response.json()['content']
                
                print(f"  └─ {firewall.get('name', 'N/A')} (ID: {firewall.get('id')})")
                print(f"     Type: {detailed_firewall.get('type', 'Unknown')}")
                print(f"     State: {firewall.get('state', 'N/A')}")
                
                rules = detailed_firewall.get('rules', [])
                print(f"     Rules ({len(rules)}):")
                for i, rule in enumerate(rules[:3]):  # Show first 3 rules
                    direction = "Inbound" if rule.get('inbound', False) else "Outbound"
                    action = "ALLOW" if rule.get('allow', False) else "DENY"
                    if detailed_firewall.get('type') == 'project':
                        print(f"       {i+1}. {direction} {action}: {rule.get('source', 'N/A')} → {rule.get('destination', 'N/A')} ({rule.get('protocol', 'N/A')}:{rule.get('port', 'N/A')})")
                    else:  # geo firewall
                        print(f"       {i+1}. {direction} {action}: Group {rule.get('group_name', 'N/A')}")
                if len(rules) > 3:
                    print(f"       ... and {len(rules) - 3} more rules")
            else:
                # Fallback
                print(f"  └─ {firewall.get('name', 'N/A')} (ID: {firewall.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {firewall.get('state', 'N/A')}")
    else:
        print("  ❌ No firewalls found")
else:
    print(f"  ❌ Failed to get firewalls: {firewall_response.status_code}")

# Get Network VPNs
print("\n🔒 Network VPNs:")
vpn_response = Compute.network_vpns.list(token=token, params={'search[project_id]': project_id})
if vpn_response.status_code == 200:
    vpns = vpn_response.json()['content']
    if vpns:
        for vpn in vpns:
            # Get detailed VPN info
            detailed_response = Compute.network_vpns.read(token=token, pk=vpn.get('id'))
            if detailed_response.status_code == 200:
                detailed_vpn = detailed_response.json()['content']
                
                print(f"  └─ {vpn.get('name', 'N/A')} (ID: {vpn.get('id')})")
                print(f"     Type: {detailed_vpn.get('type', 'Unknown')}")
                print(f"     State: {vpn.get('state', 'N/A')}")
                
                # Show VPN metadata
                metadata = detailed_vpn.get('metadata', {})
                if metadata:
                    print(f"     Gateway: {metadata.get('ike_gateway_value', 'N/A')} ({metadata.get('ike_gateway_type', 'N/A')})")
                    print(f"     IKE Version: {metadata.get('ike_version', 'N/A')}")
                    
                    child_sas = metadata.get('child_sas', [])
                    if child_sas:
                        print(f"     Routes ({len(child_sas)}):")
                        for sa in child_sas:
                            print(f"       • {sa.get('local_ts', 'N/A')} ↔ {sa.get('remote_ts', 'N/A')}")
            else:
                # Fallback
                print(f"  └─ {vpn.get('name', 'N/A')} (ID: {vpn.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {vpn.get('state', 'N/A')}")
    else:
        print("  ❌ No VPNs found")
else:
    print(f"  ❌ Failed to get VPNs: {vpn_response.status_code}")

# ================================================================= #
#                      Compute Resources                            #
# ================================================================= #
print("\n💻 COMPUTE RESOURCES")
print("-" * 40)

# Get Compute Instances
print("🖥️  Compute Instances:")
instance_response = Compute.compute_instances.list(token=token, params={'search[project_id]': project_id})
if instance_response.status_code == 200:
    instances = instance_response.json()['content']
    if instances:
        for instance in instances:
            # Get detailed instance info to show type and metadata
            detailed_response = Compute.compute_instances.read(token=token, pk=instance.get('id'))
            if detailed_response.status_code == 200:
                detailed_instance = detailed_response.json()['content']
                
                print(f"  └─ {instance.get('name', 'N/A')} (ID: {instance.get('id')})")
                print(f"     Type: {detailed_instance.get('type', 'Unknown')}")
                print(f"     State: {instance.get('state', 'N/A')}")
                print(f"     Grace Period: {instance.get('grace_period', 'N/A')} days")
                print(f"     Created: {instance.get('created', 'N/A')}")
                
                # Show instance metadata
                metadata = detailed_instance.get('metadata', {})
                if metadata.get('instance_type'):
                    print(f"     Instance Type: {metadata.get('instance_type')}")
                if metadata.get('dns'):
                    print(f"     DNS: {metadata.get('dns')}")
                
                # Show network interfaces
                interfaces = metadata.get('interfaces', [])
                if interfaces:
                    print(f"     Network Interfaces ({len(interfaces)}):")
                    for i, iface in enumerate(interfaces):
                        gateway_marker = " (Gateway)" if iface.get('gateway', False) else ""
                        print(f"       Interface {i+1}{gateway_marker}:")
                        print(f"         MAC: {iface.get('mac_address', 'N/A')}")
                        print(f"         VLAN: {iface.get('vlan', 'N/A')}")
                        
                        ipv4_addrs = iface.get('ipv4_addresses', [])
                        for addr in ipv4_addrs:
                            nat_info = f" (NAT: {addr.get('public_ip', 'N/A')})" if addr.get('nat', False) else ""
                            print(f"         IPv4: {addr.get('address', 'N/A')}{nat_info}")
                        
                        ipv6_addrs = iface.get('ipv6_addresses', [])
                        for addr in ipv6_addrs:
                            print(f"         IPv6: {addr.get('address', 'N/A')}")
            else:
                # Fallback to basic info if detailed call fails
                print(f"  └─ {instance.get('name', 'N/A')} (ID: {instance.get('id')})")
                print(f"     Type: Unknown (Resource Type ID: {instance.get('resource_type_id', 'N/A')})")
                print(f"     State: {instance.get('state', 'N/A')}")
                print(f"     Grace Period: {instance.get('grace_period', 'N/A')} days")
                print(f"     Created: {instance.get('created', 'N/A')}")
    else:
        print("  ❌ No compute instances found")
else:
    print(f"  ❌ Failed to get instances: {instance_response.status_code}")

# Get Compute GPUs
print("\n🎮 Compute GPUs:")
gpu_response = Compute.compute_gpus.list(token=token, params={'search[project_id]': project_id})
if gpu_response.status_code == 200:
    gpus = gpu_response.json()['content']
    if gpus:
        for gpu in gpus:
            # Get detailed GPU info
            detailed_response = Compute.compute_gpus.read(token=token, pk=gpu.get('id'))
            if detailed_response.status_code == 200:
                detailed_gpu = detailed_response.json()['content']
                
                print(f"  └─ {gpu.get('name', 'N/A')} (ID: {gpu.get('id')})")
                print(f"     State: {gpu.get('state', 'N/A')}")
                print(f"     Attached to Instance: {detailed_gpu.get('instance', {}).get('name', 'N/A')} (ID: {detailed_gpu.get('instance', {}).get('id', 'N/A')})")
                
                # Show GPU specs
                specs = detailed_gpu.get('specs', [])
                if specs:
                    print(f"     Specifications:")
                    for spec in specs:
                        print(f"       • {spec.get('sku_name', 'N/A')}: {spec.get('quantity', 'N/A')}")
            else:
                # Fallback
                print(f"  └─ {gpu.get('name', 'N/A')} (ID: {gpu.get('id')})")
                print(f"     State: {gpu.get('state', 'N/A')}")
    else:
        print("  ❌ No GPUs found")
else:
    print(f"  ❌ Failed to get GPUs: {gpu_response.status_code}")

# ================================================================= #
#                      Storage Resources                            #
# ================================================================= #
print("\n💾 STORAGE RESOURCES")
print("-" * 40)

# Get Storage Volumes
print("🗄️  Storage Volumes:")
volume_response = Compute.storage_volumes.list(token=token, params={'search[project_id]': project_id})
if volume_response.status_code == 200:
    volumes = volume_response.json()['content']
    if volumes:
        for volume in volumes:
            # Get detailed volume info
            detailed_response = Compute.storage_volumes.read(token=token, pk=volume.get('id'))
            if detailed_response.status_code == 200:
                detailed_volume = detailed_response.json()['content']
                
                print(f"  └─ {volume.get('name', 'N/A')} (ID: {volume.get('id')})")
                print(f"     Type: {detailed_volume.get('type', 'Unknown')}")
                print(f"     State: {volume.get('state', 'N/A')}")
                
                # Show volume specs
                specs = detailed_volume.get('specs', [])
                if specs:
                    total_capacity = sum(spec.get('quantity', 0) for spec in specs)
                    print(f"     Capacity: {total_capacity} GB")
                    for spec in specs:
                        print(f"       • {spec.get('sku_name', 'N/A')}: {spec.get('quantity', 'N/A')} GB")
                
                # Show attachment details based on type
                if detailed_volume.get('type') == 'cephfs':
                    metadata = detailed_volume.get('metadata', {})
                    attached_ids = metadata.get('attach_instance_ids', [])
                    detached_ids = metadata.get('detach_instance_ids', [])
                    mount_path = metadata.get('mount_path', 'N/A')
                    
                    print(f"     Mount Path: {mount_path}")
                    if attached_ids:
                        print(f"     Attached to instances: {attached_ids}")
                    if detached_ids:
                        print(f"     Detaching from instances: {detached_ids}")
                    if not attached_ids and not detached_ids:
                        print("     Not attached to any instances")
                        
                elif detailed_volume.get('type') == 'hyperv':
                    instance_info = detailed_volume.get('instance', {})
                    if instance_info:
                        print(f"     Attached to: {instance_info.get('name', 'N/A')} (ID: {instance_info.get('id', 'N/A')})")
                    else:
                        print("     Not attached to any instance")
                        
                # Show contra_instances (additional attachment info)
                contra_instances = detailed_volume.get('contra_instances', [])
                if contra_instances:
                    print(f"     Contra Instances ({len(contra_instances)}):")
                    for inst in contra_instances:
                        print(f"       • {inst.get('name', 'N/A')} (ID: {inst.get('id')}) - State: {inst.get('state', 'N/A')}")
            else:
                # Fallback
                print(f"  └─ {volume.get('name', 'N/A')} (ID: {volume.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {volume.get('state', 'N/A')}")
    else:
        print("  ❌ No storage volumes found")
else:
    print(f"  ❌ Failed to get volumes: {volume_response.status_code}")

# ================================================================= #
#                      Backup & Snapshot Resources                  #
# ================================================================= #
print("\n💿 BACKUP & SNAPSHOT RESOURCES")
print("-" * 40)

# Get Compute Backups
print("💾 Compute Backups:")
backup_response = Compute.compute_backups.list(token=token, params={'search[project_id]': project_id})
if backup_response.status_code == 200:
    backups = backup_response.json()['content']
    if backups:
        for backup in backups:
            # Get detailed backup info
            detailed_response = Compute.compute_backups.read(token=token, pk=backup.get('id'))
            if detailed_response.status_code == 200:
                detailed_backup = detailed_response.json()['content']
                
                print(f"  └─ {backup.get('name', 'N/A')} (ID: {backup.get('id')})")
                print(f"     Type: {detailed_backup.get('type', 'Unknown')}")
                print(f"     State: {backup.get('state', 'N/A')}")
                print(f"     Created: {backup.get('created', 'N/A')}")
                
                instance_info = detailed_backup.get('instance', {})
                if instance_info:
                    print(f"     Source Instance: {instance_info.get('name', 'N/A')} (ID: {instance_info.get('id', 'N/A')})")
            else:
                # Fallback
                print(f"  └─ {backup.get('name', 'N/A')} (ID: {backup.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {backup.get('state', 'N/A')}")
                print(f"     Created: {backup.get('created', 'N/A')}")
    else:
        print("  ❌ No backups found")
else:
    print(f"  ❌ Failed to get backups: {backup_response.status_code}")

# Get Compute Snapshots
print("\n📸 Compute Snapshots:")
snapshot_response = Compute.compute_snapshots.list(token=token, params={'search[project_id]': project_id})
if snapshot_response.status_code == 200:
    snapshots = snapshot_response.json()['content']
    if snapshots:
        for snapshot in snapshots:
            # Get detailed snapshot info
            detailed_response = Compute.compute_snapshots.read(token=token, pk=snapshot.get('id'))
            if detailed_response.status_code == 200:
                detailed_snapshot = detailed_response.json()['content']
                
                print(f"  └─ {snapshot.get('name', 'N/A')} (ID: {snapshot.get('id')})")
                print(f"     Type: {detailed_snapshot.get('type', 'Unknown')}")
                print(f"     State: {snapshot.get('state', 'N/A')}")
                print(f"     Created: {snapshot.get('created', 'N/A')}")
                
                instance_info = detailed_snapshot.get('instance', {})
                if instance_info:
                    print(f"     Source Instance: {instance_info.get('name', 'N/A')} (ID: {instance_info.get('id', 'N/A')})")
                    
                # Show HyperV snapshot metadata
                if detailed_snapshot.get('type') == 'hyperv':
                    metadata = detailed_snapshot.get('metadata', {})
                    if metadata:
                        print(f"     Active: {metadata.get('active', 'N/A')}")
                        print(f"     Remove Subtree: {metadata.get('remove_subtree', 'N/A')}")
            else:
                # Fallback
                print(f"  └─ {snapshot.get('name', 'N/A')} (ID: {snapshot.get('id')})")
                print(f"     Type: Unknown")
                print(f"     State: {snapshot.get('state', 'N/A')}")
                print(f"     Created: {snapshot.get('created', 'N/A')}")
    else:
        print("  ❌ No snapshots found")
else:
    print(f"  ❌ Failed to get snapshots: {snapshot_response.status_code}")

print(f"\n{'='*70}")
print("Complete infrastructure overview finished.")