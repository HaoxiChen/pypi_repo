# 🔌 API Documentation

RESTful API documentation for the PyPI repository.

## 📋 Basic Information

- **Base URL**: `http://localhost:8385`
- **Content Type**: `application/json`
- **Character Encoding**: `UTF-8`

## 🔍 Basic Interfaces

### Health Check

Check service health status.

```http
GET /health
```

**Response Example**:
```json
{
    "service": "pypi-repository",
    "status": "healthy",
    "timestamp": 1753612835.1297045
}
```

### Statistics

Get repository statistics.

```http
GET /stats
```

**Response Example**:
```json
{
    "packages_count": 1,
    "files_count": 3,
    "total_size_mb": 0.02,
    "uptime": 0.0004055500030517578,
    "is_healthy": true,
    "last_health_check": 1753612878.188948
}
```

### Package List

Get list of all packages.

```http
GET /packages
```

**Response Example**:
```json
{
    "payo-cli": [
        "index.html",
        "payo_cli-1.0.0-py3-none-any.whl",
        "payo_cli-1.0.0.tar.gz"
    ]
}
```

### Package Details

Get detailed information for a specific package.

```http
GET /packages/{package_name}
```

**Parameters**:
- `package_name` (string): Package name

**Response Example**:
```json
{
    "name": "payo-cli",
    "files": [
        "payo_cli-1.0.0-py3-none-any.whl",
        "payo_cli-1.0.0.tar.gz"
    ],
    "file_count": 2,
    "has_wheel": true,
    "has_source": true
}
```

## 📦 PyPI Simple Repository API

### Package Index

Get package index page (PyPI Simple API).

```http
GET /simple/
```

**Response**: HTML format package index page

### Package File List

Get file list for a specific package (PyPI Simple API).

```http
GET /simple/{package_name}/
```

**Parameters**:
- `package_name` (string): Package name

**Response**: HTML format package file list page

### Package File Download

Download package file.

```http
GET /{package_name}/{filename}
```

**Parameters**:
- `package_name` (string): Package name
- `filename` (string): File name

**Response**: File content

## 🔧 Management Interfaces

### Delete Package

Delete specified package.

```http
DELETE /admin/packages/{package_name}
```

**Parameters**:
- `package_name` (string): Package name

**Response Example**:
```json
{
    "message": "Package payo-cli deleted successfully"
}
```

### Package Detailed Information

Get detailed information for a package.

```http
GET /admin/packages/{package_name}/info
```

**Parameters**:
- `package_name` (string): Package name

**Response Example**:
```json
{
    "name": "payo-cli",
    "files": {
        "payo_cli-1.0.0-py3-none-any.whl": {
            "size": 10240,
            "size_mb": 0.01,
            "type": "wheel"
        },
        "payo_cli-1.0.0.tar.gz": {
            "size": 8192,
            "size_mb": 0.01,
            "type": "source"
        }
    },
    "file_count": 2,
    "total_size": 18432,
    "total_size_mb": 0.02,
    "has_wheel": true,
    "has_source": true
}
```

## 📊 Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Resource not found |
| 500 | Internal server error |

## 🔍 Usage Examples

### cURL Examples

```bash
# Health check
curl http://localhost:8385/health

# Get statistics
curl http://localhost:8385/stats

# Get package list
curl http://localhost:8385/packages

# Get package details
curl http://localhost:8385/packages/payo-cli

# Delete package
curl -X DELETE http://localhost:8385/admin/packages/payo-cli

# Get package information
curl http://localhost:8385/admin/packages/payo-cli/info
```

### Python Examples

```python
import requests

# Base URL
base_url = "http://localhost:8385"

# Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# Get package list
response = requests.get(f"{base_url}/packages")
packages = response.json()
print(packages)

# Delete package
response = requests.delete(f"{base_url}/admin/packages/my-package")
print(response.json())
```

### JavaScript Examples

```javascript
// Base URL
const baseUrl = "http://localhost:8385";

// Health check
fetch(`${baseUrl}/health`)
  .then(response => response.json())
  .then(data => console.log(data));

// Get package list
fetch(`${baseUrl}/packages`)
  .then(response => response.json())
  .then(data => console.log(data));

// Delete package
fetch(`${baseUrl}/admin/packages/my-package`, {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔐 Security Notes

- Management interfaces have no authentication mechanism, consider adding authentication in production
- File upload interface supports file type validation
- Consider configuring HTTPS for improved security

## 📚 Related Links

- [PyPI Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask RESTful](https://flask-restful.readthedocs.io/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) 