import os
import re
from django.conf import settings
import mimetypes

def validate_file_type(file, allowed_types=None):
    """
    验证文件类型是否允许
    
    参数:
        file: 上传的文件对象
        allowed_types: 允许的MIME类型列表
    返回:
        (bool, str): (是否有效, 错误信息)
    """
    if not file:
        return False, "没有提供文件"
        
    # 默认允许的文件类型
    if allowed_types is None:
        allowed_types = [
            'audio/mpeg',          # MP3
            'audio/wav',           # WAV
            'audio/ogg',           # OGG
            'audio/flac',          # FLAC
            'image/jpeg',          # JPEG
            'image/png',           # PNG
            'image/gif',           # GIF
            'application/pdf'      # PDF
        ]
    
    # 获取文件扩展名并推断MIME类型
    file_name = file.name
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # 使用mimetypes库猜测MIME类型
    guessed_type = mimetypes.guess_type(file_name)[0]
    
    # 如果无法猜测，则基于扩展名进行简单匹配
    if not guessed_type:
        ext_to_type = {
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf'
        }
        guessed_type = ext_to_type.get(file_ext)
    
    if not guessed_type or guessed_type not in allowed_types:
        return False, f"不支持的文件类型: {file_ext}，允许的类型: {', '.join(allowed_types)}"
    
    return True, "文件类型有效"

def validate_file_size(file, max_size_mb=10):
    """
    验证文件大小是否在允许范围内
    
    参数:
        file: 上传的文件对象
        max_size_mb: 最大允许大小（MB）
    返回:
        (bool, str): (是否有效, 错误信息)
    """
    if not file:
        return False, "没有提供文件"
        
    # 将MB转换为字节
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        return False, f"文件太大。最大允许大小: {max_size_mb}MB，当前文件大小: {file.size / (1024*1024):.2f}MB"
    
    return True, "文件大小有效"

def scan_text_content(text, blacklist=None):
    """
    扫描文本内容，检查是否包含不适当内容
    
    参数:
        text: 待检查的文本
        blacklist: 黑名单关键词列表
    返回:
        (bool, str): (是否安全, 错误信息)
    """
    if not text:
        return True, "内容为空"
        
    # 默认黑名单关键词
    if blacklist is None:
        blacklist = [
            # 这里可以添加不适当的关键词
            # 实际应用中应该从配置或数据库加载
        ]
    
    # 转换为小写以进行不区分大小写的匹配
    text_lower = text.lower()
    
    # 检查是否包含黑名单关键词
    for word in blacklist:
        if word.lower() in text_lower:
            return False, f"内容包含不适当的词语: {word}"
    
    # 检查是否包含URL
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    if urls and len(urls) > 5:  # 如果包含超过5个URL，可能是垃圾信息
        return False, "内容包含过多的URL链接"
    
    # 检查重复字符（可能是垃圾信息）
    for char in set(text):
        if text.count(char) > len(text) * 0.5 and len(text) > 10:  # 如果某个字符占比超过50%
            return False, "内容包含大量重复字符"
    
    return True, "内容安全"

def get_client_ip(request):
    """
    获取客户端IP地址
    
    参数:
        request: HTTP请求对象
    返回:
        IP地址字符串
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 