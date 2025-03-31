from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid
import os

def audio_upload_path(instance, filename):
    # 获取原始文件扩展名并保持小写
    ext = filename.split('.')[-1].lower()
    # 生成唯一文件名，同时保留原始扩展名
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('music', filename)

class Music(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    artist = models.CharField(max_length=100, verbose_name='艺术家')
    album = models.CharField(max_length=100, verbose_name='专辑')
    release_date = models.DateField(verbose_name='发行日期')
    audio_file = models.FileField(upload_to=audio_upload_path, verbose_name='音频文件')
    cover_image = models.ImageField(
        upload_to='covers/%Y/%m/%d/',
        blank=True, 
        null=True,
        verbose_name='歌曲封面',
        help_text='建议尺寸：500x500像素，支持JPG/PNG格式'
    )
    lyrics = models.TextField(blank=True, null=True, verbose_name='歌词')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='上传者')
    play_count = models.PositiveIntegerField(default=0, verbose_name='播放量')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    is_original = models.BooleanField(default=False, verbose_name='是否原创')
    category = models.CharField(max_length=20, choices=(
        ('pop', '流行'),
        ('rock', '摇滚'),
        ('classical', '古典')
    ), default='pop', verbose_name='分类')
    download_count = models.PositiveIntegerField(default=0, verbose_name='下载次数')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']
        verbose_name = '音乐作品'
        verbose_name_plural = '音乐作品管理'
    
    @property
    def file_size(self):
        """获取文件大小"""
        try:
            return self.audio_file.size
        except:
            return 0

    def file_exists(self, field_name):
        """检查文件是否存在的通用方法"""
        field = getattr(self, field_name, None)
        return field.storage.exists(field.name) if field else False
        
    def audio_file_exists(self):
        return self.file_exists('audio_file')

    def cover_image_exists(self):
        return self.file_exists('cover_image')

class Profile(models.Model):
    """用户扩展资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='个人简介')
    avatar = ResizedImageField(
        size=[200, 200],
        quality=85,
        upload_to='avatars/%Y/%m/%d/',
        default='avatars/default.png',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png'],
                message="仅支持JPG/PNG格式图片"
            )
        ],
        verbose_name='头像',
        crop=['middle', 'center']
    )
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地')
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name='个人网站')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.user.username}的个人资料'

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料管理'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Comment(models.Model):
    """音乐评论"""
    music = models.ForeignKey(Music, related_name='comments', on_delete=models.CASCADE, verbose_name='关联音乐')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.music.title}'

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = '评论管理'

class MusicDownload(models.Model):
    """音乐下载记录"""
    music = models.ForeignKey(Music, related_name='downloads', on_delete=models.CASCADE, verbose_name='下载音乐')
    user = models.ForeignKey(User, related_name='music_downloads', on_delete=models.CASCADE, verbose_name='下载用户')
    download_time = models.DateTimeField(auto_now_add=True, verbose_name='下载时间')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    
    def __str__(self):
        return f'{self.user.username} 下载了 {self.music.title} 于 {self.download_time}'
    
    class Meta:
        verbose_name = '下载记录'
        verbose_name_plural = '下载记录管理'
        ordering = ['-download_time']

class AdminLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    target = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} {self.action} {self.target}"

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '系统日志'

class ChatMessage(models.Model):
    """AI聊天消息记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    message = models.TextField(verbose_name='用户消息')
    response = models.TextField(verbose_name='AI回复')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return f"{self.user.username}的对话 - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = 'AI聊天记录'
        verbose_name_plural = 'AI聊天记录'
        ordering = ['-created_at']

class FAQEntry(models.Model):
    """常见问题解答条目"""
    question = models.CharField(max_length=200, verbose_name='常见问题')
    answer = models.TextField(verbose_name='回答内容')
    keywords = models.CharField(max_length=200, verbose_name='关键词', help_text='多个关键词用逗号分隔', blank=True)
    category = models.CharField(max_length=50, choices=(
        ('account', '账号相关'),
        ('music', '音乐相关'),
        ('website', '网站功能'),
        ('other', '其他')
    ), default='other', verbose_name='分类')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = '常见问答'
        verbose_name_plural = '常见问答管理'
        ordering = ['category', '-updated_at']

class UnknownQuery(models.Model):
    """记录机器人无法回答的问题，用于训练和改进"""
    query = models.TextField(verbose_name='问题内容')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='提问用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    is_resolved = models.BooleanField(default=False, verbose_name='是否已解决')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='resolved_queries', verbose_name='解决人')
    suggested_answer = models.TextField(blank=True, null=True, verbose_name='建议回答')
    
    def __str__(self):
        return f"未解决问题: {self.query[:30]}..." if len(self.query) > 30 else self.query
    
    class Meta:
        verbose_name = '未解决问题'
        verbose_name_plural = '未解决问题管理'
        ordering = ['-created_at']

class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_history')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='play_history')
    played_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-played_at']
        verbose_name = '播放历史'
        verbose_name_plural = '播放历史'
    
    def __str__(self):
        return f"{self.user.username} 播放了 {self.music.title}"
