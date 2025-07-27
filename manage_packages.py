#!/usr/bin/env python3
"""
Simple Package Manager - 简单的包管理脚本
支持上传、删除、列出包
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def upload_package(file_path, package_name=None):
    """上传包文件"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 验证文件类型
    if not file_path.name.endswith(('.whl', '.tar.gz', '.zip')):
        print(f"❌ 不支持的文件类型: {file_path.name}")
        return False
    
    # 如果没有指定包名，从文件名推断
    if package_name is None:
        if file_path.name.endswith('.whl'):
            name = file_path.name[:-4]
        elif file_path.name.endswith('.tar.gz'):
            name = file_path.name[:-7]
        elif file_path.name.endswith('.zip'):
            name = file_path.name[:-4]
        else:
            name = file_path.name
        
        # 提取包名（去掉版本号）
        parts = name.split('-')
        package_name = parts[0] if len(parts) >= 2 else name
    
    # 创建包目录
    packages_dir = Path("packages")
    packages_dir.mkdir(exist_ok=True)
    package_dir = packages_dir / package_name
    package_dir.mkdir(exist_ok=True)
    
    # 复制文件
    dest_path = package_dir / file_path.name
    shutil.copy2(file_path, dest_path)
    
    print(f"✅ 包上传成功: {package_name}/{file_path.name}")
    return True

def remove_package(package_name):
    """删除包"""
    package_dir = Path("packages") / package_name
    if not package_dir.exists():
        print(f"❌ 包不存在: {package_name}")
        return False
    
    # 删除包目录
    shutil.rmtree(package_dir)
    print(f"✅ 包删除成功: {package_name}")
    return True

def list_packages():
    """列出所有包"""
    packages_dir = Path("packages")
    if not packages_dir.exists():
        print("📦 没有找到包")
        return
    
    packages = {}
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir():
            files = [f.name for f in package_dir.iterdir() if f.is_file()]
            packages[package_dir.name] = files
    
    if packages:
        print("📦 已安装的包:")
        for name, files in packages.items():
            print(f"  {name}: {len(files)} 个文件")
            for file in files:
                file_type = "Wheel" if file.endswith('.whl') else "Source"
                print(f"    - {file} ({file_type})")
    else:
        print("📦 没有找到包")

def main():
    parser = argparse.ArgumentParser(description='Simple Package Manager')
    parser.add_argument('action', choices=['upload', 'remove', 'list'],
                       help='操作类型')
    parser.add_argument('--file', '-f', help='包文件路径')
    parser.add_argument('--package', '-p', help='包名')
    
    args = parser.parse_args()
    
    if args.action == 'upload':
        if not args.file:
            print("❌ 错误: 上传包需要指定文件路径 (--file)")
            sys.exit(1)
        success = upload_package(args.file, args.package)
        sys.exit(0 if success else 1)
    
    elif args.action == 'remove':
        if not args.package:
            print("❌ 错误: 删除包需要指定包名 (--package)")
            sys.exit(1)
        success = remove_package(args.package)
        sys.exit(0 if success else 1)
    
    elif args.action == 'list':
        list_packages()

if __name__ == '__main__':
    main() 