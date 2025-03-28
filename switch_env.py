#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版环境切换工具
通过修改DEBUG的值在开发环境和生产环境之间切换
"""

import os
import sys
import shutil
from pathlib import Path

def print_header(message):
    """打印标题"""
    print(f"\n{'=' * 50}")
    print(f"{message}")
    print(f"{'=' * 50}\n")

def switch_env(env_type):
    """切换环境
    
    Args:
        env_type: 'dev' 或 'prod'
    """
    if env_type not in ['dev', 'prod']:
        print("错误: 环境参数必须是 'dev' 或 'prod'")
        return False
    
    # 检测.env文件
    env_file = Path('.env')
    if not env_file.exists():
        # 如果不存在.env文件，则从.env.example复制
        if not Path('.env.example').exists():
            print("错误: .env 和 .env.example 文件均不存在")
            return False
        shutil.copy('.env.example', '.env')
        print("已从 .env.example 创建 .env 文件")
    
    # 读取当前.env内容
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改DEBUG值
    debug_value = 'True' if env_type == 'dev' else 'False'
    
    # 替换DEBUG行
    if 'DEBUG=' in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('DEBUG='):
                new_lines.append(f'DEBUG={debug_value}')
            else:
                new_lines.append(line)
        new_content = '\n'.join(new_lines)
    else:
        # 如果不存在DEBUG行，则添加
        new_content = f'DEBUG={debug_value}\n' + content
    
    # 写回文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    env_name = "开发环境" if env_type == 'dev' else "生产环境"
    print(f"已成功切换到{env_name}!")
    return True

def main():
    """主函数"""
    print_header("音乐分享与管理平台 - 简化版环境切换工具")
    
    if len(sys.argv) != 2:
        print("用法: python switch_env.py [dev|prod]")
        print("  dev  - 切换到开发环境 (DEBUG=True)")
        print("  prod - 切换到生产环境 (DEBUG=False)")
        return
    
    env_type = sys.argv[1].lower()
    if switch_env(env_type):
        env_name = "开发环境" if env_type == 'dev' else "生产环境"
        print(f"\n现在您的项目处于{env_name}模式。")
        
        if env_type == 'prod':
            print("\n生产环境注意事项:")
            print("1. DEBUG=False，错误将记录到日志而不显示在页面上")
            print("2. 请先运行 python manage.py collectstatic 收集静态文件")
            print("3. 启动方式: gunicorn music_website.wsgi:application")
        else:
            print("\n开发环境注意事项:")
            print("1. DEBUG=True，错误详情将显示在浏览器中")
            print("2. 可以使用 python manage.py runserver 启动开发服务器")

if __name__ == "__main__":
    main() 