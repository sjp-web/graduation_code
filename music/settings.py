# music app的settings.py文件
# 定义URL反向查找的辅助函数

def get_admin_url(name):
    """
    获取管理后台URL的辅助函数
    """
    return f'/admin/{name}/'

def get_music_admin_url(name):
    """
    获取自定义音乐管理后台URL的辅助函数
    """
    return f'/music-admin/{name}/' 