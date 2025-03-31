from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

# 导入视图函数 - 直接从views包导入
from .views import (
    music_list, upload_music, music_detail, download_music,
    register, login_view, profile_view, create_profile,
    music_search, search_suggestions,
    statistics_view, admin_dashboard,
    chat_with_ai
)

urlpatterns = [
    path('', music_list, name='music_list'),  # 确保根路径有处理视图
    path('login/', login_view, name='login'),  # 登录页面
    path('register/', register, name='register'),  # 用户注册页面
    path('profile/', profile_view, name='profile'),  # 用户个人资料页面
    path('upload/', upload_music, name='upload_music'),  # 上传音乐页面
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='/login/',  # 使用绝对路径
             extra_context={'logout_message': '您已成功注销'}
         ), 
         name='logout'),
    path('<int:music_id>/', music_detail, name='music_detail'),  # 音乐详细信息页面
    path('profile/create/', create_profile, name='profile_creation'), # 创建用户个人资料页面
    path('search/', music_search, name='music_search'),# 音乐搜索
    path('api/search-suggestions/', search_suggestions, name='search_suggestions'),# 搜索建议
    path('statistics/', statistics_view, name='statistics'),# 统计信息页面
    path('download/<int:music_id>/', download_music, name='download_music'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('chat/ai/', chat_with_ai, name='chat_with_ai'),
]