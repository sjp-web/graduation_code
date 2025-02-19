from django import forms
from .models import Music
from .models import Profile
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# 音乐上传表单
class MusicForm(forms.ModelForm):
    # 添加显式字段定义
    title = forms.CharField(
        label='歌曲标题',
        widget=forms.TextInput(attrs={'placeholder': '请输入歌曲标题'})
    )
    artist = forms.CharField(
        label='艺术家',
        widget=forms.TextInput(attrs={'placeholder': '请输入艺术家名称'})
    )
    
    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'release_date', 'audio_file', 'lyrics', 'cover_image']
        labels = {
            'album': '专辑名称',
            'release_date': '发行日期',
            'audio_file': '音频文件',
            'lyrics': '歌词',
            'cover_image': '专辑封面'
        }
        widgets = {
            'audio_file': forms.FileInput(attrs={
                'accept': '.mp3,.wav,.aac',
                'class': 'form-control form-control-lg'
            }),
            'album': forms.TextInput(attrs={'placeholder': '专辑名称'}),
            'release_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'YYYY-MM-DD'
                }
            ),
            'lyrics': forms.Textarea(attrs={'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control form-control-lg'})
        }

    def clean_audio_file(self):
        # 验证音频文件大小和类型
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            # 文件大小验证（最大20MB）
            if audio_file.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError('文件大小不能超过20MB')
            
            # 文件类型验证
            if audio_file.content_type not in settings.ALLOWED_AUDIO_TYPES:
                raise ValidationError('只支持MP3、WAV和AAC格式')
                
        return audio_file

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
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']  # 头像和个人简介字段
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'avatar': '支持格式：JPG/PNG，最大2MB',
            'bio': '简短的个人介绍（最多500字）',
        }
    
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