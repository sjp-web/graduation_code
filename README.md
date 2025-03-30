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
- 数据分析与统计功能

## 技术栈

- Django 4.2+
- MySQL 数据库
- Django Jazzmin (美化Admin界面)
- Pillow (图像处理)
- django-resized (图片尺寸优化)
- django-admin-rangefilter (日期范围过滤)
- django-import-export (数据导入导出)

## 详细安装指南 (适合初学者)

### 1. 安装必要的软件

首先，确保您已经安装了以下软件：

- [Python 3.8+](https://www.python.org/downloads/) - 编程语言
- [MySQL](https://dev.mysql.com/downloads/installer/) - 数据库系统
- [Git](https://git-scm.com/downloads) - 版本控制工具

### 2. 获取项目代码

打开命令提示符（Windows）或终端（Mac/Linux），执行以下命令：

```bash
# 克隆项目
git clone https://github.com/sjp-web/graduation_code.git

# 进入项目文件夹
cd graduation_code
```

### 3. 创建虚拟环境

虚拟环境是一个独立的Python环境，可以避免项目之间的依赖冲突。

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Mac/Linux）
# source venv/bin/activate
```

成功激活后，命令行前面会出现`(venv)`标识。

### 4. 安装项目依赖

```bash
# 安装所有需要的库
pip install -r requirements.txt
```

### 5. 配置环境变量

将`.env.example`文件复制为`.env`，然后根据您的环境修改其中的配置：

```bash
# Windows
copy .env.example .env

# Mac/Linux
# cp .env.example .env
```

然后用文本编辑器打开`.env`文件，修改数据库配置等信息。

### 6. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE music_website CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

您可以使用MySQL命令行工具或者图形化工具（如MySQL Workbench）来执行此命令。

### 7. 进行数据库迁移

```bash
# 创建数据库表
python manage.py migrate
```

如果您有已有的数据库备份，也可以直接导入：

```bash
# 方法一：使用命令行导入SQL文件
mysql -u 您的用户名 -p music_website < music_backup_.sql

# 方法二：使用图形化工具导入
# 打开MySQL Workbench，连接到您的数据库，然后选择导入SQL文件
```

### 8. 创建管理员账户

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

### 9. 启动开发服务器

```bash
python manage.py runserver
```

现在，打开浏览器，访问 http://127.0.0.1:8000/ 即可看到网站首页。

管理后台地址为 http://127.0.0.1:8000/admin/，使用刚才创建的管理员账户登录。

## 项目结构

- `music/` - 主应用目录
  - `admin.py` - 管理后台配置
  - `forms.py` - 表单定义
  - `models.py` - 数据模型定义
  - `urls.py` - URL路由配置
  - `static/` - 静态文件目录
  - `templates/` - 模板文件目录
  - `templatetags/` - 自定义模板标签
  - `tests/` - 测试目录
  - `utils/` - 工具函数目录
    - `decorators/` - 装饰器工具
    - `file_handlers/` - 文件处理工具
    - `statistics/` - 数据统计工具
    - `security.py` - 安全相关工具
    - `string_utils.py` - 字符串处理工具
    - `http_utils.py` - HTTP工具
  - `views/` - 视图函数目录
    - `admin_views.py` - 管理员视图
    - `music_views.py` - 音乐相关视图
    - `search_views.py` - 搜索相关视图
    - `stats_views.py` - 统计相关视图
    - `user_views.py` - 用户相关视图
- `music_website/` - 项目配置目录
- `media/` - 用户上传的媒体文件存储目录
- `requirements.txt` - 项目依赖列表
- `manage.py` - Django项目管理脚本
- `.env` - 环境配置文件
- `.env.example` - 环境配置示例

## 常见问题解答 (FAQ)

### 1. 我没有安装MySQL，可以使用SQLite吗？

可以。SQLite是一个轻量级数据库，适合开发和测试。修改`.env`文件，将`DB_ENGINE`改为`django.db.backends.sqlite3`，并删除其他数据库相关配置项。

### 2. 运行时遇到"No module named xxx"错误怎么办？

这表示缺少某个Python库。请确保已激活虚拟环境并正确安装了所有依赖：

```bash
pip install -r requirements.txt
```

### 3. 如何修改网站配置？

大部分配置可以在`.env`文件中修改。更高级的配置可以在`music_website/settings.py`中找到。

### 4. 如何重置密码？

如果忘记了管理员密码，可以使用以下命令重置：

```bash
python manage.py changepassword 用户名
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

使用启动脚本：
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
ExecStart=/var/www/music_website/venv/bin/gunicorn --workers=4 --bind=0.0.0.0:8000 music_website.wsgi:application
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

## 数据库备份与恢复

本项目提供了简单的数据库备份和恢复功能，便于在开发和部署过程中管理数据。

### 数据库备份

项目已经包含一个默认的数据库备份文件`music_backup_.sql`，您可以通过以下方式使用它：

```bash
# 使用MySQL命令行工具导入备份
mysql -u 您的用户名 -p music_website < music_backup_.sql

# 或者使用图形化工具如MySQL Workbench导入备份文件
```

### 使用启动脚本

项目包含一个便捷的启动脚本`start.py`，可以自动根据环境变量选择正确的启动方式：

```bash
# 启动应用
python start.py
```

此脚本会：
1. 读取`.env`文件中的`DEBUG`设置
2. 如果`DEBUG=True`，将以Django开发服务器模式启动
3. 如果`DEBUG=False`，将以Gunicorn生产模式启动（会先询问是否收集静态文件）

### 自建备份（开发建议）

在开发过程中，建议定期备份您的数据库：

```bash
# 使用MySQL命令行工具导出数据库
mysqldump -u 您的用户名 -p music_website > 您的备份文件名.sql
```

备份完成后，可以将备份文件保存在安全的位置。当需要恢复数据时，使用上述导入命令即可。

如果您修改了数据库结构，记得先运行迁移命令更新数据库结构：

```bash
python manage.py migrate
```

然后再导入您的数据备份。

## 贡献与反馈

欢迎提交问题报告和功能建议。如有任何问题，请通过以下方式联系：

- 提交Issue到项目仓库
- 发送邮件至[您的邮箱地址] 