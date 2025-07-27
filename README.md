# Simple Python Package Repository

这是一个生产级的Python包仓库，具备高可用性、自动恢复和监控功能。

## 功能特性

- ✅ **Simple Repository API** - 完全兼容PyPI Simple Repository规范
- ✅ **高可用性** - 自动进程监控和恢复
- ✅ **健康检查** - 实时服务状态监控
- ✅ **日志记录** - 完整的操作日志和错误追踪
- ✅ **统计信息** - 包数量、文件大小等统计
- ✅ **现代化UI** - 响应式Web界面
- ✅ **生产级部署** - 支持Supervisor和Systemd
- ✅ **自动恢复** - 崩溃时自动重启服务

## 项目结构

```
pypi_repo/
├── app.py                    # Flask应用服务器
├── manage_repo.py            # 包管理脚本
├── monitor.py                # 监控和自动恢复脚本
├── gunicorn.conf.py          # Gunicorn配置
├── supervisor.conf           # Supervisor配置
├── systemd.service           # Systemd服务文件
├── start.sh                  # 启动脚本
├── stop.sh                   # 停止脚本
├── requirements.txt          # Python依赖
├── payo-cli/                 # 示例包目录
│   ├── index.html           # 包索引页面
│   ├── payo_cli-1.0.0.tar.gz
│   └── payo_cli-1.0.0-py3-none-any.whl
└── README.md                # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip3 install -r requirements.txt

# 或者使用系统包管理器
sudo apt-get install supervisor  # Ubuntu/Debian
sudo yum install supervisor      # CentOS/RHEL
```

### 2. 启动服务

```bash
# 一键启动（推荐）
chmod +x start.sh
./start.sh

# 或者手动启动
python3 app.py
```

### 3. 访问服务

- **仓库主页**: http://localhost:8385
- **健康检查**: http://localhost:8385/health
- **统计信息**: http://localhost:8385/stats

## 部署方式

### 方式1: 使用启动脚本（推荐）

```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh

# 查看状态
supervisorctl -c supervisor.conf status pypi_repo
```

### 方式2: 使用Systemd（生产环境）

```bash
# 复制服务文件
sudo cp systemd.service /etc/systemd/system/pypi-repo.service

# 重新加载systemd
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable pypi-repo
sudo systemctl start pypi-repo

# 查看状态
sudo systemctl status pypi-repo
```

### 方式3: 使用Supervisor

```bash
# 启动supervisor
supervisord -c supervisor.conf

# 管理服务
supervisorctl -c supervisor.conf status pypi_repo
supervisorctl -c supervisor.conf restart pypi_repo
supervisorctl -c supervisor.conf stop pypi_repo
```

## 监控和自动恢复

### 监控功能

- **健康检查**: 每分钟检查服务状态
- **自动恢复**: 连续失败3次后自动重启
- **日志记录**: 详细的操作和错误日志
- **告警机制**: 可扩展的告警系统

### 监控脚本

```bash
# 启动监控
python3 monitor.py

# 查看监控日志
tail -f logs/monitor.log
```

### 健康检查API

```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 获取统计信息
curl http://localhost:8000/stats
```

## 包管理

### 添加新包

```bash
# 使用管理脚本
python3 manage_repo.py package-name

# 手动添加
mkdir package-name
cp dist/package_name-*.whl package-name/
cp dist/package_name-*.tar.gz package-name/
```

### 包目录结构

```
package-name/
├── index.html               # 包索引页面
├── package_name-1.0.0.whl   # Wheel分发
└── package_name-1.0.0.tar.gz # 源码分发
```

## 使用仓库

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

## 日志管理

### 日志文件

- `pypi_repo.log` - 应用日志
- `access.log` - 访问日志
- `error.log` - 错误日志
- `supervisor.log` - Supervisor日志
- `logs/monitor.log` - 监控日志

### 查看日志

```bash
# 实时查看应用日志
tail -f pypi_repo.log

# 查看访问日志
tail -f access.log

# 查看监控日志
tail -f logs/monitor.log
```

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   netstat -tlnp | grep 8000
   
   # 检查日志
   tail -f pypi_repo.log
   ```

2. **包无法下载**
   ```bash
   # 检查文件权限
   ls -la package-name/
   
   # 检查健康状态
   curl http://localhost:8000/health
   ```

3. **监控不工作**
   ```bash
   # 检查监控进程
   ps aux | grep monitor.py
   
   # 重启监控
   pkill -f monitor.py
   python3 monitor.py &
   ```

### 性能优化

1. **调整Gunicorn配置**
   ```python
   # 在gunicorn.conf.py中调整
   workers = multiprocessing.cpu_count() * 2 + 1
   worker_connections = 1000
   ```

2. **启用缓存**
   ```python
   # 在app.py中调整缓存时间
   self.cache_ttl = 300  # 5分钟
   ```

## 安全建议

1. **使用HTTPS**
   ```bash
   # 配置SSL证书
   # 修改gunicorn.conf.py中的bind地址
   ```

2. **访问控制**
   ```python
   # 在app.py中添加认证
   # 实现IP白名单或用户认证
   ```

3. **文件权限**
   ```bash
   # 设置适当的文件权限
   chmod 755 package-directories/
   chmod 644 package-files/*
   ```

## 扩展功能

### 添加新功能

1. **包搜索**: 实现包名搜索功能
2. **用户认证**: 添加用户登录和权限控制
3. **包上传**: 实现Web界面上传包
4. **依赖解析**: 添加包依赖关系分析
5. **统计报表**: 生成使用统计报表

### 集成第三方服务

- **邮件告警**: 集成SMTP发送告警邮件
- **监控平台**: 集成Prometheus、Grafana
- **日志聚合**: 集成ELK Stack
- **容器化**: 提供Docker支持

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License

## 参考

- [Python Packaging User Guide](https://packaging.python.org/)
- [Simple Repository API Specification](https://packaging.python.org/en/latest/specifications/simple-repository-api/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Supervisor Documentation](http://supervisord.org/) 