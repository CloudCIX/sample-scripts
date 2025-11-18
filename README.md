# sample-scripts
Example scripts for interacting with CloudCIX Applications.

## Setup

### Prerequisites
- Create an account on the CloudCIX Platform - Register

- Retrieve your CloudCIX Memebr API Key - Under the My Membership tab in the sidebar, click on Member Details - The API Key be available at the top of the form


### Installating the Python SDK

```bash
pip3 install -U "cloudcix>=5.0.0"
```

#### Configuration

Create a `my_settings.py` file with your CloudCIX credentials:

```python
# my_settings.py
CLOUDCIX_API_URL="https://legacyapi.api.cloudcix.com/"
CLOUDCIX_API_V2_URL="https://api.cloudcix.com/"
CLOUDCIX_API_VERSION="5.0"
CLOUDCIX_API_USERNAME="GeorgeBoole@cix.ie"            # Email Address registered in Prerequisites
CLOUDCIX_API_PASSWORD="My_Password"                   # Password for email registered
CLOUDCIX_API_KEY="MyCl0uDC1X4P1K3Y"                   # CloudCIX Memebr API Key
```

#### Basic Script Structure

```python
import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute
from cloudcix.auth import get_admin_token

# Get authentication token
token = get_admin_token()

# Your API calls here
response = Compute.project.list(token=token)
```

#### Authentication

The SDK uses token-based authentication. Always call `get_admin_token()` before making API requests:

```python
from cloudcix.auth import get_admin_token
token = get_admin_token()
```
