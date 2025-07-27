# 🔌 API 文档

PyPI仓库的RESTful API接口文档。

## 📋 基础信息

- **基础URL**: `http://localhost:8385`
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`

## 🔍 基础接口

### 健康检查

检查服务健康状态。

```http
GET /health
```

**响应示例**:
```json
{
    "service": "pypi-repository",
    "status": "healthy",
    "timestamp": 1753612835.1297045
}
```

### 统计信息

获取仓库统计信息。

```http
GET /stats
```

**响应示例**:
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

### 包列表

获取所有包的列表。

```http
GET /packages
```

**响应示例**:
```json
{
    "payo-cli": [
        "index.html",
        "payo_cli-1.0.0-py3-none-any.whl",
        "payo_cli-1.0.0.tar.gz"
    ]
}
```

### 包详情

获取特定包的详细信息。

```http
GET /packages/{package_name}
```

**参数**:
- `package_name` (string): 包名

**响应示例**:
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

### 包索引

获取所有包的索引页面（PyPI Simple API）。

```http
GET /simple/
```

**响应**: HTML格式的包索引页面

### 包文件列表

获取特定包的文件列表（PyPI Simple API）。

```http
GET /simple/{package_name}/
```

**参数**:
- `package_name` (string): 包名

**响应**: HTML格式的包文件列表页面

### 包文件下载

下载包文件。

```http
GET /{package_name}/{filename}
```

**参数**:
- `package_name` (string): 包名
- `filename` (string): 文件名

**响应**: 文件内容

## 🔧 管理接口

### 删除包

删除指定的包。

```http
DELETE /admin/packages/{package_name}
```

**参数**:
- `package_name` (string): 包名

**响应示例**:
```json
{
    "message": "包 payo-cli 删除成功"
}
```

### 包详细信息

获取包的详细信息。

```http
GET /admin/packages/{package_name}/info
```

**参数**:
- `package_name` (string): 包名

**响应示例**:
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

## 📊 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 🔍 使用示例

### cURL 示例

```bash
# 健康检查
curl http://localhost:8385/health

# 获取统计信息
curl http://localhost:8385/stats

# 获取包列表
curl http://localhost:8385/packages

# 获取包详情
curl http://localhost:8385/packages/payo-cli

# 删除包
curl -X DELETE http://localhost:8385/admin/packages/payo-cli

# 获取包信息
curl http://localhost:8385/admin/packages/payo-cli/info
```

### Python 示例

```python
import requests

# 基础URL
base_url = "http://localhost:8385"

# 健康检查
response = requests.get(f"{base_url}/health")
print(response.json())

# 获取包列表
response = requests.get(f"{base_url}/packages")
packages = response.json()
print(packages)

# 删除包
response = requests.delete(f"{base_url}/admin/packages/my-package")
print(response.json())
```

### JavaScript 示例

```javascript
// 基础URL
const baseUrl = "http://localhost:8385";

// 健康检查
fetch(`${baseUrl}/health`)
  .then(response => response.json())
  .then(data => console.log(data));

// 获取包列表
fetch(`${baseUrl}/packages`)
  .then(response => response.json())
  .then(data => console.log(data));

// 删除包
fetch(`${baseUrl}/admin/packages/my-package`, {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔐 安全说明

- 管理接口没有认证机制，建议在生产环境中添加认证
- 文件上传接口支持文件类型验证
- 建议配置HTTPS以提高安全性

## 📚 相关链接

- [PyPI Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask RESTful](https://flask-restful.readthedocs.io/)
- [HTTP状态码](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) 