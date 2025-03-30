from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from uuid import uuid4

from ..models import Music, Comment, MusicDownload
from ..forms import MusicForm, CommentForm
from ..utils.file_handlers.image_handlers import optimize_upload

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

# 在profile_view视图中添加下载计数
@login_required
def download_music(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    
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