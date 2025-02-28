# music/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    # 添加类型检查确保是表单字段
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    # 如果是字符串直接返回
    return field

@register.filter
def percentage(value, total):
    try:
        return "%.1f" % ((float(value) / float(total)) * 100)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def map_attribute(value, arg):
    """从字典列表或对象列表中提取指定属性"""
    if isinstance(value, list) and value:
        if isinstance(value[0], dict):
            return [item.get(arg) for item in value]
        else:
            return [getattr(item, arg) for item in value]
    return []