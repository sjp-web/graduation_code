# Generated by Django 5.1.7 on 2025-03-31 15:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_chatmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_at', models.DateTimeField(auto_now_add=True)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='play_history', to='music.music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='play_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '播放历史',
                'verbose_name_plural': '播放历史',
                'ordering': ['-played_at'],
            },
        ),
    ]
