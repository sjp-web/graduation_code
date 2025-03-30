# music/admin.py
from django.contrib import admin
from .models import Music, Comment, Profile, AdminLog, MusicDownload
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from rangefilter.filters import DateRangeFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .views import admin_dashboard
from django.db.models import Count

# 音乐资源定义（用于导入导出）
class MusicResource(resources.ModelResource):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'album', 'category', 'play_count', 'download_count')
        export_order = fields

@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    resource_class = MusicResource
    list_display = ('title', 'artist', 'category', 'play_count', 'download_count', 'cover_preview', 'upload_status')
    list_filter = ('category', 'is_original', ('release_date', DateRangeFilter))
    search_fields = ('title', 'artist', 'album')
    readonly_fields = ('play_count', 'download_count', 'uploaded_by')
    list_per_page = 20
    actions = ['approve_music', 'export_as_csv']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'artist', 'album', 'category')
        }),
        ('文件信息', {
            'fields': ('audio_file', 'cover_image', 'lyrics')
        }),
        ('统计信息', {
            'fields': ('play_count', 'download_count', 'likes')
        }),
        ('管理信息', {
            'fields': ('is_original', 'release_date', 'uploaded_by')
        })
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.cover_image.url)
        return "-"
    cover_preview.short_description = '封面预览'

    def upload_status(self, obj):
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            'success' if obj.audio_file else 'danger',
            '已上传' if obj.audio_file else '未上传'
        )
    upload_status.short_description = '上传状态'

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        return ['title', 'artist', 'category', 'play_count', 'download_count', 'cover_preview', 'upload_status']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'user', 'music_link', 'created_at', 'is_recent')
    search_fields = ('content', 'user__username', 'music__title')
    list_filter = (('created_at', DateRangeFilter),)
    list_select_related = ('user', 'music')
    
    def music_link(self, obj):
        return format_html('<a href="/admin/music/music/{}/change/">{}</a>', obj.music.id, obj.music.title)
    music_link.short_description = '关联音乐'

    def is_recent(self, obj):
        return obj.created_at > timezone.now() - timezone.timedelta(days=3)
    is_recent.boolean = True
    is_recent.short_description = '近期评论'

    def truncated_content(self, obj):
        return f"{obj.content[:30]}..." if len(obj.content) > 30 else obj.content
    truncated_content.short_description = '评论内容'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_preview', 'music_count', 'last_activity')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('music_count',)
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.avatar.url)
        return "-"
    avatar_preview.short_description = '头像预览'

    def music_count(self, obj):
        return obj.user.music_set.count()
    music_count.short_description = '上传歌曲数'

    def last_activity(self, obj):
        last_music = obj.user.music_set.order_by('-release_date').first()
        return last_music.release_date if last_music else '-'
    last_activity.short_description = '最后上传时间'

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action_type', 'target_info')
    list_filter = ('action', ('timestamp', DateRangeFilter))
    search_fields = ('user__username', 'action', 'target')
    date_hierarchy = 'timestamp'
    
    def action_type(self, obj):
        color_map = {
            'create': 'success',
            'update': 'warning',
            'delete': 'danger'
        }
        color = color_map.get(obj.action.lower(), 'primary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.action.capitalize()
        )
    action_type.short_description = '操作类型'
    action_type.admin_order_field = 'action'

    def target_info(self, obj):
        return format_html('<code>{}</code>', obj.target[:50])
    target_info.short_description = '操作目标'

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'change_message']
    list_filter = ['action_time', 'content_type']
    search_fields = ['user__username', 'object_repr']
    date_hierarchy = 'action_time'

