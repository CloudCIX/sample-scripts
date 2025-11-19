# Network Routers (VRFs)

### `Compute.network_routers`

Routers (VRFs) provide isolated network environments. CloudCIX supports two router types:

**Router Types:**
- **`router`** - Virtual router that manages IP forwarding and routing decisions for the project
- **`static_route`** - Maps a destination network to a nexthop IP for deterministic packet forwarding

#### Create Router/VRF
```python
# Create main project router (type defaults to 'router')
router_data = {
    'project_id': 123,
    'type': 'router',  # Optional - defaults to 'router'
    'name': 'Main Router',  # Optional - defaults to 'Router'
    'networks': [  # Optional - defaults to 10.0.0.1/24 if not specified
        {
            'name': 'Private Network 1',
            'ipv4': '10.0.1.0/24'  # Network CIDR, not gateway IP
        },
        {
            'name': 'Private Network 2', 
            'ipv4': '10.0.2.0/24'  # Network CIDR, not gateway IP
        }
    ]
}
response = Compute.network_routers.create(token=token, data=router_data)
```

#### Create static route

```python
static_route_data = {
    'project_id': 123,
    'type': 'static_route',
    'name': 'Office Route',  # Optional - defaults to 'Static Route'
    'metadata': {
        'destination': '192.168.1.0/24',  # Required for static_route
        'nexthop': '10.0.1.1',  # Required for static_route
        'nat': False  # Optional - defaults to False
    }
}
response = Compute.network_routers.create(token=token, data=static_route_data)
```

#### List Routers
```python
params = {
    'limit': 50,
    'page': 0,
    'search[project_id]': 123,  # Filter by project
    'search[type]': 'router'    # Filter by type ('router' or 'static_route')
}
response = Compute.network_routers.list(token=token, params=params)
```

#### Read Router Details
```python
router_id = 456
response = Compute.network_routers.read(token=token, pk=router_id)
```

#### Update Router
```python
# Update router name and add new network
update_data = {
    'name': 'Updated Router Name',
    'networks': [
        # Include existing networks with full details to preserve them
        {
            'name': 'Existing Network',
            'ipv4': '10.0.1.0/24',
            'ipv6': 'fd00:1::/64',
            'vlan': 100
        },
        # Add new network (only name and ipv4 needed)
        {
            'name': 'New Network',
            'ipv4': '10.0.3.0/24'
        }
    ],
    'state': 'update_running'  # Required for updates
}
response = Compute.network_routers.partial_update(token=token, pk=router_id, data=update_data)
```

#### Update static route

```python
static_route_update = {
    'name': 'Updated Route Name',
    'metadata': {
        'destination': '192.168.1.0/24',  # Cannot be changed
        'nexthop': '10.0.1.1',  # Cannot be changed 
        'nat': True  # Can be updated
    },
    'state': 'update_running'
}
response = Compute.network_routers.partial_update(token=token, pk=static_route_id, data=static_route_update)
```

#### Delete Router
```python
# Note: All other project resources must be deleted first
response = Compute.network_routers.partial_update(token=token, pk=router_id, data={'state': 'delete'})
```

---
