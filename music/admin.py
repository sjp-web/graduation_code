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
from . import views

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
    list_display = ('music', 'user', 'download_time', 'ip_address')
    list_filter = (('download_time', DateRangeFilter), 'user')
    search_fields = ('music__title', 'user__username', 'ip_address')
    date_hierarchy = 'download_time'
    
    def has_change_permission(self, request, obj=None):
        # 下载记录不应被修改
        return False

# 自定义管理仪表板
class CustomAdminSite(admin.AdminSite):
    name = 'music_admin'
    site_header = '音乐管理后台'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(views.admin_dashboard), name='dashboard')
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