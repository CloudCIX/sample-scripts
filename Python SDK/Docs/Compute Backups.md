# Compute Backups

### `Compute.compute_backups`

Repository-stored backups of instances for disaster recovery and data protection.

#### Create Backup
```python
# Create backup for LXD instance
lxd_backup_data = {
    'instance_id': 1001,
    'name': 'Weekly LXD Backup',
    'project_id': 123,
    'type': 'lxd'
}

# Create backup for Hyper-V instance
hyperv_backup_data = {
    'instance_id': 456,
    'name': 'Critical Windows Backup',
    'project_id': 123, 
    'type': 'hyperv'
}

response = Compute.compute_backups.create(token=token, data=lxd_backup_data)
```

#### List Backups
```python
params = {
    'limit': 50,
    'page': 0, 
    'search[project_id]': 123,
    'search[type]': 'lxd',  # Filter by backup type
    'search[instance_id]': 1001,  # Filter by instance
    'order': '-created'
}
response = Compute.compute_backups.list(token=token, params=params)
```

#### Read Backup Details
```python
backup_id = 2001
response = Compute.compute_backups.read(token=token, pk=backup_id)
```

#### Update Backup Name
```python
update_data = {
    'name': 'Monthly Backup - November 2025'
}
response = Compute.compute_backups.partial_update(token=token, pk=backup_id, data=update_data)
```

#### Delete Backup
```python
delete_data = {'state': 'delete'}
response = Compute.compute_backups.partial_update(token=token, pk=backup_id, data=delete_data)
```

#### Restore from Backup
**Note:** To restore from a backup, please contact **support@cloudcix.com** with your backup details and we will assist you in restoring your instance from the backup.

---