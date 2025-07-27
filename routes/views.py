"""
View Routes - 处理页面渲染和文件服务
"""

import logging
from flask import Blueprint, render_template, send_from_directory, abort, request
from pathlib import Path

logger = logging.getLogger(__name__)

# 创建蓝图
views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def dashboard():
    """管理仪表板主页"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        packages = repo_manager.get_packages()
        stats = repo_manager.get_stats()
        stats['uptime_hours'] = round(stats['uptime'] / 3600, 1)
        
        return render_template('dashboard.html', 
                             packages=packages, 
                             **stats)
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        return "Internal server error", 500


@views_bp.route('/<package_name>/')
def package_page(package_name):
    """包详情页面"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        files = repo_manager.get_package_files(package_name)
        
        if not files:
            abort(404)
        
        # 分析文件类型
        wheel_files = [f for f in files if f.endswith('.whl')]
        source_files = [f for f in files if f.endswith('.tar.gz')]
        
        return render_template('package.html',
                             package_name=package_name,
                             files=files,
                             wheel_files=wheel_files,
                             source_files=source_files)
    except Exception as e:
        logger.error(f"Error rendering package page for {package_name}: {e}")
        return "Internal server error", 500


@views_bp.route('/<package_name>/<filename>')
def download_file(package_name, filename):
    """下载包文件"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        files = repo_manager.get_package_files(package_name)
        
        if filename not in files:
            abort(404)
        
        # 发送文件
        package_dir = Path(repo_manager.packages_dir) / package_name
        return send_from_directory(package_dir, filename)
        
    except Exception as e:
        logger.error(f"Error downloading file {package_name}/{filename}: {e}")
        return "Internal server error", 500


@views_bp.route('/upload')
def upload_page():
    """包上传页面"""
    return render_template('upload.html')


@views_bp.route('/manage')
def manage_page():
    """包管理页面"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        packages = repo_manager.get_packages()
        
        return render_template('manage.html', packages=packages)
    except Exception as e:
        logger.error(f"Error rendering manage page: {e}")
        return "Internal server error", 500 