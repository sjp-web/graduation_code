import os
from django.conf import settings

def get_audio_file_path(instance, filename):
    """
    生成上传的音频文件的路径
    
    参数:
        instance: 音乐实例
        filename: 原始文件名
    返回:
        文件应该保存的路径
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1].lower()
    # 仅支持的音频格式
    allowed_extensions = ['mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac']
    
    if ext not in allowed_extensions:
        # 默认返回mp3格式
        ext = 'mp3'
    
    # 使用实例的标题和艺术家名称构建文件名
    # 移除非法字符
    safe_title = "".join([c for c in instance.title if c.isalpha() or c.isdigit() or c == ' ']).strip()
    safe_artist = "".join([c for c in instance.artist if c.isalpha() or c.isdigit() or c == ' ']).strip()
    
    # 构建文件名
    safe_filename = f"{safe_artist}_{safe_title}.{ext}".replace(' ', '_')
    
    # 返回上传路径
    return os.path.join('music', 'audio', safe_filename)

def get_audio_metadata(file_path):
    """
    获取音频文件的元数据
    
    参数:
        file_path: 音频文件路径
    返回:
        包含元数据的字典
    """
    # 这个函数需要安装 mutagen 库
    # 暂时返回空字典，可以在后期实现
    return {} 