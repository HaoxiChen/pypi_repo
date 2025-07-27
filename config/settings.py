"""
应用配置设置
"""

import os
from pathlib import Path

# 基础配置
class Config:
    """基础配置类"""
    
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 8385
    
    # 包仓库配置
    PACKAGES_DIR = os.environ.get('PACKAGES_DIR') or 'packages'
    CACHE_TTL = int(os.environ.get('CACHE_TTL') or 300)  # 5分钟缓存
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'pypi_repo.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 监控配置
    HEALTH_CHECK_INTERVAL = int(os.environ.get('HEALTH_CHECK_INTERVAL') or 60)  # 秒
    MAX_FAILURE_COUNT = int(os.environ.get('MAX_FAILURE_COUNT') or 3)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.whl', '.tar.gz', '.zip'}
    
    # 安全配置
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # 生产环境日志配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/pypi_repo.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('PyPI Repository startup')


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    PACKAGES_DIR = 'test_packages'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """获取当前环境配置"""
    config_name = os.environ.get('FLASK_ENV') or 'default'
    return config[config_name] 