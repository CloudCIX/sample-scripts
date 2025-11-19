# Compute Images

### `Compute.images`

Operating system images available for instance creation.

#### List Available Images

```python
params = {
    'limit': 50,
    'page': 0,
    'order': 'sku_name',
    'search[os_variant__icontains]': 'ubuntu',  # Filter by OS
    'search[region_id]': 210514                 # Filter by region
}
response = Compute.images.list(token=token, params=params)
```

#### Read Image Details

```python
image_id = 1
response = Compute.images.read(token=token, pk=image_id)
```

*Note: Images are read-only system resources, so create/update operations are not available.*

---
