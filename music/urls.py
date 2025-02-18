from .views import music_list, upload_music, music_search, search_suggestions
from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),  # 用户注册页面
    path('profile/', views.profile_view, name='profile'),  # 用户个人资料页面
    path('', music_list, name='music_list'),  # 音乐列表页面
    path('upload/', upload_music, name='upload_music'),  # 上传音乐页面
    path('login/', views.login_view, name='login'),  # 登录页面路由
    path('logout/', views.logout_view, name='logout'),  # 注销路径
    path('<int:music_id>/', views.music_detail, name='music_detail'),  # 音乐详细信息页面
    path('profile/create/', views.create_profile, name='profile_creation'), # 创建用户个人资料页面
    path('search/', music_search, name='music_search'),
    path('api/search-suggestions/', search_suggestions, name='search_suggestions'),
]