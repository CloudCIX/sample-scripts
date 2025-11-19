# Projects

### `Compute.project`

Projects are the top-level containers for all compute resources.

```python
from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token

token = get_admin_token()
```

#### Create Project
```python
project_data = {
    'name': 'My Project',
    'region_id': 12345,  # Required
    'note': 'Project description'
}
response = Compute.project.create(token=token, data=project_data)
```

#### List Projects
```python
params = {
    'limit': 50,
    'page': 0,
    'order': '-created'  # or 'name', 'id', etc.
}
response = Compute.project.list(token=token, params=params)
```

#### Read Project Details
```python
project_id = 123
response = Compute.project.read(token=token, pk=project_id)
```

#### Update Project
```python
update_data = {
    'name': 'Updated Project Name',
    'note': 'Updated description'
}
response = Compute.project.partial_update(token=token, pk=project_id, data=update_data)
```

---