# 📦 包管理使用指南

本指南介绍如何使用PyPI仓库的包管理功能，包括上传、更新、删除和管理包。

## 🚀 快速开始

### 1. Web界面管理（推荐）

访问管理界面：http://localhost:8385/admin/

#### 功能特性：
- 📊 **仪表板** - 查看仓库统计信息
- 📤 **上传包** - 通过Web界面上传包文件
- 📦 **管理包** - 查看、删除现有包

#### 使用步骤：
1. 打开浏览器访问 http://localhost:8385/admin/
2. 点击"Upload Package"标签页
3. 选择包文件（支持 .whl, .tar.gz, .zip）
4. 可选：指定包名（留空则自动检测）
5. 点击"Upload Package"上传

### 2. 命令行管理

#### 列出所有包
```bash
python3 manage_packages.py list
```

#### 上传包
```bash
# 自动检测包名
python3 manage_packages.py upload --file path/to/package-1.0.0.whl

# 指定包名
python3 manage_packages.py upload --file path/to/package-1.0.0.whl --package my-package
```

#### 删除包
```bash
python3 manage_packages.py remove --package package-name
```

### 3. 高级包管理工具

使用功能更强大的包管理工具：

```bash
# 列出包
python3 tools/package_manager.py list

# 上传包
python3 tools/package_manager.py upload --file path/to/package.whl

# 更新包
python3 tools/package_manager.py update --package package-name --file path/to/new-version.whl

# 删除包
python3 tools/package_manager.py remove --package package-name

# 查看包详细信息
python3 tools/package_manager.py info --package package-name
```

## 📋 支持的文件格式

### 1. Wheel文件 (.whl)
- **用途**: 预编译的Python包
- **优势**: 安装速度快，无需编译
- **示例**: `my_package-1.0.0-py3-none-any.whl`

### 2. 源码分发 (.tar.gz)
- **用途**: 源码包，需要编译安装
- **优势**: 跨平台兼容性好
- **示例**: `my_package-1.0.0.tar.gz`

### 3. ZIP文件 (.zip)
- **用途**: 压缩的源码包
- **示例**: `my_package-1.0.0.zip`

## 🔧 包命名规范

### 自动检测规则
1. 从文件名中提取包名
2. 移除版本号（如 `-1.0.0`）
3. 移除文件扩展名

### 示例
```
文件名: my_package-1.0.0-py3-none-any.whl
检测包名: my_package

文件名: awesome-tool-2.1.0.tar.gz
检测包名: awesome-tool
```

## 📁 包存储结构

```
packages/
├── package-name-1/
│   ├── package-name-1.0.0.whl
│   ├── package-name-1.0.0.tar.gz
│   └── index.html (自动生成)
├── package-name-2/
│   ├── package-name-2.1.0.whl
│   └── index.html
└── ...
```

## 🌐 使用仓库

### 安装包
```bash
# 从仓库安装
pip install --extra-index-url http://localhost:8385/ package-name

# 安装特定版本
pip install --extra-index-url http://localhost:8385/ package-name==1.0.0

# 永久配置
pip config set global.extra-index-url http://localhost:8385/
pip install package-name
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

## 🔍 监控和管理

### 查看仓库状态
```bash
# 健康检查
curl http://localhost:8385/health

# 统计信息
curl http://localhost:8385/stats

# 包列表
curl http://localhost:8385/packages
```

### 查看日志
```bash
# 应用日志
tail -f pypi_repo.log

# 监控日志
tail -f logs/monitor.log
```

## 🛠️ 故障排除

### 常见问题

1. **上传失败**
   ```bash
   # 检查文件权限
   ls -la packages/
   
   # 检查磁盘空间
   df -h
   ```

2. **包无法安装**
   ```bash
   # 检查包是否存在
   curl http://localhost:8385/simple/package-name/
   
   # 检查文件完整性
   ls -la packages/package-name/
   ```

3. **Web界面无法访问**
   ```bash
   # 检查服务状态
   ps aux | grep app.py
   
   # 重启服务
   ./stop.sh && ./start.sh
   ```

### 性能优化

1. **清理缓存**
   ```bash
   # 重启服务清除缓存
   ./stop.sh && ./start.sh
   ```

2. **监控磁盘使用**
   ```bash
   # 查看包目录大小
   du -sh packages/
   ```

## 📚 高级功能

### 1. 批量操作
```bash
# 批量上传多个包
for file in dist/*.whl; do
    python3 manage_packages.py upload --file "$file"
done
```

### 2. 包验证
```bash
# 验证包文件完整性
python3 tools/package_manager.py info --package package-name
```

### 3. 自动备份
```bash
# 备份包目录
tar -czf packages_backup_$(date +%Y%m%d).tar.gz packages/
```

## 🔐 安全建议

1. **文件权限**
   ```bash
   # 设置适当的权限
   chmod 755 packages/
   chmod 644 packages/*/*
   ```

2. **访问控制**
   - 考虑添加认证机制
   - 限制上传文件大小
   - 验证文件类型

3. **备份策略**
   - 定期备份包目录
   - 监控磁盘使用情况
   - 设置文件大小限制

## 📞 获取帮助

- 查看日志文件了解详细错误信息
- 检查服务状态确保正常运行
- 参考本文档的故障排除部分

---

**注意**: 本仓库支持标准的PyPI Simple Repository API，与pip完全兼容。 