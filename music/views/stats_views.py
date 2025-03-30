from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, F
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Music, MusicDownload

@login_required
def statistics_view(request):
    # 修改分类统计查询
    categories = Music.objects.values('category').annotate(
        count=Count('id'),
        name=F('category')  # 直接使用F表达式获取分类名称
    ).order_by('-count')
    
    # 获取下载量趋势数据
    total_downloads = Music.objects.aggregate(Sum('download_count'))['download_count__sum'] or 0
    avg_downloads = Music.objects.filter(download_count__gt=0).aggregate(Avg('download_count'))['download_count__avg'] or 0
    
    # 获取最近7天的每日下载数据
    today = timezone.now().date()
    date_range = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]
    
    # 获取每日新增用户数据（最近7天）
    daily_users = []
    date_labels = []
    
    # 获取每日下载数据（基于实际下载记录）
    daily_downloads = []
    
    for date in date_range:
        next_day = date + timezone.timedelta(days=1)
        # 用户数据
        new_users = User.objects.filter(date_joined__date=date).count()
        daily_users.append(new_users)
        date_labels.append(date.strftime('%m-%d'))
        
        # 查询当天的下载记录
        day_downloads = MusicDownload.objects.filter(
            download_time__date=date
        ).count()
        
        # 如果当天没有下载记录，使用估算值
        if day_downloads == 0:
            # 查询当天之前的平均下载量
            prev_days = 3  # 查看之前3天的数据
            prev_date = date - timezone.timedelta(days=prev_days)
            
            prev_downloads = MusicDownload.objects.filter(
                download_time__date__gte=prev_date,
                download_time__date__lt=date
            ).count()
            
            # 如果有之前的数据，使用平均值；否则使用基于总下载量的估算
            if prev_downloads > 0:
                day_downloads = max(1, int(prev_downloads / prev_days))
            else:
                # 基于总下载量的估算
                estimate = max(1, int(total_downloads / 30))  # 假设总下载是过去30天累计
                day_downloads = estimate
        
        daily_downloads.append(day_downloads)
    
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
        },
        # 新增下载量趋势数据
        'downloads_trend': {
            'total_downloads': total_downloads,
            'avg_downloads': avg_downloads,
            'daily_downloads': daily_downloads,
            'date_labels': date_labels
        },
        # 新增每日用户趋势数据
        'daily_users': {
            'data': daily_users,
            'labels': date_labels
        }
    }
    return render(request, 'music/statistics.html', {'stats': stats}) 