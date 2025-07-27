"""
Repository Manager - 负责包管理和统计功能
"""

import os
import time
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class RepositoryManager:
    """仓库管理器 - 负责包扫描、缓存和统计"""
    
    def __init__(self, packages_dir: str = "packages"):
        self.packages_dir = Path(packages_dir)
        self.packages_dir.mkdir(exist_ok=True)
        
        # 缓存配置
        self.cache = {}
        self.cache_ttl = 300  # 5分钟缓存
        self.last_scan = 0
        
        # 启动时间
        self.start_time = time.time()
        
        logger.info(f"Repository manager initialized with packages directory: {self.packages_dir}")
    
    def scan_packages(self) -> Dict[str, List[str]]:
        """扫描包目录，返回包名到文件列表的映射"""
        try:
            packages = {}
            
            if not self.packages_dir.exists():
                logger.warning(f"Packages directory does not exist: {self.packages_dir}")
                return packages
            
            for package_dir in self.packages_dir.iterdir():
                if package_dir.is_dir():
                    package_name = package_dir.name
                    files = []
                    
                    # 扫描包目录中的文件
                    for file_path in package_dir.iterdir():
                        if file_path.is_file():
                            files.append(file_path.name)
                    
                    if files:  # 只包含有文件的包
                        packages[package_name] = sorted(files)
            
            logger.info(f"Scanned {len(packages)} packages")
            return packages
            
        except Exception as e:
            logger.error(f"Error scanning packages: {e}")
            return {}
    
    def get_packages(self) -> Dict[str, List[str]]:
        """获取包列表（带缓存）"""
        current_time = time.time()
        
        # 检查缓存是否有效
        if (current_time - self.last_scan) < self.cache_ttl and 'packages' in self.cache:
            return self.cache['packages']
        
        # 重新扫描
        packages = self.scan_packages()
        self.cache['packages'] = packages
        self.last_scan = current_time
        
        return packages
    
    def get_package_files(self, package_name: str) -> List[str]:
        """获取指定包的文件列表"""
        packages = self.get_packages()
        return packages.get(package_name, [])
    
    def get_stats(self) -> Dict[str, Any]:
        """获取仓库统计信息"""
        try:
            packages = self.get_packages()
            packages_count = len(packages)
            files_count = sum(len(files) for files in packages.values())
            
            # 计算总大小
            total_size = 0
            for package_name, files in packages.items():
                package_dir = self.packages_dir / package_name
                for file_name in files:
                    file_path = package_dir / file_name
                    if file_path.exists():
                        total_size += file_path.stat().st_size
            
            total_size_mb = round(total_size / (1024 * 1024), 2)
            
            # 计算运行时间
            uptime = time.time() - self.start_time
            
            stats = {
                'packages_count': packages_count,
                'files_count': files_count,
                'total_size_mb': total_size_mb,
                'uptime': uptime,
                'last_health_check': time.time(),
                'is_healthy': True
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'packages_count': 0,
                'files_count': 0,
                'total_size_mb': 0,
                'uptime': time.time() - self.start_time,
                'last_health_check': time.time(),
                'is_healthy': False
            }
    
    def add_package(self, package_name: str, file_path: str) -> bool:
        """添加包文件到仓库"""
        try:
            package_dir = self.packages_dir / package_name
            package_dir.mkdir(exist_ok=True)
            
            # 复制文件到包目录
            import shutil
            dest_path = package_dir / os.path.basename(file_path)
            shutil.copy2(file_path, dest_path)
            
            # 清除缓存
            self.cache.clear()
            self.last_scan = 0
            
            logger.info(f"Added package file: {package_name}/{os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding package {package_name}: {e}")
            return False
    
    def remove_package(self, package_name: str) -> bool:
        """从仓库中删除包"""
        try:
            package_dir = self.packages_dir / package_name
            if package_dir.exists():
                import shutil
                shutil.rmtree(package_dir)
                
                # 清除缓存
                self.cache.clear()
                self.last_scan = 0
                
                logger.info(f"Removed package: {package_name}")
                return True
            else:
                logger.warning(f"Package directory does not exist: {package_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing package {package_name}: {e}")
            return False 