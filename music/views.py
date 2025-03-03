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
from django.http import JsonResponse, FileResponse
import json
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg, F
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile
from .utils.media_handlers import optimize_upload
from django.contrib.admin import site as admin_site
from django.views.decorators.http import require_POST

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

# 音乐列表视图
@login_required
def music_list(request):
    music_list = Music.objects.all().order_by('-release_date')
    return render(request, 'music/music_list.html', {'music': music_list})

# 上传音乐视图
@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)  # 确保接收文件
        if form.is_valid():
            instance = form.save(commit=False)
            instance.uploaded_by = request.user  # 关联上传用户
            
            # 处理封面图片
            if 'cover_image' in request.FILES:
                optimized = optimize_upload(request.FILES['cover_image'])
                if optimized:
                    instance.cover_image.save(
                        f"{uuid4()}.jpg",
                        ContentFile(optimized.getvalue()),
                        save=False
                    )
            
            instance.save()
            return redirect('music_list')
    else:
        form = MusicForm()
    return render(request, 'music/upload_music.html', {'form': form})

# 音乐详细信息视图
@login_required
def music_detail(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    # 增加播放计数（每次访问详情页+1）
    music.play_count += 1
    music.save(update_fields=['play_count'])
    
    comments = music.comments.all()

    if request.method == 'POST':
        if 'comment_id' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            # 添加权限校验
            if comment.user != request.user and not request.user.is_staff:
                messages.error(request, '无权删除该评论')
                return redirect('music_detail', music_id=music.id)
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

    # 修正后的歌词处理逻辑
    lyrics_lines = []
    if music.lyrics:
        # 使用splitlines()替代split('\n')以更好处理不同换行符
        # 保留空行而不是过滤掉
        lyrics_lines = [line.rstrip() for line in music.lyrics.splitlines()]
    
    return render(request, 'music/music_detail.html', {
        'music': music,
        'comments': comments,
        'form': form,
        'lyrics_lines': lyrics_lines
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

# 音乐搜索视图
def music_search(request):
    query = request.GET.get('q', '')
    artist = request.GET.get('artist', '')
    album = request.GET.get('album', '')
    year = request.GET.get('year', '')
    
    # 构建搜索查询条件
    music_list = Music.objects.all()
    if query:
        music_list = music_list.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        )
    
    # 应用高级筛选条件
    if artist:
        music_list = music_list.filter(artist__icontains=artist)
    if album:
        music_list = music_list.filter(album__icontains=album)
    if year:
        music_list = music_list.filter(release_date__year=year)
    
    # 分页处理（每页10条）
    paginator = Paginator(music_list, 10)  
    page = request.GET.get('page')
    music = paginator.get_page(page)
    
    # 获取所有可用年份
    years = Music.objects.dates('release_date', 'year', order='DESC')
    years = [date.year for date in years]
    
    return render(request, 'music/music_search.html', {
        'music': music,
        'query': query,
        'filters': {'artist': artist, 'album': album, 'year': year},
        'years': years,
        'is_paginated': paginator.num_pages > 1
    })

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
def statistics_view(request):
    # 修改分类统计查询
    categories = Music.objects.values('category').annotate(
        count=Count('id'),
        name=F('category')  # 直接使用F表达式获取分类名称
    ).order_by('-count')
    
    stats = {
        'categories': list(categories),  # 转换为列表以便模板处理
        'user_stats': {
            'upload_count': Music.objects.filter(uploaded_by=request.user).count(),
            'total_plays': Music.objects.filter(uploaded_by=request.user).aggregate(Sum('play_count'))['play_count__sum'] or 0,
            'total_downloads': Music.objects.filter(uploaded_by=request.user).aggregate(Sum('download_count'))['download_count__sum'] or 0,
            'recent_uploads': Music.objects.filter(uploaded_by=request.user).order_by('-release_date')[:5]
        },
        'global_stats': {
            'total_users': User.objects.count(),
            'total_music': Music.objects.count(),
            'popular_categories': Music.objects.values('category').annotate(count=Count('id')).order_by('-count')[:3]
        }
    }
    return render(request, 'music/statistics.html', {'stats': stats})

# 在profile_view视图中添加下载计数
@login_required
def download_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    music.download_count += 1
    music.save(update_fields=['download_count'])
    response = FileResponse(music.audio_file)
    response['Content-Disposition'] = f'attachment; filename="{music.audio_file.name}"'
    return response

@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_users': User.objects.count(),
        'total_music': Music.objects.count(),
        'new_users': User.objects.filter(date_joined__date=timezone.now().date()).count(),
        'popular_music': Music.objects.order_by('-play_count')[:5],
        'recent_comments': Comment.objects.select_related('user', 'music').order_by('-created_at')[:5]
    }
    # 添加使用admin模板的上下文
    return render(request, 'admin/dashboard.html', {
        'stats': stats,
        **admin_site.each_context(request)  # 添加管理后台的上下文变量
    })

def custom_logout(request):
    # 如果有自定义注销逻辑可能会覆盖设置
    pass