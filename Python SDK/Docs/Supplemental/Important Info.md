## Important Notes

### State Management
CloudCIX uses a comprehensive state-based approach to resource lifecycle management:

**State Transition Rules:**
- Resources transition through defined states that trigger automated backend processing
- Unlike traditional REST APIs, CloudCIX uses state changes (not HTTP DELETE) for resource deletion
- State changes are requested via PUT/PATCH operations, not separate HTTP methods
- The system automatically handles intermediate states during processing

**Grace Period and Deletion:**
- When state is set to `'delete'`, resources enter `delete_queue` with a grace period
- Default grace period is 7 days (customizable per resource type)
- During grace period: resource is non-operational but can be restored via `'restart'`
- Billing stops immediately when deletion is requested
- After grace period: resource transitions to `'deleted'` and is permanently removed

**Resource Dependencies:**
Resources must be deleted in dependency order:
1. Compute instances, storage volumes, snapshots, backups, GPUs
2. Network firewalls, VPNs, IP groups
3. Network routers (must be last)
4. Projects (must be last and empty)

### API Endpoint Corrections

**Correct Endpoint Structure:**
```python
from cloudcix.api.compute import Compute

# Project management
Compute.project.*

# Network resources
Compute.network_routers.*
Compute.network_firewalls.*
Compute.network_vpns.*
Compute.network_ip_groups.*
Compute.nat_ip_addresses.*
Compute.base_ip_addresses.*

# Compute resources
Compute.compute_instances.*
Compute.compute_gpus.*
Compute.compute_snapshots.*
Compute.compute_backups.*

# Storage and images
Compute.storage_volumes.*
Compute.images.*
```

**HTTP Methods and Operations:**
- `GET` - List resources and read individual resource details
- `POST` - Create new resources
- `PUT/PATCH` - Update resource configuration or change state
- `DELETE` - Only used for IP Groups (`network_ip_groups.delete()`)

**Firewall Rule Management:**
- **CRITICAL:** Firewall rule updates replace the ENTIRE rule list
- To add rules: include ALL existing rules + new rules in update
- Missing rules in update request will be permanently deleted
- Each project limited to ONE project firewall and ONE geo firewall

**IP Group References:**
- Project firewalls: Use `@groupname` syntax (e.g., `"source": "@office-networks"`)
- Geo firewalls: Use `@groupname` syntax (e.g., `"group_name": "@IE_v4"`)
- Wildcard source/destination: Use `"*"` for any IP

### Authentication and Tokens
```python
from cloudcix.auth import get_admin_token

# Get authentication token
token = get_admin_token()

# All API calls require token
response = Compute.some_resource.some_method(token=token, data=data)
```

### Error Handling Best Practices
```python
def safe_api_call(api_method, *args, **kwargs):
    """Wrapper for CloudCIX API calls with comprehensive error handling"""
    try:
        response = api_method(*args, **kwargs)
        
        if response.status_code in [200, 201, 202]:
            return response.json().get('content')
        elif response.status_code == 204:
            return True  # Successful deletion
        elif response.status_code == 400:
            error_data = response.json()
            if 'errors' in error_data:
                for field, error in error_data['errors'].items():
                    print(f"Validation error in {field}: {error.get('detail')}")
            else:
                print(f"Request error: {error_data.get('detail')}")
            return None
        elif response.status_code == 401:
            print("Authentication failed - check your token")
            return None
        elif response.status_code == 403:
            print("Permission denied for this operation")
            return None
        elif response.status_code == 404:
            print("Resource not found")
            return None
        else:
            print(f"API error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return None

# Usage
result = safe_api_call(
    Compute.compute_instances.create,
    token=token,
    data=instance_data
)
if result:
    print(f"Instance created with ID: {result['id']}")
```

### Resource Specifications (SKUs)
Storage and compute resources use SKUs (Stock Keeping Units) for capacity specification:

**Common SKUs:**
- `RAM_001` - RAM for an instance
- `vCPU_001` - CPU core (LXD)
- `vCPU_002` - CPU core (Hyper-V)
- `SSD_001` - SSD storage
- `HDD_001` - HDD storage
- `CEPH_001` - Secondary Ceph storage HDD
- `CEPH_002` - Secondary Ceph storage SSD
- `UBUNTU2404` - Ubuntu 24.04 OS image
- `MSServer2022` - Windows Server 2022 OS image
- `A100_GPU` - NVIDIA A100 GPU

**SKU Usage:**
```python
specs = [
    {'quantity': 8, 'sku_name': 'RAM_001'},      # 8GB RAM
    {'quantity': 4, 'sku_name': 'vCPU_001'},     # 4 CPU cores
    {'quantity': 100, 'sku_name': 'SSD_001'},    # 100GB SSD
    {'quantity': 1, 'sku_name': 'UBUNTU2404'}    # Ubuntu 24.04 image
]
```

**Available SKUs vary by region - use the Images endpoint to discover available OS SKUs.**

[More information on SKUs can be found here including pricing details](https://www.cix.ie/#/services/cloud/public_cloud)
