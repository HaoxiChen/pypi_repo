"""
API Routes - 处理API相关的路由
"""

import logging
from flask import Blueprint, jsonify, request, send_from_directory
from pathlib import Path

logger = logging.getLogger(__name__)

# 创建蓝图
api_bp = Blueprint('api', __name__)


@api_bp.route('/health')
def health_check():
    """健康检查端点"""
    try:
        # 这里可以添加更复杂的健康检查逻辑
        # 比如检查数据库连接、文件系统权限等
        return jsonify({
            'status': 'healthy',
            'timestamp': time.time(),
            'service': 'pypi-repository'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }), 500


@api_bp.route('/stats')
def get_stats():
    """获取统计信息"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        stats = repo_manager.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500


@api_bp.route('/simple/')
def simple_index():
    """PyPI Simple Repository API - 仓库索引"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        packages = repo_manager.get_packages()
        
        # 生成Simple Repository格式的HTML
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Simple Package Index</title>
</head>
<body>
    <h1>Simple Package Index</h1>
    <ul>
"""
        
        for package_name in sorted(packages.keys()):
            html_content += f'        <li><a href="{package_name}/">{package_name}</a></li>\n'
        
        html_content += """    </ul>
</body>
</html>"""
        
        return html_content, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        logger.error(f"Error generating simple index: {e}")
        return jsonify({'error': 'Failed to generate index'}), 500


@api_bp.route('/simple/<package_name>/')
def package_index(package_name):
    """PyPI Simple Repository API - 包索引"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        files = repo_manager.get_package_files(package_name)
        
        if not files:
            return jsonify({'error': 'Package not found'}), 404
        
        # 生成包索引HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Links for {package_name}</title>
</head>
<body>
    <h1>Links for {package_name}</h1>
"""
        
        for file_name in files:
            # 确定文件类型
            if file_name.endswith('.whl'):
                file_type = 'bdist_wheel'
            elif file_name.endswith('.tar.gz'):
                file_type = 'sdist'
            else:
                file_type = 'unknown'
            
            # 生成下载链接
            download_url = f"{request.url_root.rstrip('/')}/{package_name}/{file_name}"
            html_content += f'    <a href="{download_url}#sha256=..." data-requires-python=">=3.6">{file_name}</a><br/>\n'
        
        html_content += """</body>
</html>"""
        
        return html_content, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        logger.error(f"Error generating package index for {package_name}: {e}")
        return jsonify({'error': 'Failed to generate package index'}), 500


@api_bp.route('/packages')
def list_packages():
    """获取所有包列表（JSON格式）"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        packages = repo_manager.get_packages()
        return jsonify(packages)
    except Exception as e:
        logger.error(f"Error listing packages: {e}")
        return jsonify({'error': 'Failed to list packages'}), 500


@api_bp.route('/packages/<package_name>')
def get_package_info(package_name):
    """获取特定包的详细信息"""
    try:
        from models.repository import RepositoryManager
        repo_manager = RepositoryManager()
        files = repo_manager.get_package_files(package_name)
        
        if not files:
            return jsonify({'error': 'Package not found'}), 404
        
        # 分析包文件
        package_info = {
            'name': package_name,
            'files': files,
            'file_count': len(files),
            'has_wheel': any(f.endswith('.whl') for f in files),
            'has_source': any(f.endswith('.tar.gz') for f in files),
            'download_urls': {}
        }
        
        # 生成下载URL
        for file_name in files:
            package_info['download_urls'][file_name] = f"{request.url_root.rstrip('/')}/{package_name}/{file_name}"
        
        return jsonify(package_info)
        
    except Exception as e:
        logger.error(f"Error getting package info for {package_name}: {e}")
        return jsonify({'error': 'Failed to get package info'}), 500


# 导入time模块
import time 