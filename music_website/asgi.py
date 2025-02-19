"""
music_website项目的 ASGI 配置。

它将 ASGI 可调用对象公开为名为 'application' 的模块级变量。

有关此文件的更多信息，请参阅
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')

application = get_asgi_application()
