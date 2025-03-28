# 音乐分享与管理平台

这是一个基于Django开发的音乐分享与管理平台，允许用户上传、分享、下载和评论音乐作品。

## 项目特点

- 用户注册与登录系统
- 个人资料管理（头像、个人简介等）
- 音乐作品上传与管理
- 音乐分类与搜索功能
- 评论系统
- 音乐下载统计
- 后台管理系统（基于Django Admin + Jazzmin美化）
- 数据备份与恢复功能

## 技术栈

- Django 4.2+
- MySQL 数据库
- Django Jazzmin (美化Admin界面)
- Pillow (图像处理)
- django-resized (图片尺寸优化)
- django-admin-rangefilter (日期范围过滤)
- django-import-export (数据导入导出)

## 安装指南

### 1. 克隆项目

```bash
git clone <项目地址>
cd <项目文件夹>
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

在 `music_website/settings.py` 中配置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'music_website',
        'USER': '<数据库用户名>',
        'PASSWORD': '<数据库密码>',
        'HOST': 'localhost',   
        'PORT': '3306',        
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 5. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE music_website CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 数据迁移

```bash
python manage.py migrate
```

### 7. 创建超级用户

```bash
python manage.py createsuperuser
```

### 8. 运行开发服务器

```bash
python manage.py runserver
```

## 项目结构

- `music/` - 主应用目录
  - `models.py` - 数据模型定义
  - `views.py` - 视图函数
  - `forms.py` - 表单定义
  - `admin.py` - 管理后台配置
  - `templates/` - 模板文件
  - `static/` - 静态文件
- `music_website/` - 项目配置目录
- `media/` - 用户上传的媒体文件存储目录
- `backup/` - 数据备份目录
- `backup_data.py` - 数据备份脚本
- `restore_data.py` - 数据恢复脚本

## 备份与恢复

### 备份数据

```bash
python backup_data.py
```

### 恢复数据

```bash
python restore_data.py
```

## 主要功能

1. **音乐管理**：上传、编辑、删除音乐作品
2. **音乐播放**：在线播放音乐
3. **用户管理**：注册、登录、个人资料设置
4. **评论系统**：对音乐作品进行评论
5. **搜索功能**：按标题、艺术家、专辑等搜索音乐
6. **数据统计**：播放量、下载量统计
7. **后台管理**：管理用户、音乐、评论等数据

## 生产环境部署

### 1. 环境配置

项目采用简化的环境配置方式，通过`.env`文件中的`DEBUG`变量来区分开发和生产环境：

```
# 开发环境: DEBUG=True
# 生产环境: DEBUG=False
```

使用环境切换工具：
```bash
# 切换到开发环境
python switch_env.py dev

# 切换到生产环境
python switch_env.py prod
```

或者直接启动服务（会根据当前环境自动选择启动方式）：
```bash
python start.py
```

### 2. 静态文件收集

生产环境下需要收集静态文件：
```bash
python manage.py collectstatic
```

### 3. 使用Gunicorn部署

安装Gunicorn:
```bash
pip install gunicorn
```

启动服务:
```bash
gunicorn --workers=4 --bind=0.0.0.0:8000 music_website.wsgi:application
```

也可以直接使用简化的启动脚本：
```bash
python start.py
```

### 4. Nginx配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 重定向到HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL优化设置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_session_cache shared:SSL:10m;

    # 静态文件
    location /static/ {
        alias /var/www/yourdomain.com/static/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # 媒体文件
    location /media/ {
        alias /var/www/yourdomain.com/media/;
        expires 7d;
    }

    # 代理到Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Systemd服务配置

创建文件 `/etc/systemd/system/music_website.service`:

```ini
[Unit]
Description=Gunicorn daemon for Music Website
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/music_website
ExecStart=/var/www/music_website/.venv/bin/gunicorn --workers=4 --bind=0.0.0.0:8000 music_website.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl enable music_website
sudo systemctl start music_website
```

## 开发者

- 原始开发者：[开发者姓名]

## 许可证

该项目采用 [许可证类型] 许可证 