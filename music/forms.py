from django import forms
from .models import Music
from .models import Profile
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import logging

# 音乐上传表单
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'category', 'release_date', 'audio_file', 'lyrics', 'cover_image']
        labels = {
            'title': '歌曲标题',
            'artist': '艺术家',
            'album': '专辑名称',
            'category': '音乐分类',
            'release_date': '发行日期',
            'audio_file': '音频文件',
            'lyrics': '歌词',
            'cover_image': '专辑封面'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入歌曲标题'}),
            'artist': forms.TextInput(attrs={'placeholder': '请输入艺术家名称'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'audio_file': forms.FileInput(attrs={
                'accept': '.mp3,.wav,.aac,.m4a',
                'class': 'form-control form-control-lg'
            }),
            'album': forms.TextInput(attrs={'placeholder': '专辑名称'}),
            'release_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control form-control-lg',
                    'placeholder': '年-月-日'
                }
            ),
            'lyrics': forms.Textarea(attrs={'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control form-control-lg'})
        }

    def clean_audio_file(self):
        # 验证音频文件大小和类型
        audio_file = self.cleaned_data.get('audio_file')
        if not audio_file:
            return None
            
        logger = logging.getLogger('music')
        
        # 文件大小验证（最大20MB）
        if audio_file.size > settings.MAX_UPLOAD_SIZE:
            logger.error(f"文件过大: {audio_file.name}, 大小: {audio_file.size}")
            raise ValidationError('文件大小不能超过20MB')
        
        # 文件类型验证 - 详细记录信息
        file_name = audio_file.name.lower()
        file_extension = file_name.split('.')[-1]
        content_type = audio_file.content_type
        
        # 记录上传文件信息到日志
        logger.info(f"文件上传: 名称={file_name}, 扩展名={file_extension}, MIME类型={content_type}, 大小={audio_file.size}字节")
        
        # 检查扩展名
        allowed_extensions = ['mp3', 'wav', 'aac', 'm4a']
        if file_extension not in allowed_extensions:
            logger.error(f"不支持的文件扩展名: {file_extension}")
            raise ValidationError(f'不支持的文件格式: {file_extension}，只支持MP3、WAV、AAC和M4A格式')
            
        # 检查MIME类型（宽松验证）
        allowed_mimetypes = [
            'audio/mpeg',          # MP3
            'audio/wav',           # WAV
            'audio/aac',           # AAC
            'audio/mp4',           # M4A (标准MIME类型)
            'audio/x-m4a',         # M4A (某些系统使用)
            'video/mp4',           # 某些系统将M4A识别为此类型
            'audio/x-hx-aac-adts', # AAC变种
            'application/octet-stream'  # 通用二进制流
        ]
        
        # 使用宽松验证，只有在content_type存在且不在允许列表中时才记录警告
        if content_type and content_type not in allowed_mimetypes:
            logger.warning(f"不常见的MIME类型: {content_type}，但由于扩展名有效，仍然允许上传")
        
        # 通过所有验证
        return audio_file

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2 or len(title) > 100:
            raise ValidationError('标题长度需在2-100个字符之间')
        return title

    def clean_artist(self):
        artist = self.cleaned_data.get('artist')
        if len(artist) < 2 or len(artist) > 50:
            raise ValidationError('艺术家名称需在2-50个字符之间')
        return artist

# 用户注册表单
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='电子邮件', help_text='请输入有效的电子邮件地址。')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # 注册字段
        help_texts = {
            'username': '必须是 150 个字符或更少。只能包含字母、数字和 @/./+/-/_ 等字符。',
            'email': '请输入有效的电子邮件地址。',
            'password1': '您的密码至少需要 8 个字符，并不能与其它个人信息过于相似。',
            'password2': '请再次输入密码以确认。',
        }
        error_messages = {
            'username': {
                'required': '用户名是必填字段。',
                'max_length': '用户名长度不能超过 150 个字符。',
                'invalid': '用户名只能包含字母、数字和 @/./+/-/_ 字符。',
            },
            'email': {
                'required': '电子邮件是必填字段。',
                'invalid': '请输入有效的电子邮件地址。',
            },
            'password1': {
                'required': '密码是必填字段。',
                'too_short': '密码长度至少为 8 个字符。',
            },
            'password2': {
                'required': '确认密码是必填字段。',
                'password_mismatch': '两次输入的密码不匹配。',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该电子邮件地址已被注册。")
        return email

# 个人资料表单
class ProfileForm(forms.ModelForm):
    """个人资料编辑表单"""
    email = forms.EmailField(
        label='邮箱',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text='用于接收系统通知和找回密码'
    )
    
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'avatar', 'location', 'website']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nickname': '昵称',
            'bio': '个人简介',
            'avatar': '头像',
            'location': '所在地',
            'website': '个人网站'
        }
        help_texts = {
            'nickname': '显示在您的个人主页和评论中的名称',
            'bio': '简单介绍一下自己吧，不超过500字',
            'location': '您所在的城市或地区，例如：北京、上海',
            'website': '请输入完整网址，包括http://或https://'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # 验证文件类型
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("仅支持JPG/PNG格式")
            # 验证文件大小
            if avatar.size > 2*1024*1024:  # 2MB
                raise forms.ValidationError("文件大小超过2MB限制")
        return avatar

# 评论表单
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # 评论内容字段