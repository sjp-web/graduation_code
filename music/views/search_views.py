from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from ..models import Music

# 音乐搜索视图
def music_search(request):
    query = request.GET.get('q', '')
    artist = request.GET.get('artist', '')
    album = request.GET.get('album', '')
    year = request.GET.get('year', '')
    format_type = request.GET.get('format', '')  # 是否需要JSON响应
    
    # 构建搜索查询条件
    music_list = Music.objects.all()
    
    # 处理可能包含"歌曲名 - 艺术家"格式的查询
    if query and ' - ' in query and not artist:
        # 尝试拆分查询
        parts = query.split(' - ', 1)
        if len(parts) == 2:
            title_part, artist_part = parts
            # 使用组合条件查询
            music_list = music_list.filter(
                Q(title__icontains=title_part) & Q(artist__icontains=artist_part)
            )
        else:
            # 标准查询
            music_list = music_list.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query) |
                Q(album__icontains=query)
            )
    elif query:
        # 标准查询
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
    page = request.GET.get('page', 1)
    music = paginator.get_page(page)
    
    # 获取所有可用年份
    years = Music.objects.dates('release_date', 'year', order='DESC')
    years = [date.year for date in years]
    
    # 如果请求的是JSON格式，返回JSON响应
    if format_type == 'json':
        results = []
        
        for item in music:
            cover_url = item.cover_image.url if item.cover_image else ''
            
            results.append({
                'id': item.id,
                'title': item.title,
                'artist': item.artist,
                'album': item.album,
                'release_date': item.release_date.strftime('%Y-%m-%d'),
                'cover_url': cover_url,
                'audio_url': item.audio_file.url,
                'play_count': item.play_count,
                'download_count': item.download_count
            })
            
        return JsonResponse({
            'results': results,
            'total': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': int(page)
        })
    
    # 否则返回HTML模板
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

def years_api(request):
    """返回系统中所有可用年份的API视图"""
    years = Music.objects.dates('release_date', 'year', order='DESC')
    years = [date.year for date in years]
    
    return JsonResponse({'years': years}) 