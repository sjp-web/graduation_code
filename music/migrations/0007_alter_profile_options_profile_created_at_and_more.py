# Generated by Django 5.1.7 on 2025-03-31 15:43

import django.core.validators
import django.utils.timezone
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_playhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': '用户资料', 'verbose_name_plural': '用户资料管理'},
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='个人网站'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], default='avatars/default.png', force_format=None, keep_meta=True, null=True, quality=85, scale=None, size=[200, 200], upload_to='avatars/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='仅支持JPG/PNG格式图片')], verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='个人简介'),
        ),
    ]
