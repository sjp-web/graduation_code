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

urlpatterns = [
    # 自定义音乐后台
    path('music-admin/', admin_site.urls),
    
    # 默认Django admin后台
    path('admin/', admin.site.urls),
    
    # 主应用URLs
    path('', include('music.urls')),
    
    # 认证系统
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 在DEBUG模式下添加Debug Toolbar URLs
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
