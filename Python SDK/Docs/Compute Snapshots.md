# Compute Snapshots

### `Compute.compute_snapshots`

Point-in-time snapshots of instance states for LXD and Hyper-V instances.

#### Create Snapshot
```python
snapshot_data = {
    'instance_id': 1001,
    'name': 'Before Update Snapshot', 
    'project_id': 123,
    'type': 'lxd'  # or 'hyperv'
}
response = Compute.compute_snapshots.create(token=token, data=snapshot_data)
```

#### List Snapshots
```python
params = {
    'limit': 50,
    'page': 0,
    'search[project_id]': 123,    # Filter by project
    'search[instance_id]': 1001,  # Filter by instance  
    'order': '-created'
}
response = Compute.compute_snapshots.list(token=token, params=params)
```

#### Read Snapshot Details
```python
snapshot_id = 4001
response = Compute.compute_snapshots.read(token=token, pk=snapshot_id)
```

#### Revert Instance to Snapshot
```python
# To revert an instance to a snapshot, update the snapshot state
revert_data = {
    'state': 'update_running'  # This reverts the instance to snapshot state
}
response = Compute.compute_snapshots.partial_update(token=token, pk=snapshot_id, data=revert_data)
```

#### Delete Snapshot
```python
response = Compute.compute_snapshots.partial_update(token=token, pk=snapshot_id, data={'state': 'delete'})
```

---
