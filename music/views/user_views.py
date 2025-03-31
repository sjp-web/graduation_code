from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from ..models import Music, Profile, Comment
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
            return redirect('user_center')  # 改为重定向到用户中心，不需要额外参数
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

# 用户中心视图
@login_required
def user_center(request):
    user_profile = request.user.profile
    
    # 处理不同的表单提交
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        # 个人资料表单
        if form_type == 'profile_form':
            profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                # 添加头像处理逻辑
                if 'avatar' in request.FILES:
                    optimized = optimize_upload(request.FILES['avatar'], max_size=(500, 500))
                    if optimized:
                        user_profile.avatar.save(
                            f"{uuid4()}.jpg", 
                            ContentFile(optimized.getvalue()),
                            save=False
                        )
                
                # 保存个人资料
                profile_form.save()
                
                # 更新关联用户的邮箱
                if 'email' in profile_form.cleaned_data:
                    request.user.email = profile_form.cleaned_data['email']
                    request.user.save()
                
                messages.success(request, '个人资料已更新！')
                return redirect('user_center')
        
        # 密码修改表单
        elif form_type == 'password_form':
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if not request.user.check_password(current_password):
                messages.error(request, '当前密码不正确')
            elif new_password1 != new_password2:
                messages.error(request, '两次输入的新密码不一致')
            elif len(new_password1) < 8:
                messages.error(request, '密码必须包含至少8个字符')
            else:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)  # 保持用户登录状态
                messages.success(request, '密码已成功修改')
                return redirect('user_center')
        
        # 登出所有设备
        elif form_type == 'logout_all':
            # 更改用户的密码哈希部分，使所有会话无效
            request.user.set_unusable_password()
            request.user.set_password(request.user.password)  # 重新设置为相同密码，但会生成新哈希
            request.user.save()
            update_session_auth_hash(request, request.user)  # 保持当前会话
            messages.success(request, '已成功登出所有其他设备')
            return redirect('user_center')
    
    # 初始化表单
    profile_form = ProfileForm(instance=user_profile)
    
    # 获取用户音乐并分页
    user_songs = Music.objects.filter(uploaded_by=request.user).order_by('-release_date')
    music_paginator = Paginator(user_songs, 10)  # 每页10条
    music_page_number = request.GET.get('music_page')
    music_page_obj = music_paginator.get_page(music_page_number)
    
    # 获取用户评论并分页
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    comments_paginator = Paginator(user_comments, 10)  # 每页10条
    comments_page_number = request.GET.get('comments_page')
    comments_page_obj = comments_paginator.get_page(comments_page_number)
    
    context = {
        'profile_form': profile_form,
        'user_profile': user_profile,
        'user_songs': music_page_obj,
        'user_comments': comments_page_obj,
        'music_page_obj': music_page_obj,
        'comments_page_obj': comments_page_obj,
    }
    
    return render(request, 'music/user_center.html', context)

# 个人资料查看视图 - 保留旧视图但重定向到新视图
@login_required
def profile_view(request):
    return redirect('user_center')

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

# 编辑个人资料视图 - 重定向到用户中心
@login_required
def edit_profile(request):
    """编辑个人资料"""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # 保存个人资料
            profile = form.save()
            
            # 更新用户邮箱
            user = profile.user
            user.email = form.cleaned_data['email']
            user.save()
            
            messages.success(request, '个人资料已更新。')
            return redirect('user_center')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'music/edit_profile.html', {
        'form': form,
        'profile': profile
    })

def custom_logout(request):
    # 如果有自定义注销逻辑可能会覆盖设置
    pass

# 用户注销视图
@require_POST  # 确保只接受POST请求
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, '您已成功注销')
    return redirect('login')

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
        
        # 获取用户历史对话进行上下文处理
        user_history = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]
        context = [(msg.message, msg.response) for msg in user_history]
        
        # 基于关键词、历史对话和上下文的智能回复逻辑
        response = generate_ai_response(user_message, context, request.user)
        
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

