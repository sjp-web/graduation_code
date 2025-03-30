import time
import logging
import functools
from django.core.cache import cache
from django.utils.encoding import force_str
from django.conf import settings
import hashlib
import json

logger = logging.getLogger('music')

def timed_execution(view_func):
    """
    记录视图函数执行时间的装饰器
    
    用法：
    @timed_execution
    def my_view(request):
        ...
    """
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        start_time = time.time()
        response = view_func(request, *args, **kwargs)
        execution_time = time.time() - start_time
        
        # 记录执行时间
        logger.info(f'视图 {view_func.__name__} 执行时间: {execution_time:.4f}秒')
        
        # 如果执行时间过长，发出警告
        if execution_time > 1.0:  # 大于1秒的请求被认为是慢请求
            logger.warning(f'慢请求: {view_func.__name__} 耗时 {execution_time:.4f}秒')
            
        return response
    return _wrapped_view

def cache_page_for_user(timeout=60*15):
    """
    基于用户的页面缓存装饰器
    为每个用户缓存不同的结果

    用法：
    @cache_page_for_user(timeout=60*5)  # 缓存5分钟
    def profile_view(request):
        ...
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != 'GET':
                # 只缓存GET请求
                return view_func(request, *args, **kwargs)

            # 创建缓存键，包含用户ID和请求路径
            if request.user.is_authenticated:
                user_id = request.user.id
            else:
                user_id = 'anonymous'
            
            cache_key = f'view_cache_{user_id}_{request.path}'
            
            # 尝试从缓存获取
            response = cache.get(cache_key)
            if response is not None:
                return response
            
            # 执行视图函数
            response = view_func(request, *args, **kwargs)
            
            # 缓存结果
            cache.set(cache_key, response, timeout)
            
            return response
        return _wrapped_view
    return decorator

def cache_result(timeout=60*60, key_prefix='cache'):
    """
    缓存函数结果的装饰器
    适用于任何返回可序列化数据的函数

    用法：
    @cache_result(timeout=60*60)  # 缓存1小时
    def expensive_calculation(param1, param2):
        ...
    """
    def decorator(func):
        @functools.wraps(func)
        def _wrapped_func(*args, **kwargs):
            # 创建缓存键
            key_parts = [key_prefix, func.__name__]
            
            # 添加位置参数
            for arg in args:
                key_parts.append(force_str(arg))
                
            # 添加关键字参数（排序以确保一致性）
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}:{force_str(v)}")
            
            # 创建最终的缓存键
            cache_key = hashlib.md5('_'.join(key_parts).encode()).hexdigest()
            
            # 尝试从缓存获取
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 缓存结果
            cache.set(cache_key, result, timeout)
            
            return result
        return _wrapped_func
    return decorator 