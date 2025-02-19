from django.contrib.auth.models import User # 用户个人资料管理
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator

class Music(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题') # 标题
    artist = models.CharField(max_length=100, verbose_name='艺术家')
    album = models.CharField(max_length=100, verbose_name='专辑')
    release_date = models.DateField(verbose_name='发行日期')
    audio_file = models.FileField(upload_to='music/', verbose_name='音频文件')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='歌曲封面')
    lyrics = models.TextField(blank=True, null=True, verbose_name='歌词')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='上传者')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']  # 按发行日期倒序排列
        
    def get_duration(self):
        """获取音频时长（待实现）"""
        pass
    
    @property
    def file_size(self):
        """获取文件大小"""
        try:
            return self.audio_file.size
        except:
            return 0

class Profile(models.Model):
    """用户扩展资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    bio = models.TextField(blank=True, null=True, verbose_name='个人简介')
    avatar = ResizedImageField(
        size=[200, 200],
        quality=85,
        upload_to='avatars/%Y/%m/%d/',
        default='avatars/default.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name='头像'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='所在地'
    )

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
    """音乐评论"""
    music = models.ForeignKey(Music, related_name='comments', on_delete=models.CASCADE, verbose_name='关联音乐')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.music.title}'
