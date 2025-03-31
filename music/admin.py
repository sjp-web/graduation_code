# music/admin.py
from django.contrib import admin
from .models import Music, Comment, Profile, AdminLog, MusicDownload, ChatMessage, FAQEntry, UnknownQuery
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from django.urls import path
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .views import admin_dashboard
from django.db.models import Count
from django.http import HttpResponse
from .utils.string_utils import truncate_text

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
    actions = ['export_selected_items']
    
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
        """显示封面预览"""
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.cover_image.url)
        return "-"
    cover_preview.short_description = '封面预览'

    def upload_status(self, obj):
        """显示上传状态标签"""
        is_uploaded = bool(obj.audio_file)
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            'success' if is_uploaded else 'danger',
            '已上传' if is_uploaded else '未上传'
        )
    upload_status.short_description = '上传状态'

    def save_model(self, request, obj, form, change):
        """保存模型时自动设置上传者"""
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
        
    def export_selected_items(self, request, queryset):
        """导出选中项目"""
        resource = self.resource_class()
        dataset = resource.export(queryset)
        
        # 根据请求的格式导出
        format_type = request.POST.get('file_format', 'csv')
        content_types = {
            'csv': 'text/csv',
            'json': 'application/json',
            'xls': 'application/vnd.ms-excel',
        }
        
        content_type = content_types.get(format_type, 'text/csv')
        response = HttpResponse(content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="music_export.{format_type}"'
        
        # 导出到响应
        if format_type == 'json':
            response.write(dataset.json)
        elif format_type == 'xls':
            dataset.xls.save(response)
        else:  # 默认CSV
            response.write(dataset.csv)
            
        return response
    export_selected_items.short_description = "导出选中记录"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'user_display', 'music_link', 'created_at', 'is_recent')
    search_fields = ('content', 'user__username', 'user__profile__nickname', 'music__title')
    list_filter = (('created_at', DateRangeFilter),)
    list_select_related = ('user', 'music', 'user__profile')
    
    def get_admin_url(self, app_label, model_name, obj_id, admin_site_name='music-admin'):
        """获取管理界面URL"""
        return f'/{admin_site_name}/{app_label}/{model_name}/{obj_id}/change/'
    
    def music_link(self, obj):
        url = self.get_admin_url('music', 'music', obj.music.id)
        return format_html('<a href="{}">{}</a>', url, obj.music.title)
    music_link.short_description = '关联音乐'

    def user_display(self, obj):
        nickname = getattr(obj.user.profile, 'nickname', None) if hasattr(obj.user, 'profile') else None
        if nickname:
            return format_html('{} <span class="text-muted">({}))</span>', nickname, obj.user.username)
        return obj.user.username
    user_display.short_description = '用户'
    
    def is_recent(self, obj):
        return obj.created_at > timezone.now() - timezone.timedelta(days=3)
    is_recent.boolean = True
    is_recent.short_description = '近期评论'

    def truncated_content(self, obj):
        return truncate_text(obj.content)
    truncated_content.short_description = '评论内容'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'avatar_preview', 'music_count', 'last_activity')
    search_fields = ('user__username', 'nickname', 'bio')
    readonly_fields = ('music_count', 'avatar_edit_preview')
    fieldsets = (
        ('用户信息', {
            'fields': ('user', 'nickname', 'bio', 'avatar_edit_preview', 'avatar', 'location', 'website')
        }),
        ('统计信息', {
            'fields': ('music_count',),
            'classes': ('collapse',)
        }),
    )
    
    def _get_avatar_html(self, obj, max_height=50, extra_style=''):
        """生成头像预览HTML的通用方法"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height:{}px;{}" />',
                obj.avatar.url, max_height, extra_style
            )
        return format_html('<p style="color:#999;">未设置头像</p>')
    
    def avatar_preview(self, obj):
        return self._get_avatar_html(obj)
    avatar_preview.short_description = '头像预览'

    def avatar_edit_preview(self, obj):
        if obj.avatar:
            html = self._get_avatar_html(
                obj, 
                max_height=150, 
                extra_style='border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);'
            )
            return format_html(
                '<div style="margin-bottom:10px;">{}'
                '<p style="margin-top:5px; font-size:12px; color:#666;">当前头像预览</p>'
                '</div>',
                html
            )
        return self._get_avatar_html(obj)
    avatar_edit_preview.short_description = '头像预览'

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

@admin.register(MusicDownload)
class MusicDownloadAdmin(admin.ModelAdmin):
    list_display = ('music_title', 'user_username', 'download_time', 'ip_address', 'status_tag')
    list_filter = (('download_time', DateRangeFilter), 'user')
    search_fields = ('music__title', 'user__username', 'ip_address')
    date_hierarchy = 'download_time'
    list_per_page = 20
    readonly_fields = ('music', 'user', 'download_time', 'ip_address')
    actions = ['export_csv', 'export_excel']
    
    def has_change_permission(self, request, obj=None):
        # 下载记录不应被修改
        return False
        
    def has_add_permission(self, request):
        # 不允许手动添加下载记录
        return False
    
    def get_admin_url(self, app_label, model_name, obj_id, admin_site_name='music-admin'):
        """获取管理界面URL"""
        return f'/{admin_site_name}/{app_label}/{model_name}/{obj_id}/change/'
        
    def music_title(self, obj):
        """显示音乐标题并链接到音乐详情页"""
        url = self.get_admin_url('music', 'music', obj.music.id)
        return format_html('<a href="{}">{}</a>', url, obj.music.title)
    music_title.short_description = '音乐作品'
    music_title.admin_order_field = 'music__title'
    
    def user_username(self, obj):
        """显示用户名并链接到用户详情页"""
        url = self.get_admin_url('auth', 'user', obj.user.id)
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_username.short_description = '下载用户'
    user_username.admin_order_field = 'user__username'
    
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
    
    def _get_export_data(self, queryset, include_artist=False):
        """获取导出数据的通用方法"""
        # 准备表头
        headers = ['音乐标题']
        if include_artist:
            headers.append('艺术家')
        headers.extend(['下载用户', '下载时间', 'IP地址'])
        
        # 准备数据行
        rows = []
        for record in queryset:
            row = [record.music.title]
            if include_artist:
                row.append(record.music.artist)
            row.extend([
                record.user.username,
                record.download_time.strftime('%Y-%m-%d %H:%M:%S'),
                record.ip_address or '-'
            ])
            rows.append(row)
            
        return headers, rows
    
    def export_csv(self, request, queryset):
        """导出选中的下载记录为CSV文件"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="download_records.csv"'
        
        writer = csv.writer(response)
        headers, rows = self._get_export_data(queryset)
        
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
            
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
        
        # 获取数据
        headers, rows = self._get_export_data(queryset, include_artist=True)
        
        # 写入标题行
        for col_num, column_title in enumerate(headers):
            ws.write(0, col_num, column_title, header_style)
        
        # 写入数据行
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'YYYY-MM-DD HH:MM:SS'
        
        for row_num, row_data in enumerate(rows, 1):
            for col_num, cell_value in enumerate(row_data):
                # 为日期列应用特殊样式
                if col_num == 3 and isinstance(cell_value, str) and len(cell_value) == 19:
                    # 日期列，但由于已转换为字符串，不再需要特殊处理
                    ws.write(row_num, col_num, cell_value)
                else:
                    ws.write(row_num, col_num, cell_value)
            
        wb.save(response)
        return response
    export_excel.short_description = "导出所选记录为Excel"
    
    def _get_period_count(self, period_filter):
        """获取指定时段的下载计数"""
        return MusicDownload.objects.filter(**period_filter).count()
        
    def changelist_view(self, request, extra_context=None):
        """增强下载记录列表视图，添加统计信息"""
        # 添加基本统计数据
        extra_context = extra_context or {}
        
        # 使用timezone获取当前日期
        today = timezone.now().date()
        
        # 构建各时段的过滤条件
        period_filters = {
            'today': {'download_time__date': today},
            'week': {'download_time__date__gte': today - timezone.timedelta(days=today.weekday())},
            'month': {'download_time__date__gte': today.replace(day=1)}
        }
        
        # 获取各时段的下载量
        counts = {
            f"{period}_count": self._get_period_count(filters)
            for period, filters in period_filters.items()
        }
        
        # 使用同一个查询注解方式获取统计数据
        top_music = MusicDownload.objects.values('music__title', 'music__artist').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        active_users = MusicDownload.objects.values('user__username').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # 构建统计信息上下文
        stats = {
            'title': '下载记录管理',
            'total_count': MusicDownload.objects.count(),
            'top_music': top_music,
            'active_users': active_users
        }
        
        # 添加各时段下载量
        stats.update(counts)
        
        extra_context.update(stats)
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_message', 'short_response', 'created_at', 'time_since')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'message', 'response')
    date_hierarchy = 'created_at'
    list_per_page = 20
    readonly_fields = ('user', 'message', 'response', 'created_at')
    
    def short_message(self, obj):
        return truncate_text(obj.message, 50)
    
    def short_response(self, obj):
        return truncate_text(obj.response, 50)
    
    def time_since(self, obj):
        """显示距离现在的时间"""
        from django.utils.timesince import timesince
        return f"{timesince(obj.created_at, timezone.now())}前"
    
    short_message.short_description = '用户消息'
    short_response.short_description = 'AI回复'
    time_since.short_description = '时间'

    actions = ['create_faq_from_chat']
    
    def create_faq_from_chat(self, request, queryset):
        """将聊天记录转换为FAQ"""
        for chat in queryset:
            FAQEntry.objects.create(
                question=chat.message,
                answer=chat.response,
                category='other'
            )
        self.message_user(request, f"已从{queryset.count()}条聊天记录创建FAQ")
    
    create_faq_from_chat.short_description = "将选中的聊天记录转为FAQ"

