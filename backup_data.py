import os
import shutil
import django
from pathlib import Path

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
django.setup()

def backup_data():
    # 创建backup文件夹
    if not os.path.exists('backup'):
        os.makedirs('backup')

    # 备份media文件夹
    if os.path.exists('media'):
        if os.path.exists('backup/media'):
            shutil.rmtree('backup/media')
        shutil.copytree('media', 'backup/media')
        print("已备份media文件夹")

    # 备份数据库数据
    from music.models import Music
    from django.core.serializers import serialize
    data = serialize('json', Music.objects.all())
    with open('backup/music_data.json', 'w', encoding='utf-8') as f:
        f.write(data)
    print("已备份数据库数据")

    print("数据备份完成！")

if __name__ == '__main__':
    backup_data() 