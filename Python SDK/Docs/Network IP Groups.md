# Network IP Groups

### `Compute.network_ip_groups`

CIDR network groups for firewall rules.

#### Create IP Group
```python
group_data = {
    'name': 'office-networks',
    'cidrs': ['91.103.3.0/24', '192.168.1.0/24'],
    'version': 4  # 4 for IPv4, 6 for IPv6
}
response = Compute.network_ip_groups.create(token=token, data=group_data)
```

#### List IP Groups
```python
response = Compute.network_ip_groups.list(token=token)
```

#### Delete IP Group (Uses DELETE method)
```python
response = Compute.network_ip_groups.delete(token=token, pk=group_id)
```

---