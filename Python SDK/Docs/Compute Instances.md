# Compute Instances

### `Compute.compute_instances`

CloudCIX supports two different instance types:

1. **LXD Virtual Machine / Containers** - Virtual machines and containers running on LXD (Linux distributions)
2. **Hyper-V Virtual Machines** - Virtual machines running on Hyper-V hypervisor (Windows distributions)

#### Create LXD Virtual Machine (Ubuntu 24.04)

```python
lxd_vm_data = {
    'project_id': 123, # Your Project ID
    'name': 'ubuntu-vm', # The name of your instance
    'type': 'lxd', # Can be lxd or hyperv
    'grace_period': 72, # Grace period in hours before delete request to final deletion
    'metadata': {
        'instance_type': 'virtual-machine',  # virtual-machine' for VMs, 'container' for containers
        'dns': '8.8.8.8,8.8.4.4,2001:4860:4860::8888,2001:4860:4860::8844',  # IPv4 and IPv6 DNS
        'userdata': "#cloud-config\nusers:\n  - name: administrator\n    groups: sudo\n    shell: /bin/bash\n    lock_passwd: false\n    passwd: <YOUR PASSWORD HASH>\n    ssh_authorized_keys:\n      - ssh-ed25519 <YOUR PUBLIC SSH KEY>\nchpasswd:\n  expire: false\nssh_pwauth: true\n"
    }, # Your User Data for cloud-init
    'interfaces': [
        {
            'gateway': True, # Set to True for primary interface
            'ipv4_addresses': [
                {
                    'address': '10.0.1.10', # Static IPv4 address
                    'nat': True     # Enable NAT for external access
                }
            ],
            'ipv6_addresses': [
                {
                    'address': '2a02:2078:9:1234::10' # Static IPv6 address
                }
            ]
        }
    ],
    'specs': [
        {'quantity': 4, 'sku_name': 'RAM_001'},      # 4GB RAM
        {'quantity': 2, 'sku_name': 'vCPU_001'},     # 2 CPU cores
        {'quantity': 50, 'sku_name': 'SSD_001'},     # 50GB SSD 
        {'quantity': 1, 'sku_name': 'UBUNTU2404'}    # Ubuntu 24.04 see Images endpoint for full list
    ]
}
response = Compute.compute_instances.create(token=token, data=lxd_vm_data)
```

#### Create LXD Container (Ubuntu)

```python
lxd_container_data = {
    'project_id': 123,
    'name': 'ubuntu-container',
    'type': 'lxd',
    'grace_period': 72,
    'metadata': {
        'instance_type': 'container',
        'dns': '8.8.8.8,8.8.4.4,2001:4860:4860::8888,2001:4860:4860::8844',  # IPv4 and IPv6 DNS
        'userdata': "#cloud-config\nusers:\n  - name: administrator\n    groups: sudo\n    shell: /bin/bash\n    lock_passwd: false\n    passwd: $2a$12$GcOZ6Mh4GFyxABIhhDAt/eHk6mp1fXwOeyg0tPFLbTERhcFnxUR7.\n    ssh_authorized_keys:\n      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEc5NwoYuL3x0JFL0TLCutzcNl0Gpv3L8oPg57pTu6BI\nchpasswd:\n  expire: false\nssh_pwauth: true\n"
    },
    'interfaces': [
        {
            'gateway': True,
            'ipv4_addresses': [
                {
                    'address': '10.0.1.11',
                    'nat': True
                }
            ],
            'ipv6_addresses': [
                {
                    'address': '2a02:2078:9:1234::11'
                }
            ]
        }
    ],
    'specs': [
        {'quantity': 2, 'sku_name': 'RAM_001'},      # 2GB RAM
        {'quantity': 1, 'sku_name': 'vCPU_001'},     # 1 CPU core
        {'quantity': 20, 'sku_name': 'SSD_001'},     # 20GB SSD
        {'quantity': 1, 'sku_name': 'UBUNTU2404'}    # Ubuntu 24.04
    ]
}
response = Compute.compute_instances.create(token=token, data=lxd_container_data)
```

#### Create Hyper-V Virtual Machine (Windows)

```python
hyperv_vm_data = {
    'project_id': 123,
    'name': 'windows-server',
    'type': 'hyperv',
    'grace_period': 72,
    'metadata': {
        'dns4': '8.8.8.8',                          # IPv4 DNS (separate fields for Hyper-V)
        'dns6': '2001:4860:4860::8888',             # IPv6 DNS
        'email': 'admin@example.com'                # Required for Windows license
    },
    'interfaces': [
        {
            'gateway': True,
            'ipv4_addresses': [
                {
                    'address': '10.0.1.20',
                    'nat': True
                }
            ],
            'ipv6_addresses': [
                {
                    'address': '2a02:2078:9:1234::20'
                }
            ]
        }
    ],
    'specs': [
        {'quantity': 8, 'sku_name': 'RAM_001'},      # 8GB RAM
        {'quantity': 4, 'sku_name': 'vCPU_002'},     # 4 CPU cores (vCPU_002 for Hyper-V)
        {'quantity': 100, 'sku_name': 'SSD_001'},    # 100GB SSD
        {'quantity': 1, 'sku_name': 'MSServer2022'}  # Windows Server 2022
    ]
}
response = Compute.compute_instances.create(token=token, data=hyperv_vm_data)
```

**Key Differences:**

| Feature | LXD VM | LXD Container | Hyper-V VM |
|---------|---------|---------------|-------------|
| `type` | `'lxd'` | `'lxd'` | `'hyperv'` |
| `instance_type` | `'virtual-machine'` | `'container'` | Not used |
| DNS config | `dns` (combined) | `dns` (combined) | `dns4` + `dns6` (separate) |
| vCPU SKU | `vCPU_001` | `vCPU_001` | `vCPU_002` |
| OS Images | Linux distros | Linux distros | Windows editions |
| Email required | No | No | Yes (license) |
| Cloud-init | Yes (userdata) | Yes (userdata) | No |

#### List Instances
```python
params = {
    'limit': 50,
    'page': 0,
    'search[project_id]': 123,
    'order': '-created'
}
response = Compute.compute_instances.list(token=token, params=params)
```

#### Read Instance Details
```python
instance_id = 1001
response = Compute.compute_instances.read(token=token, pk=instance_id)
```

#### Update Instance
```python
# Update instance name only
update_data = {
    'name': 'Updated Instance Name',
    'state': 'update_running',
}
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data=update_data)

# Update instance specs (upgrade RAM and CPU)
upgrade_data = {
    'specs': [
        {'quantity': 16, 'sku_name': 'RAM_001'},     # Upgrade to 16GB RAM
        {'quantity': 8, 'sku_name': 'vCPU_001'},     # Upgrade to 8 CPU cores
        {'quantity': 200, 'sku_name': 'SSD_001'},    # Upgrade to 200GB SSD
    ],
    'state': 'update_running'
}
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data=upgrade_data)
```

#### Stop Instance
```python
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data={'state': 'stop'})
```

#### Restart Instance
```python
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data={'state': 'restart'})
```

#### Delete Instance
```python
response = Compute.compute_instances.partial_update(token=token, pk=instance_id, data={'state': 'delete'})
```

---