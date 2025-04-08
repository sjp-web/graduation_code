from django.urls import path
from .views import (
    music_views, user_views, search_views, 
    stats_views, admin_views
)

# 从各个视图导入具体函数
from .views import (
    register, login_view, profile_view, create_profile,
    music_search, search_suggestions,
    statistics_view, admin_dashboard,
    chat_with_ai
)

urlpatterns = [
    # 用户相关路由
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('user/center/', user_views.user_center, name='user_center'),
    
    # AI聊天机器人路由
    path('chat/ai/', chat_with_ai, name='chat_with_ai'),
    
    # 音乐相关路由
    path('', music_views.music_list, name='music_list'),
    path('upload/', music_views.upload_music, name='upload_music'),
    path('music/<int:pk>/', music_views.music_detail, name='music_detail'),
    path('music/<int:pk>/download/', music_views.download_music, name='download_music'),
    path('music/<int:pk>/comment/', music_views.add_comment, name='add_comment'),
    path('music/<int:pk>/delete/', music_views.delete_music, name='delete_music'),
    path('recommended/', music_views.recommended_music, name='recommended_music'),
    
    # 搜索相关路由
    path('search/', music_search, name='music_search'),
    path('search/suggestions/', search_suggestions, name='search_suggestions'),
    path('api/years/', search_views.years_api, name='years_api'),
    
    # 统计和管理路由
    path('statistics/', statistics_view, name='statistics'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]