@admin.register(FAQEntry)
class FAQEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'short_answer', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'keywords')
    list_editable = ('is_active',)
    fieldsets = (
        ('基本信息', {
            'fields': ('question', 'answer', 'category', 'is_active')
        }),
        ('高级选项', {
            'fields': ('keywords',),
            'classes': ('collapse',)
        }),
    )
    
    def short_answer(self, obj):
        return truncate_text(obj.answer, 50)
    
    short_answer.short_description = '回答摘要'

@admin.register(UnknownQuery)
class UnknownQueryAdmin(admin.ModelAdmin):
    list_display = ('query_excerpt', 'user', 'created_at', 'is_resolved', 'resolved_by')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('query', 'user__username')
    readonly_fields = ('query', 'user', 'created_at')
    fieldsets = (
        ('问题信息', {
            'fields': ('query', 'user', 'created_at')
        }),
        ('解决方案', {
            'fields': ('is_resolved', 'resolved_by', 'suggested_answer')
        }),
    )
    
    def query_excerpt(self, obj):
        return truncate_text(obj.query, 50)
    
    query_excerpt.short_description = '问题内容'
    
    actions = ['mark_as_resolved', 'create_faq']
    
    def mark_as_resolved(self, request, queryset):
        """将问题标记为已解决"""
        queryset.update(is_resolved=True, resolved_by=request.user)
        self.message_user(request, f"已将{queryset.count()}个问题标记为已解决")
    
    def create_faq(self, request, queryset):
        """从未解决问题创建FAQ"""
        count = 0
        for query in queryset:
            if query.suggested_answer:
                FAQEntry.objects.create(
                    question=query.query,
                    answer=query.suggested_answer,
                    category='other'
                )
                query.is_resolved = True
                query.resolved_by = request.user
                query.save()
                count += 1
        
        self.message_user(request, f"已从{count}个未解决问题创建FAQ")
    
    mark_as_resolved.short_description = "标记为已解决"
    create_faq.short_description = "从选中问题创建FAQ"

