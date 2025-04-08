import os
import logging
from django.http import Http404
from django.conf import settings

logger = logging.getLogger(__name__)

class FileExceptionMiddleware:
    """处理文件访问异常的中间件
    
    主要用于捕获文件不存在的异常，并返回适当的错误响应，
    避免因为文件不存在而导致500错误
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        return self.get_response(request)
        
    def process_exception(self, request, exception):
        # 处理文件不存在的异常
        if isinstance(exception, (FileNotFoundError, OSError)):
            # 记录错误
            logger.warning(
                f"文件访问异常: {str(exception)} "
                f"请求路径: {request.path} "
                f"用户: {request.user}"
            )
            
            # 检查是否是媒体文件请求
            if request.path.startswith(settings.MEDIA_URL):
                relative_path = request.path.replace(settings.MEDIA_URL, '')
                logger.warning(f"尝试访问不存在的媒体文件: {relative_path}")
                
                # 返回404响应
                raise Http404("请求的文件不存在")
                
        return None 