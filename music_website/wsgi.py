"""
WSGI配置文件

用于生产部署Django应用
"""

import os

from django.core.wsgi import get_wsgi_application

# 根据环境变量设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')

application = get_wsgi_application()
