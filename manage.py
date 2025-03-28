#!/usr/bin/env python
"""Django命令行工具，用于管理项目。"""
import os
import sys


def main():
    """运行管理任务"""
    # 根据环境变量设置Django设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_website.settings')
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
