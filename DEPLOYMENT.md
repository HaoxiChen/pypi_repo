# PyPI Repository 部署指南

## 系统要求

- **操作系统**: Linux (Ubuntu 18.04+, CentOS 7+, Debian 9+)
- **Python**: 3.7+
- **内存**: 最少 512MB RAM
- **磁盘**: 最少 1GB 可用空间
- **网络**: 可访问互联网（用于安装依赖）

## 快速部署

### 1. 环境准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS/RHEL

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv -y  # Ubuntu/Debian
# 或
sudo yum install python3 python3-pip -y  # CentOS/RHEL

# 安装supervisor
sudo apt install supervisor -y  # Ubuntu/Debian
# 或
sudo yum install supervisor -y  # CentOS/RHEL
```

### 2. 下载和配置

```bash
# 克隆或下载项目
cd /opt
sudo git clone <repository-url> pypi_repo
# 或解压下载的文件
sudo tar -xzf pypi_repo.tar.gz

# 设置权限
sudo chown -R $USER:$USER /opt/pypi_repo
cd /opt/pypi_repo

# 安装Python依赖
pip3 install -r requirements.txt
```

### 3. 配置调整

编辑配置文件以适应你的环境：

```bash
# 修改supervisor配置中的用户和路径
sed -i 's/haoxichen/$USER/g' supervisor.conf
sed -i 's|/home/haoxichen/Desktop/pypi_repo|/opt/pypi_repo|g' supervisor.conf

# 修改systemd服务文件
sed -i 's/haoxichen/$USER/g' systemd.service
sed -i 's|/home/haoxichen/Desktop/pypi_repo|/opt/pypi_repo|g' systemd.service
```

### 4. 启动服务

```bash
# 使用启动脚本（推荐用于测试）
./start.sh

# 或使用systemd（推荐用于生产环境）
sudo cp systemd.service /etc/systemd/system/pypi-repo.service
sudo systemctl daemon-reload
sudo systemctl enable pypi-repo
sudo systemctl start pypi-repo
```

### 5. 验证部署

```bash
# 检查服务状态
curl http://localhost:8385/health

# 运行测试脚本
python3 test_service.py

# 查看日志
tail -f pypi_repo.log
```

## 生产环境部署

### 1. 使用Nginx反向代理

创建Nginx配置：

```nginx
# /etc/nginx/sites-available/pypi-repo
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8385;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/pypi-repo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. SSL证书配置

使用Let's Encrypt：

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. 防火墙配置

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 4. 监控和告警

配置监控脚本：

```bash
# 创建监控服务
sudo cp systemd.service /etc/systemd/system/pypi-repo-monitor.service
# 修改ExecStart为：/opt/pypi_repo/monitor.py

# 启用监控
sudo systemctl enable pypi-repo-monitor
sudo systemctl start pypi-repo-monitor
```

## 高可用性配置

### 1. 负载均衡

使用HAProxy配置负载均衡：

```haproxy
# /etc/haproxy/haproxy.cfg
global
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend pypi_frontend
    bind *:80
    default_backend pypi_backend

backend pypi_backend
    balance roundrobin
    server pypi1 127.0.0.1:8000 check
    server pypi2 127.0.0.1:8001 check
```

### 2. 数据库存储

对于大型仓库，考虑使用数据库存储包元数据：

```python
# 在app.py中添加数据库支持
import sqlite3

def init_database():
    conn = sqlite3.connect('packages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            version TEXT,
            filename TEXT,
            file_size INTEGER,
            upload_time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
```

### 3. 备份策略

创建备份脚本：

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup/pypi_repo"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份包文件
tar -czf $BACKUP_DIR/packages_$DATE.tar.gz payo-cli/

# 备份配置和日志
tar -czf $BACKUP_DIR/config_$DATE.tar.gz *.conf *.py *.sh

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 性能优化

### 1. Gunicorn调优

```python
# gunicorn.conf.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
```

### 2. 缓存配置

```python
# 在app.py中启用缓存
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})
```

### 3. 静态文件优化

```nginx
# Nginx配置静态文件缓存
location ~* \.(whl|tar\.gz)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    proxy_pass http://127.0.0.1:8000;
}
```

## 安全配置

### 1. 访问控制

```python
# 在app.py中添加IP白名单
ALLOWED_IPS = ['192.168.1.0/24', '10.0.0.0/8']

@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if not any(ipaddress.ip_address(client_ip) in ipaddress.ip_network(allowed) 
               for allowed in ALLOWED_IPS):
        abort(403)
```

### 2. 包签名验证

```python
# 添加包签名验证
import hashlib

def verify_package_signature(file_path, expected_hash):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash
```

### 3. 日志审计

```python
# 添加详细的访问日志
@app.after_request
def log_request(response):
    logger.info(f'{request.remote_addr} - {request.method} {request.url} - {response.status_code}')
    return response
```

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   netstat -tlnp | grep 8000
   
   # 检查日志
   tail -f pypi_repo.log
   
   # 检查权限
   ls -la /opt/pypi_repo/
   ```

2. **包下载失败**
   ```bash
   # 检查文件权限
   ls -la payo-cli/
   
   # 检查网络连接
   curl -I http://localhost:8000/health
   ```

3. **监控不工作**
   ```bash
   # 检查监控进程
   ps aux | grep monitor.py
   
   # 检查监控日志
   tail -f logs/monitor.log
   ```

### 性能问题

1. **响应慢**
   ```bash
   # 检查系统资源
   top
   iostat -x 1
   
   # 检查网络
   netstat -i
   ```

2. **内存不足**
   ```bash
   # 调整Gunicorn配置
   workers = 2  # 减少worker数量
   ```

## 维护和更新

### 1. 定期维护

```bash
# 创建维护脚本
#!/bin/bash
# maintenance.sh

# 清理日志
find /opt/pypi_repo -name "*.log" -mtime +30 -delete

# 更新包索引
python3 manage_repo.py --update-all

# 检查磁盘空间
df -h /opt/pypi_repo

# 重启服务
sudo systemctl restart pypi-repo
```

### 2. 版本升级

```bash
# 备份当前版本
cp -r /opt/pypi_repo /opt/pypi_repo_backup

# 下载新版本
cd /opt
wget https://github.com/user/pypi_repo/archive/v2.0.0.tar.gz
tar -xzf v2.0.0.tar.gz

# 迁移配置
cp /opt/pypi_repo_backup/*.conf /opt/pypi_repo-2.0.0/
cp /opt/pypi_repo_backup/payo-cli/ /opt/pypi_repo-2.0.0/

# 测试新版本
cd /opt/pypi_repo-2.0.0
python3 test_service.py

# 切换版本
sudo systemctl stop pypi-repo
sudo ln -sf /opt/pypi_repo-2.0.0 /opt/pypi_repo
sudo systemctl start pypi-repo
```

## 监控和告警

### 1. 系统监控

使用Prometheus + Grafana：

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'pypi_repo'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### 2. 日志监控

使用ELK Stack：

```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  paths:
    - /opt/pypi_repo/*.log
  fields:
    service: pypi_repo
```

### 3. 告警配置

```python
# 在monitor.py中添加告警
def send_alert(message, level='warning'):
    if level == 'critical':
        # 发送邮件
        send_email('admin@company.com', 'PyPI Repo Alert', message)
        # 发送短信
        send_sms('+1234567890', message)
    elif level == 'warning':
        # 发送Slack通知
        send_slack_webhook(message)
```

这个部署指南涵盖了从基本部署到生产环境配置的各个方面，确保你的PyPI仓库能够稳定、安全、高效地运行。 