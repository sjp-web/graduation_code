# Generated by Django 5.1.6 on 2025-02-28 09:30

import django.core.validators
import django.db.models.deletion
import django_resized.forms
import music.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200)),
                ('target', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '系统日志',
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('artist', models.CharField(max_length=100, verbose_name='艺术家')),
                ('album', models.CharField(max_length=100, verbose_name='专辑')),
                ('release_date', models.DateField(verbose_name='发行日期')),
                ('audio_file', models.FileField(upload_to=music.models.audio_upload_path, verbose_name='音频文件')),
                ('cover_image', models.ImageField(blank=True, help_text='建议尺寸：500x500像素，支持JPG/PNG格式', null=True, upload_to='covers/%Y/%m/%d/', verbose_name='歌曲封面')),
                ('lyrics', models.TextField(blank=True, null=True, verbose_name='歌词')),
                ('play_count', models.PositiveIntegerField(default=0, verbose_name='播放量')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='点赞数')),
                ('is_original', models.BooleanField(default=False, verbose_name='是否原创')),
                ('category', models.CharField(choices=[('pop', '流行'), ('rock', '摇滚'), ('classical', '古典')], default='pop', max_length=20, verbose_name='分类')),
                ('download_count', models.PositiveIntegerField(default=0, verbose_name='下载次数')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
            ],
            options={
                'verbose_name': '音乐作品',
                'verbose_name_plural': '音乐作品管理',
                'ordering': ['-release_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='music.music', verbose_name='关联音乐')),
            ],
            options={
                'verbose_name': '用户评论',
                'verbose_name_plural': '评论管理',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='个人简介')),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], default='avatars/default.png', force_format=None, keep_meta=True, quality=85, scale=None, size=[200, 200], upload_to='avatars/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='仅支持JPG/PNG格式图片')], verbose_name='头像')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='所在地')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户资料',
                'verbose_name_plural': '用户资料',
            },
        ),
    ]
