# 🚀 Quick Start Guide

Start your private PyPI repository in 5 minutes!

## 📋 Prerequisites

- Python 3.7+
- Linux/macOS/Windows
- Internet connection (for first-time dependency installation)

## ⚡ 5-Minute Quick Start

### 1. Download the Project

```bash
# Clone the project (if you have git)
git clone <repository-url>
cd pypi_repo

# Or download and extract directly
# Then enter the project directory
cd pypi_repo
```

### 2. One-Click Startup

```bash
# Give execute permission to startup script
chmod +x start.sh

# Start the service
./start.sh
```

### 3. Verify Startup

```bash
# Check service status
curl http://localhost:8385/health

# Should return:
# {"service": "pypi-repository", "status": "healthy", "timestamp": ...}
```

### 4. Access the Interface

Open your browser and visit:
- **Repository Homepage**: http://localhost:8385
- **Management Interface**: http://localhost:8385/admin/

## 📦 Upload Your First Package

### Method 1: Web Interface (Recommended)

1. Visit http://localhost:8385/admin/
2. Click the "Upload Package" tab
3. Select your package file (.whl or .tar.gz)
4. Click "Upload Package"

### Method 2: Command Line

```bash
# Upload a package
python3 manage_packages.py upload --file my-package-1.0.0.whl

# List packages
python3 manage_packages.py list
```

## 🌐 Using the Repository

### Installing Packages

```bash
# Install package from your repository
pip install --extra-index-url http://localhost:8385/ my-package

# Permanent configuration (recommended)
pip config set global.extra-index-url http://localhost:8385/
pip install my-package
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

## 🛠️ Common Commands

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
```

## 📊 Check Status

```bash
# Health check
curl http://localhost:8385/health

# Statistics
curl http://localhost:8385/stats

# Package list
curl http://localhost:8385/packages
```

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check port usage
netstat -tlnp | grep 8385

# Check logs
tail -f pypi_repo.log

# Restart service
./stop.sh && ./start.sh
```

### Package Upload Fails

```bash
# Check file permissions
ls -la packages/

# Check disk space
df -h

# Manually create directory
mkdir -p packages
```

### Package Won't Install

```bash
# Check if package exists
curl http://localhost:8385/simple/package-name/

# Check health status
curl http://localhost:8385/health
```

## 📚 Next Steps

- View [Complete Documentation](README_EN.md)
- Learn [Package Management](PACKAGE_MANAGEMENT_EN.md)
- Understand [Deployment Options](DEPLOYMENT_EN.md)

## 🎉 Congratulations!

You have successfully started your private PyPI repository! Now you can:
- Upload and manage Python packages
- Install packages via pip
- Use web interface for management
- Enjoy the convenience of a private repository

---

**Need help?** Check log files or refer to complete documentation. 