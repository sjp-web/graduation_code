
from django.contrib.auth.models import User # 用户个人资料管理
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Music(models.Model):
    title = models.CharField(max_length=200) # 标题
    artist = models.CharField(max_length=100) # 艺术家
    album = models.CharField(max_length=100) # 专辑
    release_date = models.DateField() # 发售日期
    audio_file = models.FileField(upload_to='music/')  #音频文件
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True) #封面图像
    lyrics = models.TextField(null=True, blank=True) # 歌词
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # 关联用户

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 与用户一对一关联
    bio = models.TextField(blank=True, null=True) # 简介
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True) # 头像

    def __str__(self):
        return self.user.username

# models.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    # 确保没有再次调用用户的 save() 方法
    pass  # 不需要执行任何操作

# 音乐评论系统
class Comment(models.Model):
    music = models.ForeignKey(Music, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.music.title}'
