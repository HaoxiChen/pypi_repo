# 🚀 快速开始指南

5分钟内启动你的私有PyPI仓库！

## 📋 前置要求

- Python 3.7+
- Linux/macOS/Windows
- 网络连接（首次安装依赖）

## ⚡ 5分钟快速启动

### 1. 下载项目

```bash
# 克隆项目（如果有git）
git clone <repository-url>
cd pypi_repo

# 或者直接下载并解压
# 然后进入项目目录
cd pypi_repo
```

### 2. 一键启动

```bash
# 给启动脚本执行权限
chmod +x start.sh

# 启动服务
./start.sh
```

### 3. 验证启动

```bash
# 检查服务状态
curl http://localhost:8385/health

# 应该返回：
# {"service": "pypi-repository", "status": "healthy", "timestamp": ...}
```

### 4. 访问界面

打开浏览器访问：
- **仓库主页**: http://localhost:8385
- **管理界面**: http://localhost:8385/admin/

## 📦 上传第一个包

### 方法1: Web界面（推荐）

1. 访问 http://localhost:8385/admin/
2. 点击"Upload Package"标签
3. 选择你的包文件（.whl 或 .tar.gz）
4. 点击"Upload Package"

### 方法2: 命令行

```bash
# 上传包
python3 manage_packages.py upload --file my-package-1.0.0.whl

# 查看包列表
python3 manage_packages.py list
```

## 🌐 使用仓库

### 安装包

```bash
# 从你的仓库安装包
pip install --extra-index-url http://localhost:8385/ my-package

# 永久配置（推荐）
pip config set global.extra-index-url http://localhost:8385/
pip install my-package
```

### 配置pip

```bash
# 创建pip配置文件
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
extra-index-url = http://localhost:8385/
trusted-host = localhost
EOF
```

## 🛠️ 常用命令

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
```

## 📊 检查状态

```bash
# 健康检查
curl http://localhost:8385/health

# 统计信息
curl http://localhost:8385/stats

# 包列表
curl http://localhost:8385/packages
```

## 🔧 故障排除

### 服务无法启动

```bash
# 检查端口占用
netstat -tlnp | grep 8385

# 检查日志
tail -f pypi_repo.log

# 重启服务
./stop.sh && ./start.sh
```

### 包上传失败

```bash
# 检查文件权限
ls -la packages/

# 检查磁盘空间
df -h

# 手动创建目录
mkdir -p packages
```

### 包无法安装

```bash
# 检查包是否存在
curl http://localhost:8385/simple/package-name/

# 检查健康状态
curl http://localhost:8385/health
```

## 📚 下一步

- 查看 [完整文档](README.md)
- 学习 [包管理](PACKAGE_MANAGEMENT.md)
- 了解 [部署选项](DEPLOYMENT.md)

## 🎉 恭喜！

你已经成功启动了私有PyPI仓库！现在可以：
- 上传和管理Python包
- 通过pip安装包
- 使用Web界面管理
- 享受私有仓库的便利

---

**需要帮助？** 查看日志文件或参考完整文档。 