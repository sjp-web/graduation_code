from django import forms
from .models import Music
from .models import Profile
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

# 创建音乐上传表单
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'release_date', 'audio_file']  # 包括文件字段

# 创建用户注册表单
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='电子邮件', help_text='请输入有效的电子邮件地址。')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
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

# 用户个人信息编辑表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
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
            if avatar.size > 2*1024*1024:  # 2MB限制
                raise forms.ValidationError("文件大小超过2MB限制")
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("仅支持JPG/PNG格式")
        return avatar

# 定义评论表单
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']