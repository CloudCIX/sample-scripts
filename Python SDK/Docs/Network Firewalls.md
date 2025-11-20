# Network Firewalls

### `Compute.network_firewalls`

**IMPORTANT:** 
- Each project can have exactly ONE project firewall and ONE geo firewall maximum.
- When updating firewall rules, the entire rules array is **REPLACED** - include all existing rules you want to keep plus any new ones.

#### Create Firewall

```python
# Project Firewall - Fine-grained rules
firewall_data = {
    'project_id': 123,
    'type': 'project',  
    'name': 'Main Firewall',
    'rules': [
        {
            'allow': True,
            'description': 'Allow SSH from office',
            'destination': '10.0.1.0/24',
            'inbound': True,
            'port': '22',
            'protocol': 'tcp', 
            'source': '@office-networks'  # Reference IP group with @
        },
        {
            'allow': True,
            'description': 'Allow HTTPS from anywhere',
            'destination': '10.0.1.0/24', 
            'inbound': True,
            'port': '443',
            'protocol': 'tcp',
            'source': '*'  # Wildcard for any source
        }
    ]
}
```
#### Create Geofilter
```
# Geo Firewall - Country-based filtering  
geo_firewall_data = {
    'project_id': 123,
    'type': 'geo',
    'name': 'Geo Filter', 
    'rules': [
        {
            'allow': False,  # Block traffic
            'group_name': '@US_v4',  # Reference geo IP group
            'inbound': True
        }
    ]
}

response = Compute.network_firewalls.create(token=token, data=firewall_data)
```

#### List Firewalls
```python
params = {
    'limit': 50,
    'page': 0,
    'search[project_id]': 123
}
response = Compute.network_firewalls.list(token=token, params=params)
```

#### Read Firewall Details
```python
firewall_id = 789
response = Compute.network_firewalls.read(token=token, pk=firewall_id)
```

#### Update Firewall
```python
# IMPORTANT: When updating rules, the entire rules array is REPLACED
# To add a rule, you must include all existing rules + the new one
update_data = {
    'name': 'Updated Firewall',
    'rules': [
        {
            'allow': True,
            'description': 'Keep existing SSH rule',
            'destination': '10.0.1.0/24',
            'inbound': True,
            'port': '22',
            'protocol': 'tcp',
            'source': '@office-networks'
        },
        {
            'allow': True,
            'description': 'NEW rule - Allow HTTP',
            'destination': '10.0.1.0/24',
            'inbound': True,
            'port': '80',
            'protocol': 'tcp',
            'source': '*'
        }
    ]
}
response = Compute.network_firewalls.partial_update(token=token, pk=firewall_id, data=update_data)
```

#### Delete Firewall
```python
response = Compute.network_firewalls.partial_update(token=token, pk=firewall_id, data={'state': 'delete'})
```

---
