from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
from django.contrib.auth.models import User
from ...models import Music, Comment, MusicDownload
import datetime

def get_user_activity(user, days=30):
    """
    获取用户在指定天数内的活动统计
    
    参数:
        user: User 对象
        days: 统计的天数
    返回:
        用户活动统计字典
    """
    # 计算日期范围
    end_date = timezone.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    # 获取用户上传的音乐数量
    uploaded_count = Music.objects.filter(
        uploaded_by=user,
        release_date__gte=start_date,
        release_date__lte=end_date
    ).count()
    
    # 获取用户评论数量
    comment_count = Comment.objects.filter(
        user=user,
        created_at__gte=start_date,
        created_at__lte=end_date
    ).count()
    
    # 获取用户下载数量
    download_count = MusicDownload.objects.filter(
        user=user,
        download_time__gte=start_date,
        download_time__lte=end_date
    ).count()
    
    # 计算用户活跃度得分
    activity_score = uploaded_count * 5 + comment_count * 2 + download_count
    
    return {
        'uploaded_count': uploaded_count,
        'comment_count': comment_count,
        'download_count': download_count,
        'activity_score': activity_score,
        'days': days
    }

def get_user_music_stats(user):
    """
    获取用户音乐相关的统计信息
    
    参数:
        user: User 对象
    返回:
        用户音乐统计字典
    """
    # 获取用户上传的所有音乐
    user_music = Music.objects.filter(uploaded_by=user)
    
    # 总播放次数
    total_plays = user_music.aggregate(Sum('play_count'))['play_count__sum'] or 0
    
    # 总下载次数
    total_downloads = user_music.aggregate(Sum('download_count'))['download_count__sum'] or 0
    
    # 平均播放次数
    avg_plays = user_music.aggregate(Avg('play_count'))['play_count__avg'] or 0
    
    # 获取最受欢迎的音乐(播放量最高的5首)
    popular_music = user_music.order_by('-play_count')[:5]
    
    # 按分类统计
    category_stats = user_music.values('category').annotate(
        count=Count('id'),
        total_plays=Sum('play_count'),
        avg_plays=Avg('play_count')
    ).order_by('-count')
    
    return {
        'total_music': user_music.count(),
        'total_plays': total_plays,
        'total_downloads': total_downloads,
        'avg_plays': round(avg_plays, 2),
        'popular_music': popular_music,
        'category_stats': category_stats
    }

def get_active_users(days=30, limit=10):
    """
    获取指定时间段内最活跃的用户
    
    参数:
        days: 统计的天数
        limit: 返回的用户数量
    返回:
        活跃用户列表
    """
    # 计算日期范围
    end_date = timezone.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    # 找出最近登录的用户
    active_users = User.objects.filter(last_login__gte=start_date)
    
    # 获取每个用户的上传数量
    user_uploads = dict(Music.objects.filter(
        uploaded_by__in=active_users,
        release_date__gte=start_date
    ).values('uploaded_by').annotate(
        upload_count=Count('id')
    ).values_list('uploaded_by', 'upload_count'))
    
    # 获取每个用户的评论数量
    user_comments = dict(Comment.objects.filter(
        user__in=active_users,
        created_at__gte=start_date
    ).values('user').annotate(
        comment_count=Count('id')
    ).values_list('user', 'comment_count'))
    
    # 获取每个用户的下载数量
    user_downloads = dict(MusicDownload.objects.filter(
        user__in=active_users,
        download_time__gte=start_date
    ).values('user').annotate(
        download_count=Count('id')
    ).values_list('user', 'download_count'))
    
    # 计算每个用户的活跃度得分
    user_scores = []
    for user in active_users:
        score = (
            user_uploads.get(user.id, 0) * 5 +   # 上传权重为5
            user_comments.get(user.id, 0) * 2 +  # 评论权重为2
            user_downloads.get(user.id, 0)       # 下载权重为1
        )
        user_scores.append((user, score))
    
    # 按得分排序并返回前N名
    return sorted(user_scores, key=lambda x: x[1], reverse=True)[:limit] 