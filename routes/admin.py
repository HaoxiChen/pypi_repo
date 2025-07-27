"""
Admin Routes - 管理功能路由
包含包上传、删除、管理等功能
"""

import os
import logging
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path

logger = logging.getLogger(__name__)

# 创建蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'whl', 'tar.gz', 'zip'}


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS or \
           filename.endswith('.tar.gz')


@admin_bp.route('/')
def admin_dashboard():
    """管理仪表板"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        packages = repo_manager.get_packages()
        
        # 计算总文件数
        total_files = sum(len(files) for files in packages.values())
        return render_template('admin/dashboard.html', packages=packages, total_files=total_files)
    except Exception as e:
        logger.error(f"Error rendering admin dashboard: {e}")
        return "Internal server error", 500


@admin_bp.route('/upload', methods=['GET', 'POST'])
def upload_package():
    """包上传页面"""
    if request.method == 'POST':
        try:
            # 检查是否有文件
            if 'package_file' not in request.files:
                flash('没有选择文件', 'error')
                return redirect(request.url)
            
            file = request.files['package_file']
            if file.filename == '':
                flash('没有选择文件', 'error')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                # 安全地保存文件名
                filename = secure_filename(file.filename)
                
                # 获取包名（从表单或从文件名推断）
                package_name = request.form.get('package_name', '').strip()
                if not package_name:
                    # 从文件名推断包名
                    if filename.endswith('.whl'):
                        name = filename[:-4]
                    elif filename.endswith('.tar.gz'):
                        name = filename[:-7]
                    elif filename.endswith('.zip'):
                        name = filename[:-4]
                    else:
                        name = filename
                    
                    # 提取包名（去掉版本号）
                    parts = name.split('-')
                    package_name = parts[0] if len(parts) >= 2 else name
                
                # 创建包目录
                packages_dir = Path("packages")
                packages_dir.mkdir(exist_ok=True)
                package_dir = packages_dir / package_name
                package_dir.mkdir(exist_ok=True)
                
                # 保存文件
                file_path = package_dir / filename
                file.save(str(file_path))
                
                # 清除缓存
                from models.repository import RepositoryManager
                repo_manager = RepositoryManager()
                repo_manager.cache.clear()
                repo_manager.last_scan = 0
                
                flash(f'包 {package_name} 上传成功！', 'success')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('不支持的文件类型', 'error')
                return redirect(request.url)
                
        except Exception as e:
            logger.error(f"Error uploading package: {e}")
            flash('上传失败', 'error')
            return redirect(request.url)
    
    return render_template('admin/upload.html')


@admin_bp.route('/packages/<package_name>', methods=['DELETE'])
def delete_package(package_name):
    """删除包"""
    try:
        import shutil
        from models.repository import RepositoryManager
        
        package_dir = Path("packages") / package_name
        if not package_dir.exists():
            return jsonify({'error': '包不存在'}), 404
        
        # 删除包目录
        shutil.rmtree(package_dir)
        
        # 清除缓存
        repo_manager = RepositoryManager()
        repo_manager.cache.clear()
        repo_manager.last_scan = 0
        
        return jsonify({'message': f'包 {package_name} 删除成功'})
        
    except Exception as e:
        logger.error(f"Error deleting package {package_name}: {e}")
        return jsonify({'error': '删除失败'}), 500


@admin_bp.route('/packages/<package_name>/info')
def package_info(package_name):
    """获取包详细信息"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        files = repo_manager.get_package_files(package_name)
        
        if not files:
            return jsonify({'error': '包不存在'}), 404
        
        # 计算文件信息
        package_dir = Path("packages") / package_name
        file_info = {}
        total_size = 0
        
        for file_name in files:
            file_path = package_dir / file_name
            if file_path.exists():
                size = file_path.stat().st_size
                total_size += size
                file_info[file_name] = {
                    'size': size,
                    'size_mb': round(size / (1024 * 1024), 2),
                    'type': 'wheel' if file_name.endswith('.whl') else 'source'
                }
        
        info = {
            'name': package_name,
            'files': file_info,
            'file_count': len(files),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'has_wheel': any(f.endswith('.whl') for f in files),
            'has_source': any(f.endswith('.tar.gz') for f in files)
        }
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Error getting package info for {package_name}: {e}")
        return jsonify({'error': '获取包信息失败'}), 500 