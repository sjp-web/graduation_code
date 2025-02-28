"""
URL configuration for music_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# music_website/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from music.admin import admin_site  # 仅导入admin_site
from music.views import statistics_view  # 仅导入statistics_view

urlpatterns = [
    path('admin/', admin.site.urls),  # 默认admin（可选保留）
    path('music-admin/', admin_site.urls),  # 自定义管理后台
    path('', include('music.urls')),  # 确保主路径指向music应用
    path('accounts/', include('django.contrib.auth.urls')),  # 添加认证系统
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