@admin.register(MusicDownload)
class MusicDownloadAdmin(admin.ModelAdmin):
    list_display = ('music_link', 'user_link', 'formatted_time', 'location_info', 'status_tag')
    list_filter = (('download_time', DateRangeFilter), 'user')
    search_fields = ('music__title', 'user__username', 'ip_address')
    date_hierarchy = 'download_time'
    list_per_page = 20
    readonly_fields = ('music', 'user', 'download_time', 'ip_address')
    actions = ['export_csv', 'export_excel']
    
    # 修正模板路径
    change_list_template = 'admin/music/musicdownload/change_list.html'
    
    class Media:
        css = {
            'all': ('css/admin/custom_admin.css',)
        }
        js = ('js/admin/custom_admin.js',)
    
    def has_change_permission(self, request, obj=None):
        # 下载记录不应被修改
        return False
        
    def has_add_permission(self, request):
        # 不允许手动添加下载记录
        return False
        
    def music_link(self, obj):
        """显示音乐标题并链接到音乐详情页"""
        return format_html(
            '<strong><a href="/admin/music/music/{}/change/">'
            '<i class="fas fa-music" style="margin-right:5px;"></i>{}</a></strong>',
            obj.music.id, obj.music.title
        )
    music_link.short_description = '音乐作品'
    music_link.admin_order_field = 'music__title'
    
    def user_link(self, obj):
        """显示用户名并链接到用户详情页"""
        return format_html(
            '<a href="/admin/auth/user/{}/change/">'
            '<i class="fas fa-user" style="margin-right:5px;"></i>{}</a>',
            obj.user.id, obj.user.username
        )
    user_link.short_description = '下载用户'
    user_link.admin_order_field = 'user__username'
    
    def formatted_time(self, obj):
        """格式化下载时间显示"""
        return format_html(
            '<span title="{}">'
            '<i class="fas fa-calendar-alt" style="margin-right:5px;"></i>{}</span>',
            obj.download_time.strftime('%Y-%m-%d %H:%M:%S'),
            obj.download_time.strftime('%Y-%m-%d %H:%M')
        )
    formatted_time.short_description = '下载时间'
    formatted_time.admin_order_field = 'download_time'
    
    def location_info(self, obj):
        """显示IP地址信息"""
        if obj.ip_address:
            return format_html(
                '<span class="text-muted">'
                '<i class="fas fa-map-marker-alt" style="margin-right:5px;"></i>{}</span>',
                obj.ip_address
            )
        return format_html('<span class="text-muted">-</span>')
    location_info.short_description = 'IP地址'
    location_info.admin_order_field = 'ip_address'
    
    def status_tag(self, obj):
        """显示下载状态标签"""
        now = timezone.now()
        time_diff = now - obj.download_time
        
        if time_diff.days < 1:
            color = 'success'
            status = '今日下载'
        elif time_diff.days < 7:
            color = 'info'
            status = '本周下载'
        elif time_diff.days < 30:
            color = 'warning'
            status = '本月下载'
        else:
            color = 'secondary'
            status = '历史下载'
            
        return format_html(
            '<span class="badge bg-{}" style="font-size: 85%;">{}</span>',
            color, status
        )
    status_tag.short_description = '下载状态'
    
    def export_csv(self, request, queryset):
        """导出选中的下载记录为CSV文件"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="download_records.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['音乐标题', '下载用户', '下载时间', 'IP地址'])
        
        for record in queryset:
            writer.writerow([
                record.music.title,
                record.user.username,
                record.download_time.strftime('%Y-%m-%d %H:%M:%S'),
                record.ip_address or '-'
            ])
            
        return response
    export_csv.short_description = "导出所选记录为CSV"
    
    def export_excel(self, request, queryset):
        """导出选中的下载记录为Excel文件"""
        import xlwt
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="download_records.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('下载记录')
        
        # 设置标题行样式
        header_style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        header_style.font = font
        
        # 写入标题行
        row_num = 0
        columns = ['音乐标题', '艺术家', '下载用户', '下载时间', 'IP地址']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title, header_style)
        
        # 写入数据行
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'YYYY-MM-DD HH:MM:SS'
        
        for record in queryset:
            row_num += 1
            ws.write(row_num, 0, record.music.title)
            ws.write(row_num, 1, record.music.artist)
            ws.write(row_num, 2, record.user.username)
            ws.write(row_num, 3, record.download_time, date_style)
            ws.write(row_num, 4, record.ip_address or '-')
            
        wb.save(response)
        return response
    export_excel.short_description = "导出所选记录为Excel"
    
    def changelist_view(self, request, extra_context=None):
        """增强下载记录列表视图，添加统计信息"""
        # 添加基本统计数据
        extra_context = extra_context or {}
        
        # 计算今日下载量
        today = timezone.now().date()
        today_count = MusicDownload.objects.filter(download_time__date=today).count()
        
        # 计算本周下载量
        week_start = today - timezone.timedelta(days=today.weekday())
        week_count = MusicDownload.objects.filter(download_time__date__gte=week_start).count()
        
        # 计算本月下载量
        month_start = today.replace(day=1)
        month_count = MusicDownload.objects.filter(download_time__date__gte=month_start).count()
        
        # 计算热门下载
        top_music = MusicDownload.objects.values('music__title', 'music__artist').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # 计算活跃用户
        active_users = MusicDownload.objects.values('user__username').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        extra_context.update({
            'title': '下载记录管理',
            'today_count': today_count,
            'week_count': week_count,
            'month_count': month_count,
            'total_count': MusicDownload.objects.count(),
            'top_music': top_music,
            'active_users': active_users
        })
        
        return super().changelist_view(request, extra_context=extra_context)

# 自定义管理仪表板
class CustomAdminSite(admin.AdminSite):
    name = 'music_admin'
    site_header = '音乐管理后台'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='dashboard')
        ]
        return custom_urls + urls

    def get_app_list(self, request):
        # 获取原始应用列表
        app_list = super().get_app_list(request)
        
        # 添加自定义看板应用
        dashboard_app = {
            'name': '数据看板',
            'app_label': 'dashboard',
            'app_url': self._get_admin_url('dashboard'),
            'has_module_perms': True,
            'models': [{
                'name': '系统概览',
                'object_name': 'dashboard',
                'admin_url': self._get_admin_url('dashboard'),
                'view_only': True,
            }],
        }
        
        # 将看板插入到应用列表最前面
        return [dashboard_app] + app_list

    def _get_admin_url(self, name):
        return f'/{self.name}/{name}/'

@staff_member_required
def admin_dashboard(request):
    current_site = admin_site if 'music_admin' in request.path else admin.site
    stats = {
        'total_users': User.objects.count(),
        'total_music': Music.objects.count(),
        'new_users': User.objects.filter(date_joined__date=timezone.now().date()).count(),
        'popular_music': Music.objects.order_by('-play_count')[:5],
        'recent_comments': Comment.objects.select_related('user', 'music').order_by('-created_at')[:5]
    }
    return render(request, 'admin/dashboard.html', {
        **current_site.each_context(request),
        'stats': stats,
        'title': '系统概览',
        'opts': current_site._registry[Music].model._meta
    })

# 注册Django默认的User和Group模型
admin_site = CustomAdminSite(name='music_admin')