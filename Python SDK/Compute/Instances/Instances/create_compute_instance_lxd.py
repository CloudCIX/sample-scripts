# File my_project/create_compute_instance_lxd.py

import os
from pprint import pprint
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# LXD Instance data to create
lxd_vm_data = {
    'project_id': 123,              # Change this to your project ID
    'name': 'My First Instance',      # Change this to your desired Instance name
    'type': 'lxd',
    'grace_period': 72,
    'metadata': {
        'instance_type': 'virtual-machine', # Instance type use 'virtual-machine' or 'container'
        'dns': '8.8.8.8,8.8.4.4',     # DNS as comma-separated string
        'userdata': "#cloud-config\nusers:\n  - name: administrator\n    groups: sudo\n    shell: /bin/bash\n    lock_passwd: false\n    passwd: $MY_HASED_PASSWORD\n    ssh_authorized_keys:\n      - ssh-ed25519 mypublicsshkey1234\nchpasswd:\n  expire: false\nssh_pwauth: true\n"
    },
    'interfaces': [
        {
            'gateway': True,
            'ipv4_addresses': [
                {
                    'address': '10.0.1.2',    # Change this to your desired IP
                    'nat': True
                }
            ],
            "ipv6_addresses": [
                {
                "address": "2a02:2078:10:35gb::2"     # Change this to your desired IP
                }
            ]
        }
    ],
    'specs': [
        {'quantity': 2, 'sku_name': 'RAM_001'},        # 4GB RAM
        {'quantity': 1, 'sku_name': 'vCPU_001'},        # 2 CPU cores  
        {'quantity': 16, 'sku_name': 'SSD_001'},       # 16GB storage
        {'quantity': 1, 'sku_name': 'UBUNTU2404'}    # Ubuntu 24.04 LTS
    ]
}

# ================================================================= #
#                      Create LXD Virtual Machine                   #
# ================================================================= #
response = Compute.compute_instances.create(token=token, data=lxd_vm_data)

# Print out the json of the response data with beautiful formatting
pprint (response.json())