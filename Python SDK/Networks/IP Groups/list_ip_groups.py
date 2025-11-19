# File my_project/list_ip_groups.py

import os
os.environ.setdefault('CLOUDCIX_SETTINGS_MODULE', 'my_settings')

from cloudcix.api.compute import Compute

# Get a util function to get a session using the credentials in your settings file
from cloudcix.auth import get_admin_token

# ================================================================= #
#                      Get CloudCIX Token                           #
# ================================================================= #
token = get_admin_token()

# ================================================================= #
#                      List IP Groups with Filtering               #
# ================================================================= #

# Filter parameters - uncomment and modify as needed
params = {
    'limit': 50,                                    # Number of results per page (default: 50)
    'page': 0,                                      # Page number (0-based)
    'order': 'name',                                # Sort by: name, id, created, version
    'search[name__icontains]': 'CIX',          # Name contains (case-insensitive)
    # Text search filters (uncomment to use)
    # 'search[name__icontains]': 'office',          # Name contains "office" (case-insensitive)
    # 'search[name]': 'exact-name',                 # Exact name match
    # 'search[name__istartswith]': 'prod-',         # Name starts with "prod-"
    
    # Version filters
    # 'search[version]': 4,                         # IPv4 groups only
    # 'search[version]': 6,                         # IPv6 groups only
    
    # CIDR content filters
    # 'search[cidrs__icontains]': '192.168',        # Contains specific network
    # 'search[cidrs__icontains]': '10.0.0',         # Contains 10.x networks
    
    # Date filters
    # 'search[created__gte]': '2024-11-01',         # Created after date
    # 'search[created__lte]': '2024-11-30',         # Created before date
}

# Remove None values and empty filters
filtered_params = {k: v for k, v in params.items() if v is not None and str(v).strip()}

response = Compute.network_ip_groups.list(token=token, params=filtered_params)

# Print response and check structure
if response.status_code == 200:
    data = response.json()
    
    # Show filtering info
    total_results = data.get('total', len(data.get('content', [])))
    current_page = filtered_params.get('page', 0)
    limit = filtered_params.get('limit', 50)
    
    print(f"IP Groups Results: {total_results} total")
    if total_results > limit:
        print(f"Showing page {current_page + 1} (items {current_page * limit + 1}-{min((current_page + 1) * limit, total_results)})")
    
    # Show active filters
    active_filters = []
    for key, value in filtered_params.items():
        if key.startswith('search['):
            filter_name = key.replace('search[', '').replace(']', '')
            active_filters.append(f"{filter_name}={value}")
    
    if active_filters:
        print(f"Active filters: {', '.join(active_filters)}")
    
    print("=" * 60)
    
    if data.get('content'):
        for i, group in enumerate(data['content'], 1):
            print(f"{i}. ID: {group['id']} | Name: {group.get('name', 'N/A')} | IPv{group.get('version', 'N/A')}")
            
            # Show CIDRs with better formatting
            cidrs = group.get('cidrs', [])
            if cidrs:
                if len(cidrs) <= 5:
                    cidr_display = ', '.join(cidrs)
                else:
                    cidr_display = f"{', '.join(cidrs[:5])}... (+{len(cidrs)-5} more)"
                print(f"   Networks: {cidr_display}")
            else:
                print("   Networks: None")
            
            # Show creation date in readable format
            created = group.get('created', '')
            if created:
                # Convert ISO date to readable format
                try:
                    from datetime import datetime
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    readable_date = created_dt.strftime('%Y-%m-%d %H:%M UTC')
                    print(f"   Created: {readable_date}")
                except:
                    print(f"   Created: {created}")
            
            print("-" * 40)
    else:
        print("No IP groups found matching the current filters")
        if active_filters:
            print("Try removing some filters to see more results")
else:
    print(f"Error: {response.status_code}")
    print(response.text)