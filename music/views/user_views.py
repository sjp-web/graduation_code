from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from ..models import Music, Profile
from ..forms import UserRegistrationForm, ProfileForm
from ..utils.file_handlers.image_handlers import optimize_upload
from uuid import uuid4

# 用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'music/register.html', {'form': form})

# 用户登录视图
def login_view(request):
    form = AuthenticationForm()  # 初始化空表单
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('music_list')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'music/login.html', {'form': form})  # 确保传递表单

# 个人资料查看视图
@login_required
def profile_view(request):
    user_profile = request.user.profile
    # 修改用户歌曲查询部分
    user_songs = Music.objects.filter(uploaded_by=request.user).order_by('-release_date')
    paginator = Paginator(user_songs, 10)  # 每页10条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # 添加头像处理逻辑
            if 'avatar' in request.FILES:
                optimized = optimize_upload(request.FILES['avatar'], max_size=(500, 500))
                if optimized:
                    user_profile.avatar.save(
                        f"{uuid4()}.jpg", 
                        ContentFile(optimized.getvalue()),
                        save=False
                    )
            form.save()
            messages.success(request, '个人资料已更新！')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'music/profile.html', {
        'form': form,
        'user_profile': user_profile,
        'user_songs': user_songs,  # 添加用户上传歌曲到上下文
        'page_obj': page_obj
    })

# 用户创建或编辑个人资料视图
@login_required
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # 不立即保存到数据库
            profile.user = request.user  # 关联当前用户
            profile.save()  # 保存到数据库
            return redirect('profile')  # 成功后重定向到个人资料页面
    else:
        form = ProfileForm()  # GET 请求时，准备空表单

    return render(request, 'music/create_profile.html', {'form': form})  # 渲染表单页面

def custom_logout(request):
    # 如果有自定义注销逻辑可能会覆盖设置
    pass 