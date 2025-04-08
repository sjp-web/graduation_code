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
import json
import sys

from ..models import Music, Comment, MusicDownload, PlayHistory
from ..forms import MusicForm, CommentForm
from ..utils.file_handlers.image_handlers import optimize_upload

def is_staff(user):
    return user.is_staff

# 音乐列表视图
@login_required
def music_list(request):
    # 获取查询参数
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'title')
    
    # 构建基础查询集，使用select_related减少数据库查询
    music_query = Music.objects.select_related('uploaded_by')
    
    # 应用过滤条件
    if query:
        music_query = music_query.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        )
    
    if category:
        music_query = music_query.filter(category=category)
    
    # 应用排序
    sort_mapping = {
        'title': 'title',
        'artist': 'artist',
        'date': '-release_date',
        'popularity': '-play_count'
    }
    music_query = music_query.order_by(sort_mapping.get(sort, 'title'))
    
    # 分页处理
    paginator = Paginator(music_query, 12)  # 每页显示12条记录
    page = request.GET.get('page', 1)
    music_page = paginator.get_page(page)
    
    # 获取所有分类（定义分类选项和对应的显示名称）
    category_choices = [
        ('pop', '流行'),
        ('rock', '摇滚'),
        ('classical', '古典')
    ]
    
    # 只序列化当前页数据为JSON
    # 使用列表推导式生成数据，更加简洁和高效
    current_page_data = [{
        'id': song.id,
        'title': song.title,
        'artist': song.artist,
        'album': song.album,
        'release_date': song.release_date.strftime('%Y-%m-%d'),
        'cover_image': song.cover_image.url if song.cover_image and song.cover_image_exists() else None,
        'play_count': song.play_count,
        'category': song.category,
        'file_size': song.file_size
    } for song in music_page]
    
    # 获取当前分类的中文名称
    current_category_name = ''
    if category:
        for cat_code, cat_name in category_choices:
            if cat_code == category:
                current_category_name = cat_name
                break
    
    context = {
        'music': music_page,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': music_page,
        'music_json': json.dumps(current_page_data),
        'categories_json': json.dumps([cat[0] for cat in category_choices]),
        'category_choices': category_choices,
        'current_sort': sort,
        'current_category': category,
        'current_category_name': current_category_name,
        'current_query': query
    }
    
    return render(request, 'music/music_list.html', context)

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
    
    # 获取分类选项
    category_choices = [
        ('pop', '流行'),
        ('rock', '摇滚'),
        ('classical', '古典')
    ]
    
    return render(request, 'music/upload_music.html', {
        'form': form,
        'categories_json': json.dumps([cat[0] for cat in category_choices])
    })

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
    """基于用户历史推荐音乐"""
    # 1. 获取用户播放历史
    recent_days = 30
    recent_date = timezone.now() - timedelta(days=recent_days)
    recent_play_ids = list(PlayHistory.objects.filter(
        user=request.user,
        played_at__gte=recent_date
    ).values_list('music_id', flat=True))
    
    # 2. 检查数据库中是否有音乐
    if Music.objects.count() == 0:
        return render(request, 'music/recommended_music.html', {
            'recommended_music': [],
            'error_message': '数据库中没有音乐，请先上传一些音乐',
            'recommended_music_json': json.dumps([])
        })
    
    # 3. 创建推荐策略
    recommended = None
    recommendation_type = ""  # 记录推荐类型，用于显示推荐理由
    favorite_category_name = ""
    
    # 策略1: 基于用户最喜欢的类别推荐
    if recent_play_ids:
        # 获取用户最喜欢的类别
        favorite_categories = Music.objects.filter(
            id__in=recent_play_ids
        ).values('category').annotate(
            count=Count('id')
        ).order_by('-count')
        
        if favorite_categories.exists():
            favorite_category = favorite_categories[0]['category']
            favorite_category_name = favorite_category
            # 获取该类别下的推荐音乐
            recommended = Music.objects.filter(
                category=favorite_category
            ).exclude(
                id__in=recent_play_ids
            ).annotate(
                score=F('play_count') * 0.6 + 
                      F('download_count') * 0.2 + 
                      Count('comments') * 0.2
            ).order_by('-score')[:10]
            
            if recommended.exists():
                recommendation_type = "category"
    
    # 策略2: 如果策略1没有足够结果或用户没有历史，使用全局热度推荐
    if not recommended or recommended.count() < 5:
        recommended = Music.objects.exclude(
            id__in=recent_play_ids if recent_play_ids else []
        ).annotate(
            score=F('play_count') * 0.6 + 
                  F('download_count') * 0.2 + 
                  Count('comments') * 0.2
        ).order_by('-score')[:10]
        
        if recommended.exists() and recommendation_type != "category":
            recommendation_type = "popularity"
    
    # 策略3: 如果都没结果，推荐最新音乐
    if not recommended or recommended.count() == 0:
        recommended = Music.objects.order_by('-release_date')[:10]
        
        if recommended.exists() and recommendation_type == "":
            recommendation_type = "latest"
    
    # 4. 序列化音乐数据
    recommended_music_data = []
    try:
        for song in recommended:
            # 添加错误处理，防止访问不存在的文件
            cover_image_url = None
            if song.cover_image and song.cover_image_exists():
                cover_image_url = song.cover_image.url
            
            # 根据推荐类型生成推荐理由
            recommendation_reason = ""
            if recommendation_type == "category":
                recommendation_reason = f"因为您喜欢{favorite_category_name}类音乐"
            elif recommendation_type == "popularity":
                recommendation_reason = "这是热门音乐，很多人都在听"
            else:
                recommendation_reason = "这是最新上传的音乐，不容错过"
                
            recommended_music_data.append({
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'album': song.album,
                'release_date': song.release_date.strftime('%Y-%m-%d'),
                'cover_image': cover_image_url,
                'play_count': song.play_count,
                'category': song.category,
                'file_size': song.file_size,
                'reason': recommendation_reason
            })
    except Exception as e:
        # 只记录错误但不中断
        print(f"序列化推荐数据时出错: {e}", file=sys.stderr)
        recommended_music_data = [{'id': 0, 'title': '暂无推荐音乐', 'artist': '-', 'album': '-'}]
    
    # 5. 返回结果
    return render(request, 'music/recommended_music.html', {
        'recommended_music': recommended,
        'recommended_music_json': json.dumps(recommended_music_data),
        'recommendation_type': recommendation_type,
        'favorite_category': favorite_category_name,
        'is_staff': request.user.is_staff
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