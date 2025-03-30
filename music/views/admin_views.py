from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin import site as admin_site
from ..models import Music, Comment

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