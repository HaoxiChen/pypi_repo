# 🐍 PyPI Private Repository

<div align="center">

# 🌍 语言选择 / Language Selection

| 语言 / Language | 文档 / Documentation |
|----------------|---------------------|
| 🇨🇳 **中文** | [完整中文文档](README.md#-中文版本) |
| 🇺🇸 **English** | [Complete English Documentation](README.md#-english-version) |

---

</div>

## 🚀 快速开始 / Quick Start

### 中文用户 / Chinese Users
点击上方 **[完整中文文档](README.md#-中文版本)** 查看详细中文说明

### English Users
Click **[Complete English Documentation](README.md#-english-version)** above for detailed English instructions

## ⚡ 一键启动 / One-Click Startup

```bash
# 启动服务 / Start Service
chmod +x start.sh
./start.sh

# 访问地址 / Access URLs
# 主页 / Homepage: http://localhost:8385
# 管理 / Admin: http://localhost:8385/admin/
# 健康检查 / Health: http://localhost:8385/health
```

## 📦 包管理 / Package Management

### Web界面 / Web Interface
访问 http://localhost:8385/admin/ 使用Web界面管理包

### 命令行 / Command Line
```bash
# 列出包 / List packages
python3 manage_packages.py list

# 上传包 / Upload package
python3 manage_packages.py upload --file package.whl

# 删除包 / Remove package
python3 manage_packages.py remove --package package-name
```

## 🌐 使用仓库 / Using Repository

```bash
# 安装包 / Install package
pip install --extra-index-url http://localhost:8385/ package-name

# 永久配置 / Permanent config
pip config set global.extra-index-url http://localhost:8385/
```

## 📚 详细文档 / Detailed Documentation

- [语言选择指南](LANGUAGE.md) - Language selection guide
- [包管理指南](PACKAGE_MANAGEMENT.md) - Package management guide
- [API文档](API.md) - API documentation
- [部署指南](DEPLOYMENT.md) - Deployment guide

---

<div align="center">

**🎉 开始使用 / Get Started**: `./start.sh`

</div> 