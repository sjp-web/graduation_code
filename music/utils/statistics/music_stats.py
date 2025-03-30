from django.db.models import Count, Sum, Avg, F, Q, Max, Min, StdDev
from django.utils import timezone
from ...models import Music, Comment, MusicDownload
import datetime
from collections import defaultdict

def get_music_trends(days=30):
    """
    获取音乐平台的趋势数据
    
    参数:
        days: 统计的天数
    返回:
        趋势数据字典
    """
    # 计算日期范围
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=days)
    
    # 按日期范围创建日期列表
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += datetime.timedelta(days=1)
    
    # 获取每天上传的音乐数量
    daily_uploads = defaultdict(int)
    uploads = Music.objects.filter(
        release_date__gte=start_date,
        release_date__lte=end_date
    ).values('release_date').annotate(count=Count('id'))
    
    for upload in uploads:
        daily_uploads[upload['release_date']] = upload['count']
    
    # 获取每天的下载数量
    daily_downloads = defaultdict(int)
    downloads = MusicDownload.objects.filter(
        download_time__date__gte=start_date,
        download_time__date__lte=end_date
    ).values('download_time__date').annotate(count=Count('id'))
    
    for download in downloads:
        daily_downloads[download['download_time__date']] = download['count']
    
    # 构建趋势数据
    upload_trend = []
    download_trend = []
    date_labels = []
    
    for date in date_range:
        date_labels.append(date.strftime('%m-%d'))
        upload_trend.append(daily_uploads[date])
        download_trend.append(daily_downloads[date])
    
    return {
        'date_range': date_labels,
        'upload_trend': upload_trend,
        'download_trend': download_trend,
    }

def get_popular_music(limit=10, days=None):
    """
    获取最受欢迎的音乐
    
    参数:
        limit: 返回的音乐数量
        days: 如果提供，则只统计最近n天的数据
    返回:
        音乐列表
    """
    queryset = Music.objects.all()
    
    # 如果指定了天数，则只统计最近n天的数据
    if days:
        start_date = timezone.now().date() - datetime.timedelta(days=days)
        queryset = queryset.filter(release_date__gte=start_date)
    
    # 综合播放量和下载量，计算受欢迎程度分数
    # 这里我们将播放量权重设为1，下载量权重设为3
    popular_music = queryset.annotate(
        popularity_score=F('play_count') + F('download_count') * 3
    ).order_by('-popularity_score')[:limit]
    
    return popular_music

def get_category_stats():
    """
    获取音乐分类统计
    
    返回:
        分类统计字典
    """
    # 按分类统计音乐数量
    categories = Music.objects.values('category').annotate(
        count=Count('id'),
        total_plays=Sum('play_count'),
        total_downloads=Sum('download_count'),
        avg_plays=Avg('play_count'),
        avg_downloads=Avg('download_count')
    ).order_by('-count')
    
    # 计算每个分类的平均评论数
    categories_with_comments = []
    for category in categories:
        cat_name = category['category']
        # 获取该分类下的所有音乐ID
        music_ids = Music.objects.filter(category=cat_name).values_list('id', flat=True)
        # 统计评论数
        comment_count = Comment.objects.filter(music_id__in=music_ids).count()
        # 如果有音乐，则计算平均评论数
        if len(music_ids) > 0:
            avg_comments = comment_count / len(music_ids)
        else:
            avg_comments = 0
            
        # 添加评论统计到分类数据中
        category_data = {
            **category,
            'comment_count': comment_count,
            'avg_comments': round(avg_comments, 2)
        }
        categories_with_comments.append(category_data)
    
    return categories_with_comments

def get_music_analytics():
    """
    获取音乐数据分析统计
    
    返回:
        数据分析结果字典
    """
    # 获取基本统计
    total_music = Music.objects.count()
    total_plays = Music.objects.aggregate(Sum('play_count'))['play_count__sum'] or 0
    total_downloads = Music.objects.aggregate(Sum('download_count'))['download_count__sum'] or 0
    
    # 获取播放量和下载量的统计数据
    play_stats = Music.objects.aggregate(
        avg=Avg('play_count'),
        max=Max('play_count'),
        min=Min('play_count'),
        std=StdDev('play_count')
    )
    
    download_stats = Music.objects.aggregate(
        avg=Avg('download_count'),
        max=Max('download_count'),
        min=Min('download_count'),
        std=StdDev('download_count')
    )
    
    return {
        'total_music': total_music,
        'total_plays': total_plays,
        'total_downloads': total_downloads,
        'play_stats': {
            'avg': round(play_stats['avg'] or 0, 2),
            'max': play_stats['max'] or 0,
            'min': play_stats['min'] or 0,
            'std': round(play_stats['std'] or 0, 2)
        },
        'download_stats': {
            'avg': round(download_stats['avg'] or 0, 2),
            'max': download_stats['max'] or 0,
            'min': download_stats['min'] or 0,
            'std': round(download_stats['std'] or 0, 2)
        }
    } 