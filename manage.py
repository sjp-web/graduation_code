#!/usr/bin/env python
"""Django命令行工具，用于管理项目。
整合了开发和生产环境的启动功能
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(message):
    """打印标题"""
    print(f"\n{'=' * 50}")
    print(f"{message}")
    print(f"{'=' * 50}\n")

def start_production_server():
    """启动生产环境服务器"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print_header("音乐分享与管理平台 - 生产环境启动")
    
    # 检查gunicorn是否安装
    try:
        import gunicorn
        print("✓ gunicorn已安装")
    except ImportError:
        print("× gunicorn未安装，请先安装: pip install gunicorn")
        return
    
    # 询问是否收集静态文件
    collect_static = input("是否收集静态文件? (y/n): ").lower() == 'y'
    if collect_static:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--no-input'])
    
    # 启动Gunicorn
    try:
        import psutil
        workers = psutil.cpu_count() * 2 + 1  # 推荐的worker数量
    except ImportError:
        workers = 3  # 默认值
        
    cmd = [
        'gunicorn',
        '--workers', str(workers),
        '--bind', '0.0.0.0:8000',
        'music_website.wsgi:application'
    ]
    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def main():
    """运行管理任务"""
    # 根据环境变量设置Django设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
    
    # 检查是否要启动生产环境服务器
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver_production':
        start_production_server()
        return
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确保它已安装并且在PYTHONPATH环境变量中可用。"
            "您是否忘记激活虚拟环境?"
        ) from exc
        
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
