from .views import music_list, upload_music, music_search, search_suggestions, admin_dashboard
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('', views.music_list, name='music_list'),  # 确保根路径有处理视图
    path('login/', views.login_view, name='login'),  # 登录页面
    path('register/', views.register, name='register'),  # 用户注册页面
    path('profile/', views.profile_view, name='profile'),  # 用户个人资料页面
    path('upload/', views.upload_music, name='upload_music'),  # 上传音乐页面
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='/login/',  # 使用绝对路径
             extra_context={'logout_message': '您已成功注销'}
         ), 
         name='logout'),
    path('<int:music_id>/', views.music_detail, name='music_detail'),  # 音乐详细信息页面
    path('profile/create/', views.create_profile, name='profile_creation'), # 创建用户个人资料页面
    path('search/', views.music_search, name='music_search'),# 音乐搜索
    path('api/search-suggestions/', search_suggestions, name='search_suggestions'),# 搜索建议
    path('statistics/', views.statistics_view, name='statistics'),# 统计信息页面
    path('download/<int:music_id>/', views.download_music, name='download_music'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]