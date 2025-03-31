import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
django.setup()

from music.models import FAQEntry
from django.db import transaction


@transaction.atomic
def create_default_faqs():
    """创建默认的FAQ内容"""
    
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
        {
            'question': '歌曲上传失败怎么办',
            'answer': '如果您在上传歌曲时遇到问题，请检查：\n1. 文件格式是否受支持（MP3、WAV、FLAC等）\n2. 文件大小是否超过20MB限制\n3. 网络连接是否稳定\n4. 是否填写了所有必填字段\n\n如果问题仍然存在，请刷新页面重试或联系管理员。',
            'keywords': '上传失败,上传错误,无法上传',
            'category': 'music'
        },
        {
            'question': '如何创建播放列表',
            'answer': '目前我们的网站尚未提供创建自定义播放列表的功能，但这是我们计划在未来版本中添加的功能。敬请期待！',
            'keywords': '播放列表,歌单,创建列表',
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
            'question': '注册时提示用户名已存在',
            'answer': '如果您在注册时收到"用户名已存在"的提示，这意味着该用户名已被其他用户使用。请尝试使用不同的用户名，或者如果您认为这是您之前注册的账号，请使用"忘记密码"功能恢复访问。',
            'keywords': '用户名已存在,注册失败,重复用户名',
            'category': 'account'
        },
        {
            'question': '如何更新个人资料',
            'answer': '更新个人资料的步骤：\n1. 登录您的账号\n2. 点击右上角您的用户名\n3. 选择"个人中心"\n4. 点击"编辑资料"按钮\n5. 更新您的个人信息（昵称、头像、个人简介等）\n6. 点击"保存更改"按钮',
            'keywords': '更新资料,修改资料,个人信息,编辑资料',
            'category': 'account'
        },
        {
            'question': '如何注销账号',
            'answer': '我们目前不提供自助账号注销功能。如果您希望注销账号，请联系网站管理员，并提供您的用户名和注册邮箱进行身份验证。请注意，账号注销后，您的个人数据和上传的内容将被永久删除，且无法恢复。',
            'keywords': '注销账号,删除账号,账号删除,关闭账号',
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
        {
            'question': '网站有没有应用程序',
            'answer': '目前我们尚未提供原生应用程序，但您可以通过手机浏览器访问我们的网站，体验与应用程序类似的功能。我们正在考虑在未来开发专用的移动应用程序，敬请期待！',
            'keywords': '应用,APP,客户端,手机应用',
            'category': 'website'
        },
        {
            'question': '网站如何保护用户隐私',
            'answer': '我们非常重视用户隐私保护。我们采取了以下措施：\n1. 使用HTTPS加密所有通信\n2. 密码安全存储和加密\n3. 不会向第三方分享您的个人信息\n4. 定期安全审计和更新\n\n详细信息请查阅我们的隐私政策。',
            'keywords': '隐私,数据保护,安全,个人信息',
            'category': 'website'
        },
        {
            'question': '网站有哪些未来计划',
            'answer': '我们计划在未来添加更多功能，包括但不限于：\n1. 用户自定义播放列表\n2. 社交分享和互动功能增强\n3. 音乐推荐算法优化\n4. 移动应用程序\n5. 更多音乐格式支持\n\n我们非常欢迎用户提供反馈和建议！',
            'keywords': '未来,计划,功能更新,开发计划',
            'category': 'website'
        },
    ]
    
    # 其他问题
    other_faqs = [
        {
            'question': '如何成为音乐创作者',
            'answer': '任何注册用户都可以上传原创音乐作品。在上传音乐时，可以选择"原创"选项，这样您的作品会被标记为原创内容。我们支持和鼓励原创音乐人在平台上分享作品。',
            'keywords': '创作者,原创,音乐人,创作',
            'category': 'other'
        },
        {
            'question': '如何联系管理员',
            'answer': '您可以通过以下方式联系网站管理员：\n1. 发送邮件至contact@musicwebsite.com\n2. 在网站底部"联系我们"页面填写表单\n3. 通过我们的社交媒体账号发送消息\n\n我们会在1-2个工作日内回复您的询问。',
            'keywords': '联系,管理员,客服,帮助',
            'category': 'other'
        },
    ]
    
    # 合并所有FAQ并创建
    all_faqs = music_faqs + account_faqs + website_faqs + other_faqs
    
    # 检查是否已有FAQ数据
    if FAQEntry.objects.exists():
        print('FAQ数据已存在，跳过创建。')
        return
    
    # 创建FAQ条目
    for faq in all_faqs:
        FAQEntry.objects.create(
            question=faq['question'],
            answer=faq['answer'],
            keywords=faq['keywords'],
            category=faq['category'],
            is_active=True
        )
    
    print(f'成功创建了 {len(all_faqs)} 条FAQ数据。')


if __name__ == '__main__':
    create_default_faqs() 