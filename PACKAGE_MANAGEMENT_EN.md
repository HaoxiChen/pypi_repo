# 📦 Package Management Guide

This guide explains how to use the PyPI repository's package management features, including uploading, updating, deleting, and managing packages.

## 🚀 Quick Start

### 1. Web Interface Management (Recommended)

Access the management interface: http://localhost:8385/admin/

#### Features:
- 📊 **Dashboard** - View repository statistics
- 📤 **Upload Package** - Upload package files via web interface
- 📦 **Manage Packages** - View and delete existing packages

#### Steps:
1. Open your browser and visit http://localhost:8385/admin/
2. Click the "Upload Package" tab
3. Select your package file (supports .whl, .tar.gz, .zip)
4. Optional: Specify package name (leave empty for auto-detection)
5. Click "Upload Package"

### 2. Command Line Management

#### List all packages
```bash
python3 manage_packages.py list
```

#### Upload package
```bash
# Auto-detect package name
python3 manage_packages.py upload --file path/to/package-1.0.0.whl

# Specify package name
python3 manage_packages.py upload --file path/to/package-1.0.0.whl --package my-package
```

#### Delete package
```bash
python3 manage_packages.py remove --package package-name
```

### 3. Advanced Package Management Tools

Use more powerful package management tools:

```bash
# List packages
python3 tools/package_manager.py list

# Upload package
python3 tools/package_manager.py upload --file path/to/package.whl

# Update package
python3 tools/package_manager.py update --package package-name --file path/to/new-version.whl

# Delete package
python3 tools/package_manager.py remove --package package-name

# View package details
python3 tools/package_manager.py info --package package-name
```

## 📋 Supported File Formats

### 1. Wheel Files (.whl)
- **Purpose**: Pre-compiled Python packages
- **Advantage**: Fast installation, no compilation required
- **Example**: `my_package-1.0.0-py3-none-any.whl`

### 2. Source Distribution (.tar.gz)
- **Purpose**: Source packages requiring compilation
- **Advantage**: Good cross-platform compatibility
- **Example**: `my_package-1.0.0.tar.gz`

### 3. ZIP Files (.zip)
- **Purpose**: Compressed source packages
- **Example**: `my_package-1.0.0.zip`

## 🔧 Package Naming Conventions

### Auto-Detection Rules
1. Extract package name from filename
2. Remove version number (e.g., `-1.0.0`)
3. Remove file extension

### Examples
```
Filename: my_package-1.0.0-py3-none-any.whl
Detected package name: my_package

Filename: awesome-tool-2.1.0.tar.gz
Detected package name: awesome-tool
```

## 📁 Package Storage Structure

```
packages/
├── package-name-1/
│   ├── package-name-1.0.0.whl
│   ├── package-name-1.0.0.tar.gz
│   └── index.html (auto-generated)
├── package-name-2/
│   ├── package-name-2.1.0.whl
│   └── index.html
└── ...
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

## 🔍 Monitoring and Management

### Check Repository Status
```bash
# Health check
curl http://localhost:8385/health

# Statistics
curl http://localhost:8385/stats

# Package list
curl http://localhost:8385/packages
```

### View Logs
```bash
# Application logs
tail -f pypi_repo.log

# Monitoring logs
tail -f logs/monitor.log
```

## 🛠️ Troubleshooting

### Common Issues

1. **Upload fails**
   ```bash
   # Check file permissions
   ls -la packages/
   
   # Check disk space
   df -h
   ```

2. **Package won't install**
   ```bash
   # Check if package exists
   curl http://localhost:8385/simple/package-name/
   
   # Check file integrity
   ls -la packages/package-name/
   ```

3. **Web interface inaccessible**
   ```bash
   # Check service status
   ps aux | grep app.py
   
   # Restart service
   ./stop.sh && ./start.sh
   ```

### Performance Optimization

1. **Clear cache**
   ```bash
   # Restart service to clear cache
   ./stop.sh && ./start.sh
   ```

2. **Monitor disk usage**
   ```bash
   # Check package directory size
   du -sh packages/
   ```

## 📚 Advanced Features

### 1. Batch Operations
```bash
# Batch upload multiple packages
for file in dist/*.whl; do
    python3 manage_packages.py upload --file "$file"
done
```

### 2. Package Validation
```bash
# Validate package file integrity
python3 tools/package_manager.py info --package package-name
```

### 3. Automatic Backup
```bash
# Backup package directory
tar -czf packages_backup_$(date +%Y%m%d).tar.gz packages/
```

## 🔐 Security Recommendations

1. **File Permissions**
   ```bash
   # Set appropriate permissions
   chmod 755 packages/
   chmod 644 packages/*/*
   ```

2. **Access Control**
   - Consider adding authentication mechanisms
   - Limit upload file size
   - Validate file types

3. **Backup Strategy**
   - Regularly backup package directory
   - Monitor disk usage
   - Set file size limits

## 📞 Getting Help

- Check log files for detailed error information
- Verify service status to ensure normal operation
- Refer to the troubleshooting section of this document

---

**Note**: This repository supports the standard PyPI Simple Repository API and is fully compatible with pip. 