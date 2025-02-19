# music/admin.py
from django.contrib import admin
from .models import Music, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('music', 'user', 'created_at', 'content')  # 显示字段
    list_filter = ('music', 'user')  # 过滤器
    search_fields = ('content',)  # 搜索字段
    ordering = ('-created_at',)  # 默认排序

    def get_queryset(self, request):
        # 超级用户可以看到所有评论，普通用户只能看到自己的评论
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def has_delete_permission(self, request, obj=None):
        # 只有超级用户有删除权限
        return request.user.is_superuser

admin.site.register(Music)
admin.site.register(Comment, CommentAdmin)