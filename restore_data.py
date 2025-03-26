import os
import shutil
import django
from pathlib import Path

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
django.setup()

from music.models import Music
from django.contrib.auth.models import User

def restore_data():
    # 检查backup文件夹是否存在
    backup_dir = Path('backup')
    if not backup_dir.exists():
        print('backup文件夹不存在！')
        return

    # 恢复media文件夹
    media_backup = backup_dir / 'media'
    media_dir = Path('media')
    
    if media_backup.exists():
        if media_dir.exists():
            shutil.rmtree(media_dir)
        shutil.copytree(media_backup, media_dir)
        print('已恢复media文件夹')
    else:
        print('media备份文件夹不存在！')

    # 恢复数据库数据
    music_data_file = backup_dir / 'music_data.json'
    if music_data_file.exists():
        # 清空现有数据
        Music.objects.all().delete()
        
        # 导入备份数据
        with open(music_data_file, 'r', encoding='utf-8') as f:
            import json
            data = json.load(f)
            
            # 获取或创建默认用户
            default_user, created = User.objects.get_or_create(
                username='admin',
                defaults={'is_staff': True, 'is_superuser': True}
            )
            
            for item in data:
                fields = item['fields']
                # 设置上传者为默认用户
                fields['uploaded_by'] = default_user
                Music.objects.create(**fields)
        
        print('已恢复数据库数据')
    else:
        print('music_data.json文件不存在！')

if __name__ == '__main__':
    restore_data() 