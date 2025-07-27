# 🐍 PyPI Private Repository

A fully-featured private Python package repository with package upload, management, and distribution capabilities.

## ✨ Key Features

- 🚀 **Easy to Use** - One-click startup, web-based management
- 📦 **Package Management** - Upload, delete, and view packages
- 🌐 **Web Interface** - Modern management dashboard
- 💻 **Command Line Tools** - Script-based management
- 🔄 **Auto Recovery** - Process monitoring and automatic restart
- 📊 **Real-time Statistics** - Package count, file size, and other metrics
- 🔌 **API Support** - RESTful API interfaces
- 🛡️ **Production Ready** - Supervisor and Systemd deployment support

## 🚀 Quick Start

### 1. Start the Service

```bash
# Clone or download the project
cd pypi_repo

# One-click startup
chmod +x start.sh
./start.sh
```

### 2. Access the Service

- **Repository Homepage**: http://localhost:8385
- **Management Interface**: http://localhost:8385/admin/
- **Health Check**: http://localhost:8385/health
- **Statistics**: http://localhost:8385/stats

## 📦 Package Management

### Web Interface Management (Recommended)

1. Open your browser and visit http://localhost:8385/admin/
2. Click the "Upload Package" tab
3. Select your package file (supports .whl, .tar.gz, .zip)
4. Click "Upload Package"

### Command Line Management

```bash
# List all packages
python3 manage_packages.py list

# Upload a package
python3 manage_packages.py upload --file my-package-1.0.0.whl

# Delete a package
python3 manage_packages.py remove --package my-package
```

### Advanced Management Tools

```bash
# Use more powerful management tools
python3 tools/package_manager.py upload --file package.whl
python3 tools/package_manager.py update --package name --file new-version.whl
python3 tools/package_manager.py info --package package-name
```

## 🌐 Using the Repository

### Installing Packages

```bash
# Install from repository
pip install --extra-index-url http://localhost:8385/ package-name

# Install specific version
pip install --extra-index-url http://localhost:8385/ package-name==1.0.0

# Permanent configuration
pip config set global.extra-index-url http://localhost:8385/
pip install package-name
```

### Configuring pip

```bash
# Create pip configuration file
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
extra-index-url = http://localhost:8385/
trusted-host = localhost
EOF
```

## 🛠️ Management Commands

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

## 📊 API Interfaces

### Basic Interfaces

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

### Management Interfaces

```bash
# Delete package
curl -X DELETE http://localhost:8385/admin/packages/package-name

# Package information
curl http://localhost:8385/admin/packages/package-name/info
```

## 📁 Project Structure

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

## 🔧 Configuration Options

### Environment Variables

```bash
# Port configuration
export PORT=8385

# Package storage directory
export PACKAGES_DIR=packages

# Log level
export LOG_LEVEL=INFO
```

### Configuration File

Main configuration in `config/settings.py`:

```python
class Config:
    HOST = '0.0.0.0'
    PORT = 8385
    PACKAGES_DIR = 'packages'
    DEBUG = False
    LOG_LEVEL = 'INFO'
```

## 🚀 Deployment Options

### 1. Development Environment

```bash
# Direct run
python3 app.py
```

### 2. Production Environment (Recommended)

```bash
# Use startup script
./start.sh

# Or use Gunicorn
gunicorn -c gunicorn.conf.py app:create_app()

# Or use Supervisor
supervisord -c supervisor.conf
```

### 3. Systemd Service

```bash
# Install system service
sudo cp systemd.service /etc/systemd/system/pypi-repo.service
sudo systemctl daemon-reload
sudo systemctl enable pypi-repo
sudo systemctl start pypi-repo
```

## 📋 Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| Wheel | `.whl` | Pre-compiled package, fast installation |
| Source | `.tar.gz` | Source package, requires compilation |
| ZIP | `.zip` | Compressed source package |

## 🔍 Monitoring and Logging

### Log Files

- `pypi_repo.log` - Main application log
- `logs/monitor.log` - Monitoring log
- `access.log` - Access log
- `error.log` - Error log

### Monitoring Features

- Automatic health checks
- Process monitoring and restart
- Performance statistics
- Error alerts

## 🛠️ Troubleshooting

### Common Issues

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

### Performance Optimization

```bash
# Adjust Gunicorn configuration
# Edit gunicorn.conf.py

# Clear cache
./stop.sh && ./start.sh

# Monitor disk usage
du -sh packages/
```

## 📚 Detailed Documentation

- [Package Management Guide](PACKAGE_MANAGEMENT_EN.md) - Detailed package management instructions
- [Deployment Guide](DEPLOYMENT_EN.md) - Production environment deployment instructions
- [Project Structure](PROJECT_STRUCTURE_EN.md) - Code architecture explanation

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project.

## 📄 License

MIT License

## 🔗 Related Links

- [Python Packaging User Guide](https://packaging.python.org/)
- [Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

<div align="center">

**Get Started**: Run `./start.sh` to start your private PyPI repository! 🎉

</div> 