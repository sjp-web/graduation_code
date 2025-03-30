import re
import html
from django.utils.text import slugify

def clean_text(text):
    """
    清理文本内容，移除HTML标签和多余空白
    
    参数:
        text: 需要清理的文本
    返回:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除HTML标签
    clean = re.sub(r'<[^>]*>', '', text)
    # 转换HTML实体
    clean = html.unescape(clean)
    # 替换多个空格为单个空格
    clean = re.sub(r'\s+', ' ', clean)
    # 移除首尾空白
    clean = clean.strip()
    
    return clean

def format_lyrics(lyrics_text):
    """
    格式化歌词文本，处理时间标签和结构
    
    参数:
        lyrics_text: 原始歌词文本
    返回:
        格式化后的歌词列表，每个元素为一行
    """
    if not lyrics_text:
        return []
        
    # 移除时间标签 [00:01.02]
    cleaned_lyrics = re.sub(r'\[\d{2}:\d{2}\.\d{2}\]', '', lyrics_text)
    
    # 按行分割
    lines = cleaned_lyrics.splitlines()
    
    # 移除空行前后的空白并过滤空行
    formatted_lines = [line.strip() for line in lines]
    
    return formatted_lines

def generate_slug(text):
    """
    生成SEO友好的URL slug
    
    参数:
        text: 原始文本
    返回:
        格式化后的slug
    """
    # 使用django的slugify函数
    return slugify(text)

def truncate_text(text, max_length=100, suffix='...'):
    """
    截断文本到指定长度，添加后缀
    
    参数:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后添加的后缀
    返回:
        截断后的文本
    """
    if not text:
        return ""
        
    if len(text) <= max_length:
        return text
        
    # 截断到最大长度
    truncated = text[:max_length].strip()
    
    # 确保不会截断单词
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
        
    # 添加后缀
    return truncated + suffix

def format_file_size(size_in_bytes):
    """
    将字节大小格式化为易读形式
    
    参数:
        size_in_bytes: 字节大小
    返回:
        格式化后的大小字符串 (如 "1.5 MB")
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes/1024:.1f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_in_bytes/(1024*1024*1024):.1f} GB" 