# 音乐播放器项目

这是一个基于Django和Vue.js的音乐播放器项目，适用于个人音乐收藏和分享。该项目实现了完整的音乐管理、播放、下载和用户互动功能。

## 目录
1. [功能特点](#功能特点)
2. [技术栈](#技术栈)
3. [安装步骤](#安装步骤)
4. [用户功能](#用户功能)
5. [管理员功能](#管理员功能)
6. [项目结构](#项目结构)
7. [开发指南](#开发指南)
8. [部署指南](#部署指南)
9. [常见问题](#常见问题)

## 功能特点

- 音乐上传、播放、下载和管理
- 用户注册、登录和个人资料管理
- 音乐评论和互动系统
- 音乐搜索和多维度过滤
- 虚拟滚动优化的音乐列表
- 图片懒加载
- 播放历史记录
- AI聊天助手和FAQ系统
- 完善的管理后台
- 响应式设计，支持多设备

## 技术栈

- **后端**：
  - Django 4.2+
  - MySQL数据库
  - Django Jazzmin（美化管理界面）
  - Django Debug Toolbar（开发调试）
  - 自定义中间件和扩展
  
- **前端**：
  - Vue.js 3
  - 原生CSS3
  - 构建工具：Vite
  - 虚拟滚动和懒加载

- **部署**：
  - Whitenoise（静态文件处理）
  - Gunicorn（WSGI服务器）
  - 环境变量配置

## 安装步骤

### 1. 环境准备

- Python 3.8+
- Node.js 14+
- MySQL 5.7+

### 2. 克隆项目

```bash
git clone [项目地址]
cd [项目目录]
```

### 3. 后端设置

```bash
# 创建虚拟环境
python -m venv venv
# Windows激活虚拟环境
venv\Scripts\activate
# Linux/Mac激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建.env文件
cp .env.example .env
# 编辑.env文件，设置数据库等配置

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化项目（创建默认数据）
python init_project.py
```

### 4. 前端设置

```bash
# 安装前端依赖
npm install

# 构建前端资源
npm run build
```

### 5. 启动服务

```bash
# 开发模式启动
python manage.py runserver

# 生产模式启动
python manage.py runserver_production
```

## 用户功能

### 注册与登录

1. 访问首页，点击右上角的"注册"按钮
2. 填写用户名、邮箱和密码
3. 注册成功后，使用用户名和密码登录
4. 登录后可以修改个人资料和头像

### 音乐播放与下载

1. 在首页可以浏览所有音乐
2. 使用搜索框按标题、艺术家或专辑搜索
3. 点击音乐卡片播放音乐
4. 登录后可以下载音乐文件
5. 播放器支持常见控制：暂停、继续、上一首、下一首、音量调节

### 评论与互动

1. 在音乐详情页可以查看和发表评论
2. 可以对喜欢的音乐进行点赞
3. 系统会记录您的播放历史

### AI助手和FAQ

1. 点击导航栏中的"帮助"访问FAQ页面
2. 使用AI聊天助手询问问题，获取即时回答

## 管理员功能

### 后台管理入口

1. 访问 `/admin` 路径登录管理后台
2. 使用超级用户账号登录

### 内容管理

1. **音乐管理**：上传、编辑和删除音乐
2. **用户管理**：查看和管理用户账号
3. **评论管理**：审核和管理用户评论
4. **FAQ管理**：添加和更新常见问题
5. **系统日志**：查看系统操作日志

### 数据统计

1. 查看音乐播放和下载统计
2. 查看用户活跃度统计
3. 查看系统资源使用情况

## 项目结构

### 目录结构

```
music_website/           # Django项目配置
music/                   # 主应用
  ├── models.py          # 数据模型
  ├── admin.py           # 管理界面配置
  ├── forms.py           # 表单
  ├── urls.py            # URL路由
  ├── views/             # 视图函数
  │   ├── music_views.py # 音乐相关视图
  │   ├── user_views.py  # 用户相关视图
  │   ├── search_views.py# 搜索相关视图
  │   └── admin_views.py # 管理员相关视图
  ├── utils/             # 工具函数
  ├── middleware/        # 中间件
  ├── static/            # 静态资源
  ├── templates/         # 模板文件
  └── templatetags/      # 自定义模板标签
staticfiles/             # 开发静态文件
  ├── js/                # JavaScript文件
  │   ├── components/    # Vue组件
  │   └── vue-music-list.js  # 入口文件
  ├── css/               # CSS样式
  └── images/            # 图片资源
static_collected/        # 生产环境静态文件
media/                   # 用户上传文件
logs/                    # 日志文件
```

### 核心功能模块

#### 1. 用户系统
- 用户注册和登录
- 用户权限管理
- 用户个人中心
- 用户收藏和播放历史

#### 2. 音乐管理
- 音乐上传（支持MP3、WAV、M4A等格式）
- 音乐播放
- 音乐分类管理
- 音乐评论系统

#### 3. 搜索系统
- 音乐搜索
- 高级筛选
- 搜索结果排序

#### 4. 管理员功能
- 音乐审核
- 用户管理
- 系统设置

### 数据模型说明

#### Music（音乐）
- title: 音乐标题
- artist: 艺术家
- album: 专辑名
- release_date: 发行日期
- cover_image: 封面图片
- audio_file: 音频文件
- category: 音乐分类
- play_count: 播放次数

#### User（用户）
- username: 用户名
- email: 邮箱
- avatar: 头像
- is_staff: 是否为管理员

#### Comment（评论）
- content: 评论内容
- created_at: 评论时间
- user: 评论用户
- music: 评论的音乐

### 前端代码组织结构

前端代码采用了组件化的设计模式，主要使用Vue.js框架。组织结构如下：

```
├── static/js/                  # 静态JavaScript文件目录
│   ├── pages/                 # 页面级组件目录
│   │   ├── music-player-page.js  # 音乐播放页面组件
│   │   ├── search-page.js     # 搜索页面组件
│   │   └── user-center-page.js # 用户中心页面组件
│   ├── components/            # 组件目录
│   │   ├── common/           # 通用组件
│   │   ├── player/           # 播放器相关组件
│   │   └── search/           # 搜索相关组件
│   ├── utils/                 # 工具函数目录
│   └── main.js                # 主JavaScript文件
```

## 开发指南

### 后端开发

- 项目结构采用模块化设计，核心功能在`music`应用中
- 视图函数采用基于类的视图，位于`music/views/`目录
- 工具函数和辅助类位于`music/utils/`目录
- 中间件位于`music/middleware/`目录
- 模板标签在`music/templatetags/`目录

### 前端开发

- 开发模式：`npm run dev`
- 构建生产版本：`npm run build`
- 预览生产版本：`npm run preview`

## 部署指南

### 服务器准备

1. 准备Linux服务器（推荐Ubuntu 20.04+）
2. 安装必要软件：
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv mysql-server nginx
   ```

### 应用部署

1. 克隆代码库到服务器
2. 创建虚拟环境并安装依赖
3. 配置生产环境变量（设置 `DEBUG=False`）
4. 执行数据库迁移
5. 收集静态文件：`python manage.py collectstatic`

### Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/your/project/static_collected/;
        expires 30d;
    }

    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 使用Gunicorn运行

```bash
gunicorn music_website.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 120
```

### Systemd服务配置

创建文件 `/etc/systemd/system/music_website.service`:

```ini
[Unit]
Description=Music Website Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/gunicorn music_website.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 120
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl enable music_website
sudo systemctl start music_website
```

## 常见问题

### 数据库连接问题

- 确保MySQL服务已启动
- 检查数据库用户名和密码是否正确
- 确保数据库名称存在

### 静态文件不显示

- 确保已运行 `python manage.py collectstatic`
- 检查 Nginx 配置中的静态文件路径是否正确
- 检查文件权限是否正确

### 上传文件失败

- 检查 `media` 目录权限是否正确
- 确保文件大小未超过 `MAX_UPLOAD_SIZE` 设置
- 检查磁盘空间是否充足

### 其他问题

如果遇到其他问题，请查看系统日志：
- 应用日志：项目目录下的 `logs/error.log`
- Nginx日志：`/var/log/nginx/error.log`
- Systemd日志：`journalctl -u music_website.service` 