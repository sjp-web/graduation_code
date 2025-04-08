# 音乐播放器项目

## 项目简介

这是一个基于 Django 和 Vue.js 的音乐播放器项目，提供完整的音乐管理、播放、下载和用户互动功能。项目采用前后端分离架构，后端使用 Django 提供 RESTful API，前端使用 Vue.js 构建现代化的用户界面。

### 主要特性

- 🎵 音乐管理：上传、播放、下载和管理音乐文件
- 👥 用户系统：注册、登录、个人资料管理
- 💬 社交功能：音乐评论、点赞和互动
- 🔍 智能搜索：多维度音乐搜索和过滤
- 🎨 现代化界面：响应式设计，支持多设备
- 🤖 AI助手：智能问答和FAQ系统
- 📊 管理后台：完善的内容管理和数据统计

### 技术栈

- **后端**：
  - Django 4.2+
  - MySQL 数据库
  - Django REST framework
  - Django Jazzmin（美化管理界面）
  
- **前端**：
  - Vue.js 3
  - 原生CSS3
  - Vite 构建工具
  - 虚拟滚动和懒加载优化

## 快速开始

### 首次安装

1. 克隆项目：
```bash
git clone https://github.com/sjp-web/graduation_code.git
cd graduation_code
```

2. 环境准备：
```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
npm install
```

3. 配置项目：
```bash
# 复制环境配置
cp .env.example .env
# 编辑.env文件，设置数据库等配置

# 初始化数据库
python manage.py migrate
python manage.py createsuperuser
python init_project.py
```

4. 启动服务：
```bash
python manage.py runserver
```

### 数据恢复

如果你之前使用过该项目，需要恢复数据，请参考[数据恢复指南](#数据恢复指南)。

## 项目结构

```
music_website/                # Django项目配置
├── music/                   # 主应用
│   ├── models.py           # 数据模型
│   ├── views/              # 视图函数
│   │   ├── music_views.py  # 音乐相关视图
│   │   ├── user_views.py   # 用户相关视图
│   │   └── search_views.py # 搜索相关视图
│   ├── static/             # 静态资源
│   │   ├── js/             # JavaScript文件
│   │   │   ├── components/ # Vue组件
│   │   │   └── pages/      # 页面组件
│   │   └── css/            # 样式文件
│   └── templates/          # 模板文件
├── media/                   # 用户上传文件
└── staticfiles/            # 开发静态文件
```

## 功能模块

### 1. 用户系统
- 用户注册和登录
- 个人资料管理
- 权限控制

### 2. 音乐管理
- 音乐上传和存储
- 音乐播放器
- 音乐分类管理
- 播放历史记录

### 3. 社交功能
- 音乐评论
- 点赞系统
- 用户互动

### 4. 搜索系统
- 音乐搜索
- 高级筛选
- 结果排序

### 5. 管理后台
- 内容管理
- 用户管理
- 数据统计

## 开发指南

### 后端开发
- 使用 Django REST framework 开发 API
- 遵循 RESTful 设计规范
- 使用 Django ORM 进行数据库操作

### 前端开发
- 使用 Vue.js 3 开发组件
- 采用组件化设计
- 使用 Vite 进行构建

## 部署说明

### 服务器要求
- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Nginx

### 部署步骤
1. 服务器环境配置
2. 应用部署
3. Nginx 配置
4. 服务启动

## 常见问题

### 1. 数据库问题
- 连接错误
- 迁移失败
- 数据备份恢复

### 2. 静态文件问题
- 文件不显示
- 路径错误
- 权限问题

### 3. 上传问题
- 文件大小限制
- 格式不支持
- 存储空间不足

## 数据恢复指南

如果你需要恢复之前的数据，请按以下步骤操作：

1. 备份数据：
```bash
# 数据库备份
mysqldump -u shengjieping -p music_website > music_website_backup.sql

# 备份媒体文件
# 复制 media 目录到安全位置

# 备份环境配置
# 复制 .env 文件到安全位置
```

2. 恢复数据：
```bash
# 恢复数据库
mysql -u shengjieping -p
source D:\music\Backup\music_website_backup.sql

# 恢复媒体文件
# 将备份的 media 目录复制到项目根目录

# 恢复环境配置
# 将备份的 .env 文件复制到项目根目录
```

3. 更新项目：
```bash
# 安装依赖
pip install -r requirements.txt
npm install

# 收集静态文件
python manage.py collectstatic

# 运行迁移
python manage.py migrate
```

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 MIT 许可证。 