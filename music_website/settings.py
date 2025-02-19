"""
Django settings for music_website project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# 建立基础路径
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&5g^pnyqp4ksfuiyd9ep8qraoh)zpfjdtq1uou*qr!0fvocvpa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',        # Admin app
    'django.contrib.auth',         # Authentication framework
    'django.contrib.contenttypes', # Content types framework
    'django.contrib.sessions',      # Session framework
    'django.contrib.messages',      # Messaging framework
    'django.contrib.staticfiles',   # Static files handling
    'music',                       # Your custom app
]

# 这里添加 LOGIN_URL
LOGIN_URL = '/accounts/login/'  # 设置自定义登录路径

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 如果没有额外的模板路径，保持为空
        'APP_DIRS': True,  # 确保设置为 True，这样 Django 会自动在每个应用程序的 templates 目录中查找模板
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# MEDIA_URL 用于引用到文件的 URL 前缀
MEDIA_URL = '/media/'

# MEDIA_ROOT 是文件存储的根目录，使用 BASE_DIR 作为基础路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'music_website',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',   # 如有必要可替换为你的数据库主机
        'PORT': '3306',        # MySQL 默认端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 简体中文

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True  # 启用国际化

USE_TZ = True

USE_L10N = False  # 禁用本地化格式

DATE_INPUT_FORMATS = ['%Y-%m-%d']  # 明确指定日期格式


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# 静态文件的 URL 配置

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'music/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 文件上传配置
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# 分页设置
PAGE_SIZE = 10

# 允许的文件类型
ALLOWED_AUDIO_TYPES = ['audio/mpeg', 'audio/wav', 'audio/aac']
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB

# 保留必要安全设置
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2周会话有效期

