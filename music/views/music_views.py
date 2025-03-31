from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from uuid import uuid4
from django.db.models import Count, Q, F
from django.utils import timezone
from datetime import timedelta

from ..models import Music, Comment, MusicDownload, PlayHistory
from ..forms import MusicForm, CommentForm
from ..utils.file_handlers.image_handlers import optimize_upload

def is_staff(user):
    return user.is_staff

# 音乐列表视图
@login_required
def music_list(request):
    # 使用select_related优化查询，减少数据库访问次数
    music_list = Music.objects.select_related('uploaded_by').order_by('-release_date')
    paginator = Paginator(music_list, 12)  # 每页显示12条记录
    page = request.GET.get('page')
    music = paginator.get_page(page)
    return render(request, 'music/music_list.html', {
        'music': music,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': music
    })

# 上传音乐视图
@login_required
@user_passes_test(is_staff)
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
            messages.success(request, '音乐上传成功！')
            return redirect('music_list')
        else:
            messages.error(request, '请检查表单填写是否正确。')
    else:
        form = MusicForm()
    return render(request, 'music/upload_music.html', {'form': form})

# 音乐详细信息视图
@login_required
def music_detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    # 增加播放计数（每次访问详情页+1）
    music.play_count += 1
    music.save(update_fields=['play_count'])
    
    # 记录播放历史
    PlayHistory.objects.create(user=request.user, music=music)
    
    comments = music.comments.all()

    if request.method == 'POST':
        if 'comment_id' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            # 添加权限校验
            if comment.user != request.user and not request.user.is_staff:
                messages.error(request, '无权删除该评论')
                return redirect('music_detail', pk=music.id)
            comment.delete()
            messages.success(request, '评论已成功删除。')
            return redirect('music_detail', pk=music.id)
        else:
            # 添加评论
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.music = music
                comment.user = request.user
                comment.save()
                messages.success(request, '评论已成功发布。')
                return redirect('music_detail', pk=music.id)
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

# 在profile_view视图中添加下载计数
@login_required
def download_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    
    # 增加下载计数
    music.download_count += 1
    music.save(update_fields=['download_count'])
    
    # 记录下载历史
    # 获取用户IP地址
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    # 创建下载记录
    MusicDownload.objects.create(
        music=music,
        user=request.user,
        ip_address=ip
    )
    
    # 返回文件响应
    response = FileResponse(music.audio_file)
    response['Content-Disposition'] = f'attachment; filename="{music.audio_file.name}"'
    return response

@login_required
def recommended_music(request):
    # 获取用户最近30天的播放历史
    recent_days = 30
    recent_date = timezone.now() - timedelta(days=recent_days)
    
    # 获取用户最近播放的音乐ID列表
    recent_play_ids = list(PlayHistory.objects.filter(
        user=request.user,
        played_at__gte=recent_date
    ).values_list('music_id', flat=True))
    
    # 基于用户最近播放的音乐推荐
    if recent_play_ids:
        # 获取用户最常听的音乐类别
        favorite_categories = Music.objects.filter(
            id__in=recent_play_ids
        ).values('category').annotate(count=Count('id')).order_by('-count')
        
        if favorite_categories.exists():
            # 获取用户最常听的类别
            favorite_category = favorite_categories[0]['category']
            
            # 获取该类别下所有音乐的推荐分数
            recommended = Music.objects.filter(
                category=favorite_category
            ).exclude(
                id__in=recent_play_ids
            ).annotate(
                score=(
                    F('play_count') * 0.6 +
                    F('download_count') * 0.2 +
                    Count('comments') * 0.2
                )
            ).order_by('-score')[:10]
            
            # 如果推荐数量不足，补充最新上传的音乐
            if recommended.count() < 10:
                remaining_count = 10 - recommended.count()
                additional_music = Music.objects.filter(
                    category=favorite_category
                ).exclude(
                    id__in=recent_play_ids + list(recommended.values_list('id', flat=True))
                ).order_by('-release_date')[:remaining_count]
                recommended = list(recommended) + list(additional_music)
        else:
            # 如果没有类别信息，基于全局热度推荐
            recommended = Music.objects.exclude(
                id__in=recent_play_ids
            ).annotate(
                score=(
                    F('play_count') * 0.6 +
                    F('download_count') * 0.2 +
                    Count('comments') * 0.2
                )
            ).order_by('-score')[:10]
    else:
        # 如果没有播放记录，基于全局热度推荐
        recommended = Music.objects.annotate(
            score=(
                F('play_count') * 0.6 +
                F('download_count') * 0.2 +
                Count('comments') * 0.2
            )
        ).order_by('-score')[:10]
    
    return render(request, 'music/recommended_music.html', {
        'recommended_music': recommended
    })

@login_required
def add_comment(request, pk):
    music = get_object_or_404(Music, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.music = music
            comment.user = request.user
            comment.save()
            messages.success(request, '评论已成功发布。')
    return redirect('music_detail', pk=pk)

@login_required
@user_passes_test(is_staff)
def delete_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    if request.method == 'POST':
        music.delete()
        messages.success(request, '音乐已成功删除。')
        return redirect('music_list')
    return render(request, 'music/delete_music_confirm.html', {'music': music})

# 音乐搜索视图
@login_required
def music_search(request):
    query = request.GET.get('q', '')
    if query:
        # 使用Q对象进行多字段搜索
        music_list = Music.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-release_date')
    else:
        music_list = Music.objects.none()
    
    # 分页
    paginator = Paginator(music_list, 12)
    page = request.GET.get('page')
    music = paginator.get_page(page)
    
    context = {
        'query': query,
        'music': music,
        'is_paginated': True,
        'page_obj': music,
    }
    return render(request, 'music/music_search.html', context) 