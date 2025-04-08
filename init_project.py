#!/usr/bin/env python
"""
项目初始化脚本
整合了默认头像生成和FAQ数据创建功能
"""
import os
import django
from PIL import Image, ImageDraw

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
django.setup()

from django.db import transaction
from music.models import FAQEntry

def generate_default_avatar():
    """生成一个简单的灰色用户头像"""
    print("开始生成默认头像...")
    
    # 确保目录存在
    os.makedirs('music/static/images/avatars', exist_ok=True)
    os.makedirs('media/avatars', exist_ok=True)
    
    # 创建一个200x200的图片，背景色为灰色
    image = Image.new('RGB', (200, 200), color=(200, 200, 200))
    draw = ImageDraw.Draw(image)
    
    # 画一个深灰色圆形作为头部
    draw.ellipse((50, 30, 150, 130), fill=(150, 150, 150))
    
    # 画一个深灰色矩形作为身体
    draw.rectangle((75, 120, 125, 180), fill=(150, 150, 150))
    
    # 保存图片到静态目录
    image.save('music/static/images/avatars/default.png')
    # 同时保存一份到media目录
    image.save('media/avatars/default.png')
    
    print("✓ 默认头像已生成并保存到以下位置:")
    print("  - music/static/images/avatars/default.png")
    print("  - media/avatars/default.png")

@transaction.atomic
def create_default_faqs():
    """创建默认的FAQ内容"""
    print("开始创建默认FAQ数据...")
    
    # 检查是否已有FAQ数据
    if FAQEntry.objects.exists():
        print("✓ FAQ数据已存在，跳过创建。")
        return
    
    # 音乐相关问题
    music_faqs = [
        {
            'question': '如何搜索音乐',
            'answer': '您可以通过以下方式搜索音乐：\n1. 使用网站顶部的搜索栏输入关键词\n2. 根据分类浏览音乐\n3. 查看推荐列表\n搜索支持按歌名、艺术家、专辑名称等进行匹配。',
            'keywords': '搜索,查找,寻找,歌曲,音乐',
            'category': 'music'
        },
        {
            'question': '如何播放音乐',
            'answer': '点击任何音乐项目后，您将被带到音乐详情页面，在那里您可以点击播放按钮开始播放。我们的播放器支持播放/暂停、音量调节、进度控制等功能。',
            'keywords': '播放,听歌,音乐播放器',
            'category': 'music'
        },
        {
            'question': '支持哪些音乐格式',
            'answer': '我们的网站目前支持上传和播放以下格式的音乐文件：\n- MP3（最常用）\n- WAV（无损音质）\n- FLAC（无损压缩）\n- OGG\n上传时请确保文件大小不超过20MB。',
            'keywords': '格式,mp3,wav,flac,支持格式',
            'category': 'music'
        },
    ]
    
    # 账号相关问题
    account_faqs = [
        {
            'question': '如何修改密码',
            'answer': '修改密码的步骤：\n1. 登录您的账号\n2. 点击右上角您的用户名\n3. 选择"个人中心"\n4. 点击"账号安全"选项\n5. 选择"修改密码"\n6. 输入当前密码和新密码\n7. 点击"保存"按钮',
            'keywords': '密码,修改密码,更改密码,账号安全',
            'category': 'account'
        },
        {
            'question': '如何更新个人资料',
            'answer': '更新个人资料的步骤：\n1. 登录您的账号\n2. 点击右上角您的用户名\n3. 选择"个人中心"\n4. 点击"编辑资料"按钮\n5. 更新您的个人信息（昵称、头像、个人简介等）\n6. 点击"保存更改"按钮',
            'keywords': '更新资料,修改资料,个人信息,编辑资料',
            'category': 'account'
        },
    ]
    
    # 网站功能问题
    website_faqs = [
        {
            'question': '网站支持手机访问吗',
            'answer': '是的，我们的网站采用响应式设计，支持在手机、平板和电脑等各种设备上访问。网站会自动适应您的屏幕大小，提供最佳的浏览体验。',
            'keywords': '手机,移动设备,响应式,适配',
            'category': 'website'
        },
        {
            'question': '如何举报不良内容',
            'answer': '如果您发现违规或不良内容，可以通过以下步骤举报：\n1. 在有问题的内容页面点击"举报"按钮\n2. 选择举报原因（侵权、违规、垃圾内容等）\n3. 可选填写额外说明\n4. 提交举报\n\n我们的管理团队将尽快审核并处理您的举报。',
            'keywords': '举报,不良内容,违规,投诉',
            'category': 'website'
        },
    ]
    
    # 合并所有FAQ并创建
    all_faqs = music_faqs + account_faqs + website_faqs
    
    # 创建FAQ条目
    for faq in all_faqs:
        FAQEntry.objects.create(
            question=faq['question'],
            answer=faq['answer'],
            keywords=faq['keywords'],
            category=faq['category'],
            is_active=True
        )
    
    print(f"✓ 成功创建了 {len(all_faqs)} 条FAQ数据。")

def init_directories():
    """初始化项目所需的目录结构"""
    print("创建必要的目录结构...")
    
    # 确保这些目录存在
    directories = [
        'media/covers',
        'media/music',
        'media/avatars',
        'staticfiles/dist',
        'staticfiles/images',
        'logs',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  - 创建目录: {directory}")
    
    print("✓ 所有必要目录已创建")

def init_project():
    """执行所有初始化任务"""
    print("\n" + "="*50)
    print("      音乐网站项目初始化")
    print("="*50 + "\n")
    
    # 1. 创建必要的目录结构
    init_directories()
    
    # 2. 生成默认头像
    generate_default_avatar()
    
    # 3. 创建默认FAQ数据
    create_default_faqs()
    
    print("\n初始化完成！您现在可以运行项目了。")
    print("="*50)

if __name__ == "__main__":
    init_project() 