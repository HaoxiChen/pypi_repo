"""
PyPI Simple Repository Server

重构后的简洁版本，使用模块化架构。
"""

import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# 导入配置和路由
from config.settings import get_config
from routes.api import api_bp
from routes.views import views_bp
from routes.admin import admin_bp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pypi_repo.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    config = get_config()
    app.config.from_object(config)
    config.init_app(app)
    
    # 中间件
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(admin_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("Starting PyPI repository server...")
    app.run(
        host=app.config['HOST'], 
        port=app.config['PORT'], 
        debug=app.config['DEBUG']
    ) 