# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, login
from .models import Music
from .forms import UserRegistrationForm, MusicForm


def music_list(request):
    music = Music.objects.all()
    return render(request, 'music/music_list.html', {'music': music})

# 需要修改视图以处理表单的显示和提交。添加一个新视图来处理音乐上传
@login_required
def upload_music(request):
    if request.method == "POST":
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)  # 保存表单但不提交到数据库
            music.uploaded_by = request.user  # 将当前用户赋值给 uploaded_by 字段
            music.save()  # 将音乐记录存入数据库
            return redirect('music_list')  # 上传完成后重定向到音乐列表页面
    else:
        form = MusicForm()  # GET 请求时，显示上传表单
    return render(request, 'music/upload_music.html', {'form': form})  # 渲染上传页面

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存用户
            login(request, user)  # 自动登录用户
            return redirect('profile')  # 重定向到个人资料页面
    else:
        form = UserRegistrationForm()  # 处理 GET 请求，准备空表单

    return render(request, 'music/register.html', {'form': form})  # 渲染注册页面

@login_required
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('music_list')  # 登录成功重定向
    else:
        form = AuthenticationForm()
    return render(request, 'music/login.html', {'form': form})

@login_required
def music_detail(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    return render(request, 'music/music_detail.html', {'music': music})

@login_required
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # 关联当前用户
            profile.save()
            return redirect('profile')  # 创建完成后重定向到个人资料页面
    else:
        form = ProfileForm()
    return render(request, 'music/create_profile.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm  # 确保您有这个表单类


@login_required
def profile_view(request):
    user_profile = request.user.profile  # 获取用户的个人资料
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()  # 保存资料
            return redirect('profile')  # 重定向到个人资料页面
    else:
        form = ProfileForm(instance=user_profile)  # 加载表单

    return render(request, 'music/profile.html', {
        'form': form,
        'user_profile': user_profile,
        # 删除与 user_songs 相关的传递
        # 'user_songs': user_songs,
    })