def generate_ai_response(message, context=None, user=None):
    """根据用户消息生成AI回复
    
    Args:
        message: 用户消息
        context: 历史对话记录
        user: 用户对象，用于个性化回复
    """
    message = message.lower()
    
    # 首先尝试匹配数据库中的FAQ
    faq_response = get_db_faq_response(message)
    if faq_response:
        return faq_response
    
    # 其次尝试匹配静态知识库FAQ
    static_faq_response = get_static_faq_response(message)
    if static_faq_response:
        return static_faq_response
    
    # 音乐推荐相关问题 - 增强版
    if any(keyword in message for keyword in ['推荐', '好听', '喜欢']) and any(keyword in message for keyword in ['歌', '音乐', '专辑']):
        # 从用户历史播放记录获取喜好
        if user:
            try:
                # 获取用户最近播放的音乐类型
                from ..models import PlayHistory
                user_play_history = PlayHistory.objects.filter(user=user).order_by('-played_at')[:10]
                if user_play_history.exists():
                    # 分析用户播放偏好
                    categories = {}
                    for history in user_play_history:
                        cat = history.music.category
                        categories[cat] = categories.get(cat, 0) + 1
                    
                    # 找出最常听的类型
                    fav_category = max(categories.items(), key=lambda x: x[1])[0]
                    if fav_category == 'pop':
                        return '根据您的听歌习惯，我推荐您听一些流行音乐，比如周杰伦的《晴天》或邓紫棋的《光年之外》。'
                    elif fav_category == 'rock':
                        return '您似乎喜欢摇滚音乐，推荐Beyond的《海阔天空》或Linkin Park的经典专辑。'
                    elif fav_category == 'classical':
                        return '您偏爱古典音乐，推荐贝多芬的《月光奏鸣曲》或莫扎特的钢琴协奏曲。'
            except Exception:
                pass
        
        # 默认推荐
        return '我推荐您听一些流行音乐，比如周杰伦的《晴天》或者Taylor Swift的新专辑《Midnights》。如果您登录并播放一些歌曲，下次我可以根据您的喜好给出更精准的推荐。'
    
    # 上传音乐相关问题 - 详细说明
    elif any(keyword in message for keyword in ['怎么上传', '如何上传', '上传音乐']):
        return '上传音乐的详细步骤：\n1. 登录您的账号\n2. 点击网站顶部导航栏的"上传音乐"按钮\n3. 填写歌曲标题、艺术家、专辑等信息\n4. 上传音频文件（支持MP3、WAV格式）\n5. 可选择上传歌曲封面\n6. 点击"提交"按钮完成上传\n\n注意：上传的音乐需符合版权要求。'
    
    # 下载音乐相关问题 - 详细说明
    elif any(keyword in message for keyword in ['下载', '保存']) and any(keyword in message for keyword in ['歌', '音乐', '歌曲']):
        return '下载音乐的步骤：\n1. 找到您想下载的歌曲\n2. 点击进入歌曲详情页\n3. 登录您的账号（如果尚未登录）\n4. 点击页面上的"下载"按钮\n5. 文件将自动下载到您的设备\n\n每次下载会记录在您的下载历史中，可在个人中心查看。'
    
    # 账号相关问题 - 增强版
    elif any(keyword in message for keyword in ['账号', '注册', '登录', '密码']):
        if '忘记密码' in message or '重置密码' in message:
            return '如果您忘记了密码，请点击登录页面的"忘记密码"链接，输入您的注册邮箱，我们会发送密码重置链接到您的邮箱。'
        elif '注册' in message:
            return '注册新账号的步骤：\n1. 点击网站右上角的"注册"按钮\n2. 填写用户名、有效邮箱和安全密码\n3. 点击"注册"按钮\n4. 完成邮箱验证（如有）\n5. 登录并完善您的个人资料'
        elif '登录' in message:
            return '登录步骤：\n1. 点击网站右上角的"登录"按钮\n2. 输入您的用户名或邮箱和密码\n3. 点击"登录"按钮\n\n如遇登录问题，可尝试重置密码或联系网站管理员。'
        else:
            return '您可以通过点击网站右上角的"注册"按钮创建新账号。如果已有账号，点击"登录"按钮进行登录。账号信息可在个人中心进行管理和更新。'
    
    # 用户中心相关问题
    elif any(keyword in message for keyword in ['个人中心', '用户中心', '个人资料', '我的信息']):
        return '登录后，您可以点击右上角的用户名进入个人中心。在个人中心可以：\n1. 查看和编辑个人资料\n2. 管理您上传的音乐\n3. 查看播放历史和下载记录\n4. 修改账号设置和密码\n5. 查看您的评论和互动'
    
    # 功能查询相关问题
    elif any(keyword in message for keyword in ['功能', '可以做什么', '怎么用']):
        return '本网站主要功能包括：\n1. 浏览和搜索音乐\n2. 上传和分享您的音乐作品\n3. 在线播放和下载音乐\n4. 评论和点赞喜欢的音乐\n5. 个人用户中心管理\n6. 音乐推荐和发现\n\n如需详细了解某项功能，可以直接询问。'
    
    # 分析上下文，找出相关问题的回答
    if context:
        for prev_q, prev_a in context:
            # 如果当前问题和历史问题相似度高
            if calculate_similarity(message, prev_q) > 0.7:
                return prev_a
    
    # 网站相关问题
    elif '网站' in message and ('介绍' in message or '关于' in message or '是什么' in message):
        return '这是一个音乐分享平台，您可以上传、分享和下载音乐作品，发现新的音乐，还可以与其他音乐爱好者互动。支持多种音乐格式，提供个性化推荐，让您发现更多喜爱的音乐。'
    
    # 记录未解决的问题
    if user:
        try:
            from ..models import UnknownQuery
            UnknownQuery.objects.create(
                query=message,
                user=user
            )
        except Exception:
            pass
    
    # 默认回复
    return '抱歉，我目前无法理解您的问题。您可以询问关于音乐上传、下载、账号注册、网站功能等问题，我会尽力回答。如果您想了解更多功能，可以输入"网站功能"。'

