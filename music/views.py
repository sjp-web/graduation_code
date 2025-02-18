from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from .models import Music, Comment
from .forms import UserRegistrationForm, MusicForm, ProfileForm, CommentForm
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

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
    if request.user.is_authenticated:  # 检查用户是否已登录
        return redirect('music_list')  # 如果已登录，则重定向到音乐列表

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # 使用 Django 内置的 AuthenticationForm
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # 使用 auth_login 登录用户
                return redirect('music_list')  # 登录成功后重定向
    else:
        form = AuthenticationForm()  # GET 请求，显示登录表单

    return render(request, 'music/login.html', {'form': form})  # 渲染登录模板

# 个人资料查看视图
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

# 音乐列表视图
@login_required
def music_list(request):
    music = Music.objects.all()
    return render(request, 'music/music_list.html', {'music': music})

# 上传音乐视图
@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.uploaded_by = request.user
            music.save()
            
            # 如果是AJAX请求，返回JSON响应
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('music_list')
    else:
        form = MusicForm()
    return render(request, 'music/upload_music.html', {'form': form})

# 音乐详细信息视图
@login_required
def music_detail(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    return render(request, 'music/music_detail.html', {'music': music})

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

# 用户注销视图
@login_required
def logout_view(request):
    logout(request)  # 注销用户
    return redirect('login')  # 注销后重定向到登录页面

def music_search(request):
    query = request.GET.get('q', '')
    artist = request.GET.get('artist', '')
    album = request.GET.get('album', '')
    year = request.GET.get('year', '')
    
    # 构建查询条件
    music_list = Music.objects.all()
    if query:
        music_list = music_list.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        )
    
    # 应用高级筛选
    if artist:
        music_list = music_list.filter(artist__icontains=artist)
    if album:
        music_list = music_list.filter(album__icontains=album)
    if year:
        music_list = music_list.filter(release_date__year=year)
    
    # 分页处理
    paginator = Paginator(music_list, 10)  # 每页显示10条
    page = request.GET.get('page')
    music = paginator.get_page(page)
    
    # 获取所有年份选项
    years = Music.objects.dates('release_date', 'year', order='DESC')
    years = [date.year for date in years]
    
    context = {
        'music': music,
        'query': query,
        'filters': {
            'artist': artist,
            'album': album,
            'year': year
        },
        'years': years,
        'is_paginated': paginator.num_pages > 1
    }
    
    return render(request, 'music/music_search.html', context)

def search_suggestions(request):
    """处理实时搜索建议的API视图"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if len(query) >= 2:  # 至少2个字符才开始搜索
        # 从数据库中获取匹配的歌曲
        matches = Music.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        )[:5]  # 限制返回5个建议
        
        for music in matches:
            suggestions.append(f"{music.title} - {music.artist}")
    
    return JsonResponse({'suggestions': suggestions})

@login_required
def music_detail(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    comments = music.comments.all()

    if request.method == 'POST':
        if 'comment_id' in request.POST:
            # 删除评论
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
            comment.delete()
            messages.success(request, '评论已成功删除。')
            return redirect('music_detail', music_id=music.id)
        else:
            # 添加评论
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.music = music
                comment.user = request.user
                comment.save()
                messages.success(request, '评论已成功发布。')
                return redirect('music_detail', music_id=music.id)
    else:
        form = CommentForm()

    return render(request, 'music/music_detail.html', {'music': music, 'comments': comments, 'form': form})