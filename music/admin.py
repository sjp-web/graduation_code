# music/admin.py
from django.contrib import admin
from .models import Music, Comment, Profile, AdminLog
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from rangefilter.filters import DateRangeFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.models import User
from django.utils import timezone

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
    
    def action_type(self, obj):
        color = {
            'create': 'success',
            'update': 'warning',
            'delete': 'danger'
        }.get(obj.action.lower(), 'primary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.action
        )
    action_type.short_description = '操作类型'

    def target_info(self, obj):
        return format_html('<code>{}</code>', obj.target)
    target_info.short_description = '操作目标'

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'change_message']
    list_filter = ['action_time', 'content_type']
    search_fields = ['user__username', 'object_repr']
    date_hierarchy = 'action_time'

# 自定义管理仪表板
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='admin_dashboard'),
        ]
        return custom_urls + urls

    # 添加Jazzmin需要的菜单配置
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                'name': '数据看板',
                'app_label': 'custom_dashboard',
                'models': [
                    {
                        'name': '仪表盘',
                        'object_name': 'dashboard',
                        'admin_url': self.reverse('admin_dashboard'),
                        'view_only': True,
                        'permissions': ['auth.view_user']
                    }
                ],
                'icon': 'fas fa-chart-line',
                'app_url': self.reverse('admin_dashboard')
            }
        ]
        return app_list

    def reverse(self, view_name):
        return f'/admin/{view_name}/'

@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_users': User.objects.count(),
        'total_music': Music.objects.count(),
        'new_users': User.objects.filter(date_joined__date=timezone.now().date()).count(),
        'popular_music': Music.objects.order_by('-play_count')[:5],
        'recent_comments': Comment.objects.select_related('user', 'music').order_by('-created_at')[:5]
    }
    return render(request, 'music/dashboard.html', {'stats': stats})

admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(Music, MusicAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Profile, ProfileAdmin)
admin_site.register(AdminLog, AdminLogAdmin)
admin_site.register(LogEntry, LogEntryAdmin)