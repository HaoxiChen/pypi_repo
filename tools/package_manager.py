"""
Package Manager - 包管理工具
支持上传、更新、删除Python包
"""

import os
import sys
import shutil
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.repository import RepositoryManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PackageManager:
    """包管理器"""
    
    def __init__(self, packages_dir: str = "packages"):
        self.repo_manager = RepositoryManager(packages_dir)
        self.packages_dir = Path(packages_dir)
        self.packages_dir.mkdir(exist_ok=True)
    
    def upload_package(self, file_path: str, package_name: Optional[str] = None) -> bool:
        """上传包文件"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return False
            
            # 验证文件类型
            if not self._is_valid_package_file(file_path.name):
                logger.error(f"不支持的文件类型: {file_path.name}")
                return False
            
            # 如果没有指定包名，从文件名推断
            if package_name is None:
                package_name = self._extract_package_name(file_path.name)
            
            if not package_name:
                logger.error(f"无法从文件名推断包名: {file_path.name}")
                return False
            
            # 创建包目录
            package_dir = self.packages_dir / package_name
            package_dir.mkdir(exist_ok=True)
            
            # 复制文件
            dest_path = package_dir / file_path.name
            shutil.copy2(file_path, dest_path)
            
            # 清除缓存
            self.repo_manager.cache.clear()
            self.repo_manager.last_scan = 0
            
            logger.info(f"包上传成功: {package_name}/{file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"上传包失败: {e}")
            return False
    
    def update_package(self, package_name: str, file_path: str) -> bool:
        """更新包文件"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return False
            
            # 检查包是否存在
            package_dir = self.packages_dir / package_name
            if not package_dir.exists():
                logger.error(f"包不存在: {package_name}")
                return False
            
            # 复制文件（覆盖）
            dest_path = package_dir / file_path.name
            shutil.copy2(file_path, dest_path)
            
            # 清除缓存
            self.repo_manager.cache.clear()
            self.repo_manager.last_scan = 0
            
            logger.info(f"包更新成功: {package_name}/{file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"更新包失败: {e}")
            return False
    
    def remove_package(self, package_name: str) -> bool:
        """删除包"""
        try:
            package_dir = self.packages_dir / package_name
            if not package_dir.exists():
                logger.error(f"包不存在: {package_name}")
                return False
            
            # 删除包目录
            shutil.rmtree(package_dir)
            
            # 清除缓存
            self.repo_manager.cache.clear()
            self.repo_manager.last_scan = 0
            
            logger.info(f"包删除成功: {package_name}")
            return True
            
        except Exception as e:
            logger.error(f"删除包失败: {e}")
            return False
    
    def list_packages(self) -> dict:
        """列出所有包"""
        return self.repo_manager.get_packages()
    
    def get_package_info(self, package_name: str) -> Optional[dict]:
        """获取包信息"""
        try:
            files = self.repo_manager.get_package_files(package_name)
            if not files:
                return None
            
            package_dir = self.packages_dir / package_name
            
            # 计算文件大小
            total_size = 0
            file_info = {}
            for file_name in files:
                file_path = package_dir / file_name
                if file_path.exists():
                    size = file_path.stat().st_size
                    total_size += size
                    file_info[file_name] = {
                        'size': size,
                        'size_mb': round(size / (1024 * 1024), 2),
                        'type': self._get_file_type(file_name)
                    }
            
            return {
                'name': package_name,
                'files': file_info,
                'file_count': len(files),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'has_wheel': any(f.endswith('.whl') for f in files),
                'has_source': any(f.endswith('.tar.gz') for f in files)
            }
            
        except Exception as e:
            logger.error(f"获取包信息失败: {e}")
            return None
    
    def _is_valid_package_file(self, filename: str) -> bool:
        """检查是否为有效的包文件"""
        valid_extensions = {'.whl', '.tar.gz', '.zip'}
        return any(filename.endswith(ext) for ext in valid_extensions)
    
    def _extract_package_name(self, filename: str) -> Optional[str]:
        """从文件名提取包名"""
        # 移除扩展名
        if filename.endswith('.whl'):
            name = filename[:-4]
        elif filename.endswith('.tar.gz'):
            name = filename[:-7]
        elif filename.endswith('.zip'):
            name = filename[:-4]
        else:
            return None
        
        # 提取包名（去掉版本号）
        parts = name.split('-')
        if len(parts) >= 2:
            return parts[0]
        return name
    
    def _get_file_type(self, filename: str) -> str:
        """获取文件类型"""
        if filename.endswith('.whl'):
            return 'wheel'
        elif filename.endswith('.tar.gz'):
            return 'source'
        elif filename.endswith('.zip'):
            return 'zip'
        return 'unknown'


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='PyPI Repository Package Manager')
    parser.add_argument('action', choices=['upload', 'update', 'remove', 'list', 'info'],
                       help='操作类型')
    parser.add_argument('--file', '-f', help='包文件路径')
    parser.add_argument('--package', '-p', help='包名')
    parser.add_argument('--packages-dir', '-d', default='packages',
                       help='包存储目录')
    
    args = parser.parse_args()
    
    manager = PackageManager(args.packages_dir)
    
    if args.action == 'upload':
        if not args.file:
            print("错误: 上传包需要指定文件路径 (--file)")
            sys.exit(1)
        success = manager.upload_package(args.file, args.package)
        sys.exit(0 if success else 1)
    
    elif args.action == 'update':
        if not args.file or not args.package:
            print("错误: 更新包需要指定文件路径 (--file) 和包名 (--package)")
            sys.exit(1)
        success = manager.update_package(args.package, args.file)
        sys.exit(0 if success else 1)
    
    elif args.action == 'remove':
        if not args.package:
            print("错误: 删除包需要指定包名 (--package)")
            sys.exit(1)
        success = manager.remove_package(args.package)
        sys.exit(0 if success else 1)
    
    elif args.action == 'list':
        packages = manager.list_packages()
        if packages:
            print("已安装的包:")
            for name, files in packages.items():
                print(f"  {name}: {len(files)} 个文件")
                for file in files:
                    print(f"    - {file}")
        else:
            print("没有找到包")
    
    elif args.action == 'info':
        if not args.package:
            print("错误: 查看包信息需要指定包名 (--package)")
            sys.exit(1)
        info = manager.get_package_info(args.package)
        if info:
            print(f"包信息: {args.package}")
            print(f"  文件数量: {info['file_count']}")
            print(f"  总大小: {info['total_size_mb']} MB")
            print(f"  包含Wheel: {info['has_wheel']}")
            print(f"  包含源码: {info['has_source']}")
            print("  文件列表:")
            for file_name, file_info in info['files'].items():
                print(f"    - {file_name} ({file_info['type']}, {file_info['size_mb']} MB)")
        else:
            print(f"包不存在: {args.package}")
            sys.exit(1)


if __name__ == '__main__':
    main() 