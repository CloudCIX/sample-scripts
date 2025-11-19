## Response Handling

### Standard Response Pattern
```python
response = Compute.some_resource.some_method(token=token, data=data)

if response.status_code in [200, 201, 202]:
    # Success responses
    data = response.json()
    content = data.get('content', {})  # Single resource
    content = data.get('content', [])  # List of resources
    metadata = data.get('_metadata', {})  # Pagination info
    
elif response.status_code == 400:
    # Bad request - validation errors
    error_data = response.json()
    if 'errors' in error_data:
        # Multi-field errors
        for field, error in error_data['errors'].items():
            print(f"Field '{field}': {error.get('detail', error)}")
    else:
        # Single error
        print(f"Error: {error_data.get('detail', 'Invalid input data')}")
    
elif response.status_code == 401:
    # Unauthorized - invalid or missing token
    error_detail = response.json().get('detail', 'Authentication failed')
    print(f"Authentication error: {error_detail}")
    
elif response.status_code == 403:
    # Forbidden - permission denied
    error_data = response.json()
    error_detail = error_data.get('detail', 'Permission denied')
    print(f"Access denied: {error_detail}")
    
elif response.status_code == 404:
    # Resource not found
    error_data = response.json()
    error_detail = error_data.get('detail', 'Resource not found')
    print(f"Not found: {error_detail}")
    
elif response.status_code == 204:
    # No content (successful deletion)
    print("Resource deleted successfully")
    
else:
    # Other errors
    try:
        error_data = response.json()
        error_detail = error_data.get('detail', response.text)
        print(f"Error {response.status_code}: {error_detail}")
    except:
        print(f"Error {response.status_code}: {response.text}")
```

### HTTP Status Codes

**Success Codes:**
- `200 OK`: Resource retrieved or updated successfully
- `201 Created`: Resource created successfully
- `202 Accepted`: Request accepted and processing (state changes)
- `204 No Content`: Resource deleted successfully

**Client Error Codes:**
- `400 Bad Request`: Invalid input data or validation errors
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Valid authentication but insufficient permissions
- `404 Not Found`: Requested resource does not exist

**Error Response Formats:**
```python
# Single field error (400)
{
  "detail": "Verbose error message explaining the issue",
  "error_code": "CLOUDCIX_ERROR_CODE"
}

# Multi-field errors (400)
{
  "errors": {
    "field_name": {
      "detail": "Field-specific error message",
      "error_code": "FIELD_ERROR_CODE"
    }
  }
}

# Authentication error (401)
{
  "detail": "No / invalid token provided"
}

# Permission error (403)
{
  "detail": "Permission denied for this user",
  "error_code": "PERMISSION_DENIED"
}

# Not found error (404)
{
  "detail": "One of the specified resources could not be found",
  "error_code": "RESOURCE_NOT_FOUND"
}
```

### Example Error Handling
```python
def handle_response(response, operation="operation"):
    """Standard response handler for CloudCIX API calls"""
    if response.status_code in [200, 201, 202]:
        return response.json().get('content')
    
    elif response.status_code == 400:
        errors = response.json().get('errors', {})
        print(f"Validation errors in {operation}:")
        for field, error in errors.items():
            print(f"  {field}: {error.get('detail', error)}")
        return None
    
    elif response.status_code in [401, 403]:
        print(f"Permission denied for {operation}")
        return None
    
    elif response.status_code == 404:
        print(f"Resource not found for {operation}")
        return None
    
    else:
        print(f"Error in {operation}: {response.status_code} - {response.text}")
        return None
```

---