def get_db_faq_response(message):
    """从数据库FAQ知识库中查找匹配的回答"""
    try:
        from ..models import FAQEntry
        
        # 1. 尝试精确匹配
        exact_matches = FAQEntry.objects.filter(
            question__icontains=message, 
            is_active=True
        )
        if exact_matches.exists():
            return exact_matches.first().answer
        
        # 2. 关键词匹配
        keyword_matches = []
        for faq in FAQEntry.objects.filter(is_active=True):
            # 如果有关键词字段，检查关键词匹配
            if faq.keywords:
                keywords = [k.strip().lower() for k in faq.keywords.split(',')]
                if any(keyword in message.lower() for keyword in keywords):
                    keyword_matches.append(faq)
        
        if keyword_matches:
            return keyword_matches[0].answer
        
        # 3. 相似度匹配
        best_match = None
        highest_similarity = 0.7  # 相似度阈值
        
        for faq in FAQEntry.objects.filter(is_active=True):
            similarity = calculate_similarity(message, faq.question)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = faq
        
        if best_match:
            return best_match.answer
            
    except Exception:
        pass
        
    return None

def get_static_faq_response(message):
    """从静态FAQ知识库中查找匹配的回答"""
    # 常见问题及回答
    faqs = {
        '网站是做什么的': '这是一个音乐分享网站，您可以在这里发现、分享和欣赏各种音乐作品。',
        '如何联系管理员': '您可以通过页面底部的"联系我们"发送邮件，或在社交媒体上关注我们。',
        '支持哪些音乐格式': '目前支持MP3、WAV和FLAC格式的音乐文件上传和播放。',
        '音乐上传有大小限制吗': '是的，单个音乐文件上传限制为20MB。如有特殊需求，请联系管理员。',
        '如何修改个人资料': '登录后，点击右上角您的用户名，选择"个人中心"，然后点击"编辑资料"按钮进行修改。',
        '忘记密码怎么办': '在登录页面点击"忘记密码"，输入您的注册邮箱，按照邮件中的指引重置密码。',
        '如何删除我上传的音乐': '在您的个人中心可以查看您上传的所有音乐，点击对应音乐旁的"删除"按钮即可删除。',
        '网站收费吗': '本网站基础功能完全免费。我们提供部分高级功能可能需要付费订阅。',
        '如何举报不良内容': '在有问题的内容页面点击"举报"按钮，填写举报原因提交即可。',
        '是否有音乐推荐': '是的，我们会根据您的听歌历史和喜好，在首页为您推荐可能感兴趣的音乐。'
    }
    
    # 简单的FAQ匹配
    for q, a in faqs.items():
        if calculate_similarity(message, q) > 0.8:
            return a
            
    # 关键词匹配
    keywords = {
        '费用': '本网站基础功能完全免费。我们提供部分高级功能可能需要付费订阅。',
        '版权': '用户上传的音乐应确保拥有版权或相应许可。违反版权的内容将被移除。',
        '隐私': '我们重视用户隐私保护，详情请查看网站底部的"隐私政策"链接。',
        '客服': '如需帮助，请通过页面底部的"联系我们"发送邮件，我们会尽快回复。'
    }
    
    for k, v in keywords.items():
        if k in message:
            return v
    
    return None

def calculate_similarity(text1, text2):
    """计算两段文本的相似度，返回0-1之间的值"""
    # 简单实现，生产环境可以使用更复杂的NLP方法
    text1 = set(text1.lower().split())
    text2 = set(text2.lower().split())
    
    # 使用Jaccard相似度
    if not text1 or not text2:
        return 0
    
    intersection = len(text1.intersection(text2))
    union = len(text1.union(text2))
    
    return intersection / union if union > 0 else 0 