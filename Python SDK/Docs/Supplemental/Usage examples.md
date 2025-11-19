## Usage Examples

### Complete Infrastructure Setup
```python
# 1. Create project
project = handle_response(
    Compute.project.create(token=token, data=project_data),
    "project creation"
)

# 2. Create router
router = handle_response(
    Compute.network_routers.create(token=token, data=router_data),
    "router creation"
)

# 3. Create firewall
firewall = handle_response(
    Compute.network_firewalls.create(token=token, data=firewall_data),
    "firewall creation"
)

# 4. Create instance
instance = handle_response(
    Compute.compute_instances.create(token=token, data=instance_data),
    "instance creation"
)
```

### Resource Cleanup
```python
# Delete in reverse order of dependencies
resources = [
    (Compute.compute_instances, instance_id, 'delete'),
    (Compute.network_firewalls, firewall_id, 'delete'),
    (Compute.network_routers, router_id, 'delete'),
    (Compute.project, project_id, 'delete')
]

for resource_api, resource_id, state in resources:
    response = resource_api.partial_update(
        token=token, 
        pk=resource_id, 
        data={'state': state}
    )
    if response.status_code in [200, 202]:
        print(f"Deleted {resource_api.__name__} {resource_id}")
```

---

---