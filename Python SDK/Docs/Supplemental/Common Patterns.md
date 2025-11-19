# Common Parameters

### Pagination Parameters
```python
params = {
    'limit': 50,        # Items per page (0-100)
    'page': 0,          # Page number (0-based)
    'order': 'field',   # Sort field, prefix with '-' for descending
}
```

### Search/Filter Parameters
```python
params = {
    # Text matching
    'search[field]': 'value',                    # Exact match
    'search[field__icontains]': 'partial',       # Contains (case-insensitive)
    'search[field__iexact]': 'exact',            # Exact (case-insensitive)
    'search[field__istartswith]': 'prefix',      # Starts with (case-insensitive)
    'search[field__iendswith]': 'suffix',        # Ends with (case-insensitive)
    
    # Numeric comparisons
    'search[field__gt]': 100,                    # Greater than
    'search[field__gte]': 100,                   # Greater than or equal
    'search[field__lt]': 200,                    # Less than
    'search[field__lte]': 200,                   # Less than or equal
    
    # List operations
    'search[field__in]': 'value1,value2',        # In list
    'search[field__range]': 'start,end',         # Range (inclusive)
    
    # Null/existence checks
    'search[field__isnull]': True,               # Field is null
    'search[field__isnull]': False,              # Field is not null
    
    # Exclusions
    'exclude[field]': 'value',                   # Exclude exact matches
    'exclude[field__icontains]': 'partial',      # Exclude containing text
}
```

### Common Filterable Fields

**All Resources:**
- `id`, `created`, `updated`, `name`, `project_id`, `state`
- `project__address_id`, `project__name`, `project__region_id`, `project__reseller_id`

**Additional Fields by Resource Type:**
- **Compute Instances:** `type`, `grace_period`
- **Network Routers:** `type`, `grace_period`  
- **Network Firewalls:** `type`
- **Storage Volumes:** `type`
- **Images:** `os_variant`, `sku_name`, `region_id`, `type`
- **Snapshots/Backups:** `type`, `instance_id`
- **VPNs:** `type`

### Common States

**User-Triggered State Changes:**

```python
# State changes for compute instances:
{'state': 'stop'}               # Stop a running instance
{'state': 'restart'}            # Restart an instance  
{'state': 'delete'}             # Request deletion
{'state': 'update_running'}     # Update instance while running
{'state': 'update_stopped'}     # Update instance while stopped

# State changes for network resources (routers, firewalls, VPNs):
{'state': 'update_running'}     # Apply configuration changes
{'state': 'delete'}             # Request deletion
{'state': 'restart'}            # Restore from delete_queue

# State changes for storage volumes:
{'state': 'update_running'}     # Mount/unmount, expand capacity
{'state': 'delete'}             # Request deletion

# State changes for snapshots:
{'state': 'update_running'}     # Revert instance to snapshot state
{'state': 'delete'}             # Delete snapshot

# State changes for backups:
{'state': 'delete'}             # Delete backup

# State changes for GPUs:
{'state': 'delete'}             # Detach GPU from instance
```

**System-Managed States (Read-Only):**
- `pending` (1): Resource creation queued
- `building` (2): Resource being provisioned  
- `unresourced` (3): Failed to allocate resources
- `running` (4): Resource is operational
- `stopped` (6): Resource is halted
- `delete_queue` (9): Queued for deletion after grace period
- `deleted` (99): Permanently removed

**Grace Period Management:**
When you set a resource's state to `delete`, it enters `delete_queue` and waits for a grace period before permanent deletion. During this period:
- The resource remains visible but non-operational
- You can cancel deletion by setting state to `restart`
- Billing stops immediately when deletion is requested
- Default grace period is 7 days (can be customized per resource)

---