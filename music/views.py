from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from .models import Music
from .forms import UserRegistrationForm, MusicForm, ProfileForm
from django.contrib.auth import logout

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

def login_view(request):
    if request.user.is_authenticated:  # 检查用户是否已登录
        return redirect('music_list')  # 如果已登录，则重定向到音乐列表

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('music_list')  # 登录成功后重定向
    else:
        form = AuthenticationForm()  # GET 请求，显示登录表单

    return render(request, 'music/login.html', {'form': form})  # 渲染登录模板

@login_required
def profile_view(request):
    user_profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'music/profile.html', {
        'form': form,
        'user_profile': user_profile,
    })

@login_required
def music_list(request):
    music = Music.objects.all()
    return render(request, 'music/music_list.html', {'music': music})

@login_required
def upload_music(request):
    if request.method == "POST":
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.uploaded_by = request.user
            music.save()
            return redirect('music_list')
    else:
        form = MusicForm()
    return render(request, 'music/upload_music.html', {'form': form})

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
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'music/create_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)  # 注销用户
    return redirect('login')  # 注销后重定向到登录页面