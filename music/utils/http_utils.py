import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

def ajax_response(status=200, message='', data=None, errors=None):
    """
    创建标准的AJAX JSON响应
    
    参数:
        status: HTTP状态码
        message: 响应消息
        data: 响应数据
        errors: 错误字典
    返回:
        JsonResponse对象
    """
    response_data = {
        'status': 'success' if status < 400 else 'error',
        'message': message
    }
    
    if data is not None:
        response_data['data'] = data
        
    if errors is not None:
        response_data['errors'] = errors
        
    return JsonResponse(response_data, status=status)

def render_template_fragment(request, template_name, context=None):
    """
    渲染模板片段，用于AJAX请求
    
    参数:
        request: 请求对象
        template_name: 模板名称
        context: 模板上下文
    返回:
        HTML字符串
    """
    context = context or {}
    html = render_to_string(template_name, context, request=request)
    return html

def is_ajax(request):
    """
    检查请求是否为AJAX请求
    Django 3.1后移除了request.is_ajax()方法，这是替代方案
    
    参数:
        request: 请求对象
    返回:
        布尔值
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def ajax_or_template_response(request, template_name, context=None, json_data=None):
    """
    根据请求类型返回AJAX或模板响应
    
    参数:
        request: 请求对象
        template_name: 模板名称
        context: 模板上下文
        json_data: AJAX响应数据
    返回:
        HttpResponse或JsonResponse对象
    """
    context = context or {}
    json_data = json_data or {}
    
    if is_ajax(request):
        # 如果请求要求HTML片段
        if request.GET.get('html', False):
            html = render_template_fragment(request, template_name, context)
            return HttpResponse(html)
        # 否则返回JSON
        return JsonResponse(json_data)
    else:
        # 返回完整的模板响应
        return render(request, template_name, context)

def paginated_response(paginator, page_obj, template_name=None, request=None, extra_context=None):
    """
    创建分页响应，支持普通和AJAX请求
    
    参数:
        paginator: 分页器对象
        page_obj: 当前页面对象
        template_name: 模板名称 (AJAX请求需要)
        request: 请求对象 (AJAX请求需要)
        extra_context: 额外的上下文数据
    返回:
        字典或HttpResponse
    """
    extra_context = extra_context or {}
    
    response_data = {
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        **extra_context
    }
    
    if request and is_ajax(request) and template_name:
        # 如果是AJAX请求并提供了模板名称
        context = {
            'page_obj': page_obj,
            'paginator': paginator,
            **extra_context
        }
        html = render_template_fragment(request, template_name, context)
        response_data['html'] = html
        return JsonResponse(response_data)
    
    return response_data 