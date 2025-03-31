from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from ..models import Music, Comment
import psutil
import os

@staff_member_required
def admin_dashboard(request):
    """管理员仪表盘视图"""
    # 应用统计数据
    stats = {
        'total_users': User.objects.count(),
        'total_music': Music.objects.count(),
        'new_users': User.objects.filter(date_joined__date=timezone.now().date()).count(),
        'popular_music': Music.objects.order_by('-play_count')[:5],
        'recent_comments': Comment.objects.select_related('user', 'music').order_by('-created_at')[:5]
    }
    
    # 获取实时系统资源使用情况
    system_stats = {}
    
    try:
        # CPU使用率
        system_stats['cpu_percent'] = psutil.cpu_percent(interval=0.5)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        system_stats['memory_used'] = round(memory.used / (1024 * 1024 * 1024), 2)  # GB
        system_stats['memory_total'] = round(memory.total / (1024 * 1024 * 1024), 2)  # GB
        system_stats['memory_percent'] = memory.percent
        
        # 磁盘使用情况
        disk = psutil.disk_usage(os.path.abspath(os.sep))  # 根目录
        system_stats['disk_used'] = round(disk.used / (1024 * 1024 * 1024), 2)  # GB
        system_stats['disk_total'] = round(disk.total / (1024 * 1024 * 1024), 2)  # GB
        system_stats['disk_percent'] = disk.percent
        
        # 网络信息
        net_io = psutil.net_io_counters()
        system_stats['net_sent'] = round(net_io.bytes_sent / (1024 * 1024), 2)  # MB
        system_stats['net_recv'] = round(net_io.bytes_recv / (1024 * 1024), 2)  # MB
    except Exception as e:
        # 如果系统资源监控失败，添加默认值
        system_stats = {
            'cpu_percent': 0,
            'memory_used': 0,
            'memory_total': 0,
            'memory_percent': 0,
            'disk_used': 0,
            'disk_total': 0,
            'disk_percent': 0,
            'net_sent': 0,
            'net_recv': 0,
            'error': str(e)
        }
    
    # 确定使用哪个admin site的上下文
    if 'music-admin' in request.path:
        from ..admin import admin_site
        current_site = admin_site
    else:
        current_site = admin.site
    
    # 合并自定义上下文和admin上下文
    context = {
        'stats': stats,
        'system_stats': system_stats,
        'title': '系统数据概览',
        'has_permission': True,
        **current_site.each_context(request)  # 添加完整的admin上下文
    }
    
    return render(request, 'admin/dashboard.html', context) 