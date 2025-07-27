#!/usr/bin/env python3
"""
PyPI Repository Monitor and Auto-Recovery Script
"""

import os
import sys
import time
import json
import logging
import requests
import subprocess
import signal
from pathlib import Path
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RepositoryMonitor:
    """仓库监控器"""
    
    def __init__(self, repo_url="http://localhost:8385", check_interval=60):
        self.repo_url = repo_url
        self.check_interval = check_interval
        self.last_healthy = None
        self.consecutive_failures = 0
        self.max_failures = 3
        self.recovery_attempts = 0
        self.max_recovery_attempts = 5
        
    def check_health(self):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.repo_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.consecutive_failures = 0
                    self.last_healthy = datetime.now()
                    logger.info("Service is healthy")
                    return True
                else:
                    logger.warning(f"Service reports unhealthy status: {data}")
                    return False
            else:
                logger.error(f"Health check failed with status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during health check: {e}")
            return False
    
    def check_stats(self):
        """检查服务统计信息"""
        try:
            response = requests.get(f"{self.repo_url}/stats", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                logger.info(f"Service stats: {stats}")
                return stats
            else:
                logger.error(f"Stats check failed with status code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Stats check failed: {e}")
            return None
    
    def restart_service(self):
        """重启服务"""
        try:
            logger.info("Attempting to restart service...")
            
            # 使用supervisor重启
            result = subprocess.run(
                ['supervisorctl', '-c', 'supervisor.conf', 'restart', 'pypi_repo'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("Service restart command executed successfully")
                return True
            else:
                logger.error(f"Service restart failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Service restart timed out")
            return False
        except Exception as e:
            logger.error(f"Service restart error: {e}")
            return False
    
    def check_supervisor_status(self):
        """检查supervisor状态"""
        try:
            result = subprocess.run(
                ['supervisorctl', '-c', 'supervisor.conf', 'status', 'pypi_repo'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                status = result.stdout.strip()
                logger.info(f"Supervisor status: {status}")
                return 'RUNNING' in status
            else:
                logger.error(f"Supervisor status check failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Supervisor status check error: {e}")
            return False
    
    def start_supervisor(self):
        """启动supervisor"""
        try:
            logger.info("Starting supervisor...")
            result = subprocess.run(
                ['supervisord', '-c', 'supervisor.conf'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("Supervisor started successfully")
                return True
            else:
                logger.error(f"Supervisor start failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Supervisor start error: {e}")
            return False
    
    def recover_service(self):
        """恢复服务"""
        logger.info(f"Attempting service recovery (attempt {self.recovery_attempts + 1}/{self.max_recovery_attempts})")
        
        # 检查supervisor是否运行
        if not self.check_supervisor_status():
            logger.info("Supervisor not running, starting it...")
            if not self.start_supervisor():
                logger.error("Failed to start supervisor")
                return False
            time.sleep(5)  # 等待supervisor启动
        
        # 重启服务
        if self.restart_service():
            self.recovery_attempts += 1
            time.sleep(10)  # 等待服务启动
            
            # 检查是否恢复
            if self.check_health():
                logger.info("Service recovered successfully")
                self.recovery_attempts = 0
                return True
            else:
                logger.warning("Service restart did not resolve the issue")
                return False
        else:
            logger.error("Failed to restart service")
            return False
    
    def send_alert(self, message):
        """发送告警（可以扩展为邮件、短信等）"""
        logger.error(f"ALERT: {message}")
        # 这里可以添加邮件、短信、钉钉等告警方式
        # 例如：发送到日志文件、邮件、webhook等
    
    def run(self):
        """运行监控"""
        logger.info("Starting PyPI repository monitor...")
        
        while True:
            try:
                # 检查健康状态
                is_healthy = self.check_health()
                
                if is_healthy:
                    # 服务健康，检查统计信息
                    self.check_stats()
                    
                    # 重置恢复尝试计数
                    if self.recovery_attempts > 0:
                        logger.info("Service is healthy, resetting recovery attempts")
                        self.recovery_attempts = 0
                        
                else:
                    # 服务不健康
                    self.consecutive_failures += 1
                    logger.warning(f"Service unhealthy (failure {self.consecutive_failures}/{self.max_failures})")
                    
                    # 连续失败达到阈值，尝试恢复
                    if self.consecutive_failures >= self.max_failures:
                        if self.recovery_attempts < self.max_recovery_attempts:
                            if self.recover_service():
                                self.consecutive_failures = 0
                            else:
                                # 恢复失败，发送告警
                                self.send_alert(f"Service recovery failed after {self.recovery_attempts} attempts")
                        else:
                            # 达到最大恢复尝试次数
                            self.send_alert(f"Service recovery failed after {self.max_recovery_attempts} attempts. Manual intervention required.")
                            logger.error("Maximum recovery attempts reached, stopping monitor")
                            break
                
                # 等待下次检查
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(self.check_interval)

def signal_handler(signum, frame):
    """信号处理器"""
    logger.info(f"Received signal {signum}, shutting down monitor...")
    sys.exit(0)

if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建监控器
    monitor = RepositoryMonitor()
    
    # 运行监控
    monitor.run() 