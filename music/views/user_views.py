from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from ..models import Music, Profile
from ..forms import UserRegistrationForm, ProfileForm
from ..utils.file_handlers.image_handlers import optimize_upload
from uuid import uuid4
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from music.models import ChatMessage

# 用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'music/register.html', {'form': form})

# 用户登录视图
def login_view(request):
    form = AuthenticationForm()  # 初始化空表单
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('music_list')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'music/login.html', {'form': form})  # 确保传递表单

# 个人资料查看视图
@login_required
def profile_view(request):
    user_profile = request.user.profile
    # 修改用户歌曲查询部分
    user_songs = Music.objects.filter(uploaded_by=request.user).order_by('-release_date')
    paginator = Paginator(user_songs, 10)  # 每页10条
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # 添加头像处理逻辑
            if 'avatar' in request.FILES:
                optimized = optimize_upload(request.FILES['avatar'], max_size=(500, 500))
                if optimized:
                    user_profile.avatar.save(
                        f"{uuid4()}.jpg", 
                        ContentFile(optimized.getvalue()),
                        save=False
                    )
            form.save()
            messages.success(request, '个人资料已更新！')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'music/profile.html', {
        'form': form,
        'user_profile': user_profile,
        'user_songs': user_songs,  # 添加用户上传歌曲到上下文
        'page_obj': page_obj
    })

# 用户创建或编辑个人资料视图
@login_required
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # 不立即保存到数据库
            profile.user = request.user  # 关联当前用户
            profile.save()  # 保存到数据库
            return redirect('profile')  # 成功后重定向到个人资料页面
    else:
        form = ProfileForm()  # GET 请求时，准备空表单

    return render(request, 'music/create_profile.html', {'form': form})  # 渲染表单页面

def custom_logout(request):
    # 如果有自定义注销逻辑可能会覆盖设置
    pass

@login_required
@csrf_exempt
@require_POST
def chat_with_ai(request):
    """简单的AI聊天机器人API"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': '消息不能为空'}, status=400)
        
        # 基于关键词的简单回复逻辑
        response = generate_ai_response(user_message)
        
        # 保存对话记录
        ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=response
        )
        
        return JsonResponse({
            'response': response,
            'success': True
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_ai_response(message):
    """根据用户消息生成AI回复"""
    message = message.lower()
    
    # 音乐相关问题
    if '推荐' in message and ('歌' in message or '音乐' in message):
        return '我推荐你听一些流行音乐，比如周杰伦的《晴天》或者Taylor Swift的新专辑。'
    
    elif '怎么上传' in message or '如何上传' in message:
        return '在网站顶部导航栏找到"上传音乐"按钮，点击后填写歌曲信息并上传音频文件即可。'
    
    elif '下载' in message and ('歌' in message or '音乐' in message):
        return '在歌曲详情页面，登录后可以看到下载按钮。点击即可下载音乐。'
    
    # 网站相关问题
    elif '网站' in message and '介绍' in message:
        return '这是一个音乐分享平台，你可以上传、分享和下载音乐作品，还可以与其他音乐爱好者互动。'
    
    elif '账号' in message or '注册' in message:
        return '点击网站右上角的"注册"按钮，填写用户名、邮箱和密码即可创建账号。'
    
    # 默认回复
    else:
        return '抱歉，我无法理解您的问题。您可以询问关于音乐上传、下载、账号注册等问题，我会尽力回答。' 