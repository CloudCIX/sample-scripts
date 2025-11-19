# Compute GPUs

### `Compute.compute_gpus`

GPU hardware accelerators for LXD instances.

#### Attach GPU

```python
gpu_data = {
    'instance_id': 1001,  # LXD instance only
    'name': 'ML GPU',
    'project_id': 123,
    'specs': [
        {'sku_name': 'A100_GPU'}  # GPU SKU
    ]
}
response = Compute.compute_gpus.create(token=token, data=gpu_data)
```

#### List GPUs

```python
params = {
    'search[project_id]': 123,
    'search[instance_id]': 1001,  # Filter by instance
    'order': '-created'
}
response = Compute.compute_gpus.list(token=token, params=params)
```

#### Read GPU Details

```python
gpu_id = 3001
response = Compute.compute_gpus.read(token=token, pk=gpu_id)
```

#### Update GPU

```python
# Update GPU name
update_data = {
    'name': 'High Performance GPU'
}
response = Compute.compute_gpus.partial_update(token=token, pk=gpu_id, data=update_data)
```

#### Detach GPU

```python
response = Compute.compute_gpus.partial_update(token=token, pk=gpu_id, data={'state': 'delete'})
```

---