# 自定义管理仪表板
class CustomAdminSite(admin.AdminSite):
    name = 'music-admin'
    site_header = '音乐管理后台'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='dashboard'),
        ]
        return custom_urls + urls
    
    def get_model_url(self, app_label, model_name, obj_id=None, action='change'):
        """获取模型URL的通用方法"""
        url = f'/{self.name}/{app_label}/{model_name}/'
        if obj_id is not None:
            url += f'{obj_id}/{action}/'
        return url
    
    def get_app_list(self, request, app_label=None):
        # 获取原始应用列表
        app_list = super().get_app_list(request, app_label)
        
        # 如果是特定应用标签的请求，不添加自定义看板
        if app_label:
            return app_list
        
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
        
        # 定义应用分类
        app_categories = {
            'logs': {'name': '系统日志', 'order': 99},  # 放在最后
            'interaction': {'name': '用户互动', 'order': 2},
            'content': {'name': '内容管理', 'order': 1},
            'user_management': {'name': '用户管理', 'order': 3}
        }
        
        # 初始化分类应用
        categorized_apps = {
            category: {
                'name': details['name'],
                'app_label': category,
                'app_url': '#',
                'has_module_perms': True,
                'models': [],
                'order': details['order']
            } for category, details in app_categories.items()
        }
        
        # 模型分类规则
        model_categorization = {
            'logs': lambda name: 'log' in name or 'adminlog' in name or 'logentry' in name,
            'interaction': lambda name: 'comment' in name or 'chatmessage' in name or 'download' in name,
            'content': lambda name: 'music' in name and 'download' not in name,
            'user_management': lambda name: 'user' in name or 'profile' in name or 'group' in name
        }
        
        # 整理应用列表
        remaining_apps = []
        for app in app_list:
            models_to_remove = []
            for model in app.get('models', []):
                object_name = model.get('object_name', '').lower()
                
                # 将模型放入相应分类
                categorized = False
                for category, match_func in model_categorization.items():
                    if match_func(object_name):
                        categorized_apps[category]['models'].append(model)
                        models_to_remove.append(model)
                        categorized = True
                        break
                
                if not categorized:
                    # 保留未分类的模型
                    pass
            
            # 从原应用中移除已分类的模型
            for model in models_to_remove:
                app['models'].remove(model)
            
            # 保留未分类的应用
            if app.get('models'):
                remaining_apps.append(app)
        
        # 构建最终的导航结构
        result = [dashboard_app]
        
        # 按顺序添加有内容的分类
        for category, app_info in sorted(categorized_apps.items(), key=lambda x: x[1]['order']):
            if app_info['models']:
                result.append(app_info)
        
        # 添加未分类的应用
        result.extend(remaining_apps)
        
        return result

    def _get_admin_url(self, name):
        return f'/{self.name}/{name}/'

# 注册Django默认的User和Group模型
admin_site = CustomAdminSite(name='music-admin')

# 使用字典批量注册模型到自定义管理站点
admin_models = {
    Music: MusicAdmin,
    Comment: CommentAdmin,
    Profile: ProfileAdmin,
    AdminLog: AdminLogAdmin,
    MusicDownload: MusicDownloadAdmin,
    ChatMessage: ChatMessageAdmin,
    FAQEntry: FAQEntryAdmin,
    UnknownQuery: UnknownQueryAdmin,
    User: admin.ModelAdmin,  # 使用默认ModelAdmin
    Group: admin.ModelAdmin   # 使用默认ModelAdmin
}

# 批量注册所有模型
for model, admin_class in admin_models.items():
    admin_site.register(model, admin_class)