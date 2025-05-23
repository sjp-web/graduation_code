"""
Django settings for music_website project.

简化版设置文件
使用单一文件管理所有环境设置
通过DEBUG=True/False切换开发/生产环境
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 建立基础路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全设置
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-&5g^pnyqp4ksfuiyd9ep8qraoh)zpfjdtq1uou*qr!0fvocvpa')

# 环境设置: True为开发环境，False为生产环境
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# 允许的主机设置
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# 应用定义
INSTALLED_APPS = [
    'jazzmin',  # 放在最前面
    'rangefilter',  # 添加在jazzmin之后
    'django.contrib.admin',        # Admin app
    'django.contrib.auth',         # Authentication framework
    'django.contrib.contenttypes', # Content types framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static files handling
    'music',                       # 音乐应用
]

# 如果是开发环境，添加debug_toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

# 认证设置
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/login/'

# 中间件设置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'music.middleware.FileExceptionMiddleware',  # 添加我们的文件异常处理中间件
]

# 针对不同环境设置特定中间件
if DEBUG:
    # 开发环境添加调试中间件
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
else:
    # 生产环境添加whitenoise处理静态文件
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'music_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'music_website.wsgi.application'

# 数据库设置
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'music_website'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# 密码验证设置
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化设置
LANGUAGE_CODE = 'zh-hans'  # 简体中文
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False  # 禁用时区支持，解决数据库时区问题
USE_L10N = False  # 禁用本地化格式
DATE_INPUT_FORMATS = ['%Y-%m-%d']  # 明确指定日期格式

# 静态文件设置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

# 媒体文件设置
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT', 'media'))

# 默认主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 文件上传配置
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# 分页设置
PAGE_SIZE = 10

# 允许的文件类型
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 20 * 1024 * 1024))  # 默认20MB
ALLOWED_AUDIO_TYPES = ['audio/mpeg', 'audio/wav', 'audio/aac', 'audio/mp4', 'audio/x-m4a', 'video/mp4', 'audio/x-hx-aac-adts', 'application/octet-stream']

# 安全设置
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 两周

# 根据环境配置日志
# 确保日志文件目录存在
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOG_FILE', os.path.join(LOG_DIR, 'error.log')),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console' if DEBUG else 'file'],
            'level': 'INFO' if DEBUG else 'ERROR',
            'propagate': True,
        },
        'music': {
            'handlers': ['console' if DEBUG else 'file'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
    },
}

# 邮件设置 - 根据环境使用不同配置
if DEBUG:
    # 开发环境使用控制台输出
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # 生产环境使用SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'noreply@example.com')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Music Website <noreply@example.com>')

# 调试工具栏配置 - 只在开发环境使用
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']

# 在文件末尾添加
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# 添加会话安全设置
SESSION_COOKIE_SECURE = False  # 开发时设为False，生产环境应设为True
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Jazzmin配置
JAZZMIN_SETTINGS = {
    # 基本设置
    "site_title": "音乐网站管理",
    "site_header": "音乐网站管理系统",
    "site_brand": "音乐网站",
    "welcome_sign": "欢迎访问音乐网站管理后台",
    "copyright": "音乐分享与管理平台 - 毕业设计作品",
    
    # UI设置
    "changeform_format": "horizontal_tabs",
    "topmenu_links": [
        {"name": "主页", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "回到网站", "url": "/", "new_window": True},
    ],
    
    # 图标设置
    "hide_apps": [],  # 确保没有隐藏应用
    "navigation_expanded": True,
    "icons": {
        "auth.user": "fas fa-user-cog",
        "auth.Group": "fas fa-users-cog",
        "music.Music": "fas fa-music",
        "music.Comment": "fas fa-comment-dots",
        "music.Profile": "fas fa-id-card",
        "music.AdminLog": "fas fa-clipboard-list",
        "music.MusicDownload": "fas fa-download",
        "music.ChatMessage": "fas fa-comment-alt",
        "admin.LogEntry": "fas fa-history",
        "logs": "fas fa-clipboard-list",
        "dashboard": "fas fa-chart-line",
        "interaction": "fas fa-comments",
        "content": "fas fa-folder-open",
        "user_management": "fas fa-users"
    },
    
    # 模型显示顺序
    "order_with_respect_to": [
        "dashboard",
        "content",
        "interaction", 
        "user_management",
        "auth",
        "logs"
    ],
    
    # 自定义菜单项
    "custom_links": {
        # 添加前台快捷访问区域，放在最上方
        "前台快捷访问": [{
            "name": "网站首页",
            "url": "/",
            "icon": "fas fa-home",
            "new_window": True
        }, {
            "name": "音乐搜索",
            "url": "/search/",
            "icon": "fas fa-search",
            "new_window": True
        }]
    }
}

# 添加MIME类型配置
MIME_TYPES = {
    '.js': 'application/javascript',
}

