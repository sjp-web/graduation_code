#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目启动脚本 - 简化版
根据环境变量DEBUG自动选择启动方式
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def print_header(message):
    """打印标题"""
    print(f"\n{'=' * 50}")
    print(f"{message}")
    print(f"{'=' * 50}\n")

def start_server():
    """根据环境启动服务器"""
    # 加载环境变量
    load_dotenv()
    
    # 检查环境
    debug = os.getenv('DEBUG', 'True') == 'True'
    env_name = "开发环境" if debug else "生产环境"
    
    print_header(f"音乐分享与管理平台 - {env_name}启动")
    
    if debug:
        # 开发环境启动
        print("以开发模式启动 (DEBUG=True)")
        
        # 运行开发服务器
        cmd = [sys.executable, 'manage.py', 'runserver']
        print(f"执行命令: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n开发服务器已停止")
    else:
        # 生产环境启动
        print("以生产模式启动 (DEBUG=False)")
        
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
            workers = os.cpu_count() * 2 + 1  # 推荐的worker数量
            cmd = [
                'gunicorn',
                '--workers', str(workers),
                '--bind', '0.0.0.0:8000',
                'music_website.wsgi:application'
            ]
            print(f"执行命令: {' '.join(cmd)}")
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\nGunicorn服务器已停止")

if __name__ == "__main__":
    start_server() 