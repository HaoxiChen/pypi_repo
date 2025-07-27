# 🐍 PyPI Private Repository

<div align="center">

# 🌍 语言选择 / Language Selection

[🇨🇳 中文版本](#-中文版本) | [🇺🇸 English Version](#-english-version)

---

</div>

---

## 🇨🇳 中文版本

一个功能完整的私有Python包仓库，支持包上传、管理和分发。

### ✨ 主要特性

- 🚀 **简单易用** - 一键启动，Web界面管理
- 📦 **包管理** - 上传、删除、查看包
- 🌐 **Web界面** - 现代化管理仪表板
- 💻 **命令行工具** - 脚本化管理
- 🔄 **自动恢复** - 进程监控和自动重启
- 📊 **实时统计** - 包数量、文件大小等统计
- 🔌 **API支持** - RESTful API接口
- 🛡️ **生产就绪** - 支持Supervisor和Systemd部署

### 🚀 快速开始

#### 1. 启动服务

```bash
# 克隆或下载项目
cd pypi_repo

# 一键启动
chmod +x start.sh
./start.sh
```

#### 2. 访问服务

- **仓库主页**: http://localhost:8385
- **管理界面**: http://localhost:8385/admin/
- **健康检查**: http://localhost:8385/health
- **统计信息**: http://localhost:8385/stats

### 📦 包管理

#### Web界面管理（推荐）

1. 打开浏览器访问 http://localhost:8385/admin/
2. 点击"Upload Package"标签页
3. 选择包文件（支持 .whl, .tar.gz, .zip）
4. 点击"Upload Package"上传

#### 命令行管理

```bash
# 列出所有包
python3 manage_packages.py list

# 上传包
python3 manage_packages.py upload --file my-package-1.0.0.whl

# 删除包
python3 manage_packages.py remove --package my-package
```

### 🌐 使用仓库

#### 安装包

```bash
# 从仓库安装
pip install --extra-index-url http://localhost:8385/ package-name

# 安装特定版本
pip install --extra-index-url http://localhost:8385/ package-name==1.0.0

# 永久配置
pip config set global.extra-index-url http://localhost:8385/
pip install package-name
```

#### 配置pip

```bash
# 创建pip配置文件
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
extra-index-url = http://localhost:8385/
trusted-host = localhost
EOF
```

### 🛠️ 管理命令

```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh

# 重启服务
./stop.sh && ./start.sh

# 查看状态
ps aux | grep app.py

# 查看日志
tail -f pypi_repo.log
tail -f logs/monitor.log
```

### 📊 API接口

#### 基础接口

```bash
# 健康检查
curl http://localhost:8385/health

# 统计信息
curl http://localhost:8385/stats

# 包列表
curl http://localhost:8385/packages

# 包详情
curl http://localhost:8385/packages/package-name
```

#### 管理接口

```bash
# 删除包
curl -X DELETE http://localhost:8385/admin/packages/package-name

# 包信息
curl http://localhost:8385/admin/packages/package-name/info
```

### 📁 项目结构

```
pypi_repo/
├── app.py                    # 主应用文件
├── start.sh                  # 启动脚本
├── stop.sh                   # 停止脚本
├── manage_packages.py        # 简单包管理脚本
├── packages/                 # 包存储目录
├── config/                   # 配置模块
├── models/                   # 数据模型
├── routes/                   # 路由模块
├── templates/                # 模板文件
├── tools/                    # 工具模块
└── logs/                     # 日志目录
```

### 🔧 配置选项

#### 环境变量

```bash
# 端口配置
export PORT=8385

# 包存储目录
export PACKAGES_DIR=packages

# 日志级别
export LOG_LEVEL=INFO
```

#### 配置文件

主要配置在 `config/settings.py` 中：

```python
class Config:
    HOST = '0.0.0.0'
    PORT = 8385
    PACKAGES_DIR = 'packages'
    DEBUG = False
    LOG_LEVEL = 'INFO'
```

### 🚀 部署选项

#### 1. 开发环境

```bash
# 直接运行
python3 app.py
```

#### 2. 生产环境（推荐）

```bash
# 使用启动脚本
./start.sh

# 或使用Gunicorn
gunicorn -c gunicorn.conf.py app:create_app()

# 或使用Supervisor
supervisord -c supervisor.conf
```

#### 3. Systemd服务

```bash
# 安装系统服务
sudo cp systemd.service /etc/systemd/system/pypi-repo.service
sudo systemctl daemon-reload
sudo systemctl enable pypi-repo
sudo systemctl start pypi-repo
```

### 📋 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Wheel | `.whl` | 预编译包，安装速度快 |
| Source | `.tar.gz` | 源码包，需要编译 |
| ZIP | `.zip` | 压缩源码包 |

### 🔍 监控和日志

#### 日志文件

- `pypi_repo.log` - 应用主日志
- `logs/monitor.log` - 监控日志
- `access.log` - 访问日志
- `error.log` - 错误日志

#### 监控功能

- 自动健康检查
- 进程监控和重启
- 性能统计
- 错误告警

### 🛠️ 故障排除

#### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   netstat -tlnp | grep 8385
   
   # 检查日志
   tail -f pypi_repo.log
   ```

2. **包上传失败**
   ```bash
   # 检查文件权限
   ls -la packages/
   
   # 检查磁盘空间
   df -h
   ```

3. **包无法安装**
   ```bash
   # 检查包是否存在
   curl http://localhost:8385/simple/package-name/
   
   # 检查健康状态
   curl http://localhost:8385/health
   ```

#### 性能优化

```bash
# 调整Gunicorn配置
# 编辑 gunicorn.conf.py

# 清理缓存
./stop.sh && ./start.sh

# 监控磁盘使用
du -sh packages/
```

### 📚 详细文档

- [包管理指南](PACKAGE_MANAGEMENT.md) - 详细的包管理使用说明
- [部署指南](DEPLOYMENT.md) - 生产环境部署说明
- [项目结构](PROJECT_STRUCTURE.md) - 代码架构说明

### 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

### 📄 许可证

MIT License

### 🔗 相关链接

- [Python Packaging User Guide](https://packaging.python.org/)
- [Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🇺🇸 English Version

A fully-featured private Python package repository with package upload, management, and distribution capabilities.

### ✨ Key Features

- 🚀 **Easy to Use** - One-click startup, web-based management
- 📦 **Package Management** - Upload, delete, and view packages
- 🌐 **Web Interface** - Modern management dashboard
- 💻 **Command Line Tools** - Script-based management
- 🔄 **Auto Recovery** - Process monitoring and automatic restart
- 📊 **Real-time Statistics** - Package count, file size, and other metrics
- 🔌 **API Support** - RESTful API interfaces
- 🛡️ **Production Ready** - Supervisor and Systemd deployment support

### 🚀 Quick Start

#### 1. Start the Service

```bash
# Clone or download the project
cd pypi_repo

# One-click startup
chmod +x start.sh
./start.sh
```

#### 2. Access the Service

- **Repository Homepage**: http://localhost:8385
- **Management Interface**: http://localhost:8385/admin/
- **Health Check**: http://localhost:8385/health
- **Statistics**: http://localhost:8385/stats

### 📦 Package Management

#### Web Interface Management (Recommended)

1. Open your browser and visit http://localhost:8385/admin/
2. Click the "Upload Package" tab
3. Select your package file (supports .whl, .tar.gz, .zip)
4. Click "Upload Package"

#### Command Line Management

```bash
# List all packages
python3 manage_packages.py list

# Upload a package
python3 manage_packages.py upload --file my-package-1.0.0.whl

# Delete a package
python3 manage_packages.py remove --package my-package
```

### 🌐 Using the Repository

#### Installing Packages

```bash
# Install from repository
pip install --extra-index-url http://localhost:8385/ package-name

# Install specific version
pip install --extra-index-url http://localhost:8385/ package-name==1.0.0

# Permanent configuration
pip config set global.extra-index-url http://localhost:8385/
pip install package-name
```

#### Configuring pip

```bash
# Create pip configuration file
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
extra-index-url = http://localhost:8385/
trusted-host = localhost
EOF
```

### 🛠️ Management Commands

```bash
# Start service
./start.sh

# Stop service
./stop.sh

# Restart service
./stop.sh && ./start.sh

# Check status
ps aux | grep app.py

# View logs
tail -f pypi_repo.log
tail -f logs/monitor.log
```

### 📊 API Interfaces

#### Basic Interfaces

```bash
# Health check
curl http://localhost:8385/health

# Statistics
curl http://localhost:8385/stats

# Package list
curl http://localhost:8385/packages

# Package details
curl http://localhost:8385/packages/package-name
```

#### Management Interfaces

```bash
# Delete package
curl -X DELETE http://localhost:8385/admin/packages/package-name

# Package information
curl http://localhost:8385/admin/packages/package-name/info
```

### 📁 Project Structure

```
pypi_repo/
├── app.py                    # Main application file
├── start.sh                  # Startup script
├── stop.sh                   # Stop script
├── manage_packages.py        # Simple package management script
├── packages/                 # Package storage directory
├── config/                   # Configuration module
├── models/                   # Data models
├── routes/                   # Route modules
├── templates/                # Template files
├── tools/                    # Tool modules
└── logs/                     # Log directory
```

### 🔧 Configuration Options

#### Environment Variables

```bash
# Port configuration
export PORT=8385

# Package storage directory
export PACKAGES_DIR=packages

# Log level
export LOG_LEVEL=INFO
```

#### Configuration File

Main configuration in `config/settings.py`:

```python
class Config:
    HOST = '0.0.0.0'
    PORT = 8385
    PACKAGES_DIR = 'packages'
    DEBUG = False
    LOG_LEVEL = 'INFO'
```

### 🚀 Deployment Options

#### 1. Development Environment

```bash
# Direct run
python3 app.py
```

#### 2. Production Environment (Recommended)

```bash
# Use startup script
./start.sh

# Or use Gunicorn
gunicorn -c gunicorn.conf.py app:create_app()

# Or use Supervisor
supervisord -c supervisor.conf
```

#### 3. Systemd Service

```bash
# Install system service
sudo cp systemd.service /etc/systemd/system/pypi-repo.service
sudo systemctl daemon-reload
sudo systemctl enable pypi-repo
sudo systemctl start pypi-repo
```

### 📋 Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| Wheel | `.whl` | Pre-compiled package, fast installation |
| Source | `.tar.gz` | Source package, requires compilation |
| ZIP | `.zip` | Compressed source package |

### 🔍 Monitoring and Logging

#### Log Files

- `pypi_repo.log` - Main application log
- `logs/monitor.log` - Monitoring log
- `access.log` - Access log
- `error.log` - Error log

#### Monitoring Features

- Automatic health checks
- Process monitoring and restart
- Performance statistics
- Error alerts

### 🛠️ Troubleshooting

#### Common Issues

1. **Service won't start**
   ```bash
   # Check port usage
   netstat -tlnp | grep 8385
   
   # Check logs
   tail -f pypi_repo.log
   ```

2. **Package upload fails**
   ```bash
   # Check file permissions
   ls -la packages/
   
   # Check disk space
   df -h
   ```

3. **Package won't install**
   ```bash
   # Check if package exists
   curl http://localhost:8385/simple/package-name/
   
   # Check health status
   curl http://localhost:8385/health
   ```

#### Performance Optimization

```bash
# Adjust Gunicorn configuration
# Edit gunicorn.conf.py

# Clear cache
./stop.sh && ./start.sh

# Monitor disk usage
du -sh packages/
```

### 📚 Detailed Documentation

- [Package Management Guide](PACKAGE_MANAGEMENT_EN.md) - Detailed package management instructions
- [Deployment Guide](DEPLOYMENT_EN.md) - Production environment deployment instructions
- [Project Structure](PROJECT_STRUCTURE_EN.md) - Code architecture explanation

### 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project.

### 📄 License

MIT License

### 🔗 Related Links

- [Python Packaging User Guide](https://packaging.python.org/)
- [Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

<div align="center">

**开始使用 / Get Started**: 运行 `./start.sh` 即可启动你的私有PyPI仓库！🎉

**Run `./start.sh` to start your private PyPI repository! 🎉**

</div> 