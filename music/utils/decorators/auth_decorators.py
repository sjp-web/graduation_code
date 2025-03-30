from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _

def owner_required(view_func):
    """
    确保只有资源的拥有者才能访问
    
    用法：
    @owner_required
    def edit_music(request, music_id):
        music = get_object_or_404(Music, pk=music_id)
        ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 获取音乐ID
        music_id = kwargs.get('music_id')
        if not music_id:
            return HttpResponseForbidden("没有指定资源ID")
            
        # 导入模型
        from ...models import Music
        
        # 获取音乐对象
        try:
            music = Music.objects.get(pk=music_id)
        except Music.DoesNotExist:
            return HttpResponseForbidden("资源不存在")
            
        # 检查当前用户是否为上传者
        if music.uploaded_by != request.user and not request.user.is_staff:
            messages.error(request, "您没有权限执行此操作")
            return redirect('music_detail', music_id=music_id)
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def redirect_authenticated_user(view_func):
    """
    如果用户已登录，则重定向到音乐列表页面
    用于登录和注册页面

    用法：
    @redirect_authenticated_user
    def login_view(request):
        ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('music_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def profile_required(view_func):
    """
    确保用户已创建个人资料才能访问
    如果未创建，重定向到创建资料页面

    用法：
    @profile_required
    def upload_music(request):
        ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 确保用户已登录（这个装饰器应该与login_required一起使用）
        if not request.user.is_authenticated:
            return redirect('login')
            
        # 检查用户是否有资料
        try:
            if not hasattr(request.user, 'profile') or not request.user.profile:
                messages.warning(request, "请先完善您的个人资料")
                return redirect('profile_creation')
        except:
            messages.warning(request, "请先完善您的个人资料")
            return redirect('profile_creation')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view 