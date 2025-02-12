# music/admin.py
from django.contrib import admin
from .models import Music, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('music', 'user', 'created_at', 'content')
    list_filter = ('music', 'user')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        # 仅当用户是超级用户时，显示所有评论
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)  # 普通用户只看到自己的评论

    def has_delete_permission(self, request, obj=None):
        # 只有超级用户可以删除评论
        return request.user.is_superuser

admin.site.register(Music)
admin.site.register(Comment, CommentAdmin)