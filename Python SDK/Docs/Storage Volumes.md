# Storage Volumes

### `Compute.storage_volumes`

CloudCIX supports two types of persistent storage volumes:

**CephFS Volumes (`type: "cephfs"`):**

- Network-attached file system volumes that can be mounted to multiple LXD instances simultaneously
- Shared storage accessible across multiple containers/VMs
- Managed through mount/unmount operations using metadata
- Uses Ceph storage SKUs (e.g., CEPH_001)

**Hyper-V Volumes (`type: "hyperv"`):**

- Secondary drives attached directly to a single Hyper-V Windows VM
- Instance-specific storage that cannot be shared
- Requires `instance_id` to specify target VM during creation
- Uses standard storage SKUs (e.g., SSD_001, HDD_001)

**Key Storage Features:**

- Volume capacity can be increased (but not decreased) after creation
- CephFS volumes support multiple concurrent mounts with configurable mount paths
- Storage capacity is specified using SKUs with quantity in GB
- Available SKUs depend on your region's configured storage devices

#### Create CephFS Filesystem (Shared Network Storage)

```python
cephfs_volume_data = {
    'project_id': 123,
    'name': 'Shared Data',
    'type': 'cephfs',
    'specs': [
        {'quantity': 500, 'sku_name': 'CEPH_001'}  # 500GB Ceph storage
    ]
}
response = Compute.storage_volumes.create(token=token, data=cephfs_volume_data)
```

#### Create Hyper-V Volume (VM Secondary Drive)

```python
hyperv_volume_data = {
    'project_id': 123,
    'instance_id': 456,  # Required - target Hyper-V VM
    'name': 'Additional Storage',
    'type': 'hyperv',
    'specs': [
        {'quantity': 250, 'sku_name': 'SSD_001'}  # 250GB SSD storage
    ]
}
response = Compute.storage_volumes.create(token=token, data=hyperv_volume_data)
```

#### List Storage Volumes

```python
params = {
    'limit': 50,
    'page': 0,
    'search[project_id]': 123,
    'search[type]': 'cephfs'  # Filter by volume type
}
response = Compute.storage_volumes.list(token=token, params=params)
```

#### Read Volume Details

```python
volume_id = 2001
response = Compute.storage_volumes.read(token=token, pk=volume_id)
```

#### Mount CephFS Volume to LXD Instances

```python
# Mount shared volume to multiple LXD instances
mount_data = {
    'name': 'Shared Data Volume',
    'metadata': {
        'attach_instance_ids': [123, 456, 789],  # LXD instance IDs
        'mount_path': '/mnt/shared-data'
    },
    'state': 'update_running'
}
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data=mount_data)
```

#### Unmount CephFS Volume from Instances

```python
# Unmount volume from specific instances
unmount_data = {
    'metadata': {
        'detach_instance_ids': [456],  # Instance IDs to unmount from
        'mount_path': '/mnt/shared-data'
    },
    'state': 'update_running'
}
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data=unmount_data)
```

#### Expand Volume Storage Capacity

```python
# Increase storage size (cannot decrease)
expand_data = {
    'specs': [
        {'quantity': 1000, 'sku_name': 'CEPH_001'}  # Expand to 1TB
    ],
    'state': 'update_running'
}
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data=expand_data)
```

#### Update Volume Name

```python
update_data = {
    'name': 'Updated Volume Name',
    'state': 'update_running'
}
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data=update_data)
```

#### Delete Volume

```python
response = Compute.storage_volumes.partial_update(token=token, pk=volume_id, data={'state': 'delete'})
```

---
