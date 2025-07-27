#!/usr/bin/env python3
"""
Gunicorn configuration for PyPI repository server
"""

import multiprocessing
import os

# 服务器配置
bind = "0.0.0.0:8385"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 超时配置
timeout = 30
keepalive = 2
graceful_timeout = 30

# 日志配置
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程配置
preload_app = True
daemon = False
pidfile = "gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 环境变量
raw_env = [
    "PYTHONPATH=/home/haoxichen/Desktop/pypi_repo",
]

def when_ready(server):
    """服务器启动完成时的回调"""
    server.log.info("PyPI repository server is ready to serve requests")

def worker_int(worker):
    """工作进程中断时的回调"""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """fork工作进程前的回调"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """fork工作进程后的回调"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """工作进程初始化后的回调"""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    """工作进程异常退出时的回调"""
    worker.log.info("Worker aborted (pid: %s)", worker.pid) 