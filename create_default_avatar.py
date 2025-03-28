"""
生成默认用户头像的简单脚本
"""
from PIL import Image, ImageDraw
import os

def generate_default_avatar():
    """生成一个简单的灰色用户头像"""
    # 确保目录存在
    os.makedirs('music/static/images/avatars', exist_ok=True)
    os.makedirs('media/avatars', exist_ok=True)
    
    # 创建一个200x200的图片，背景色为灰色
    image = Image.new('RGB', (200, 200), color=(200, 200, 200))
    draw = ImageDraw.Draw(image)
    
    # 画一个深灰色圆形作为头部
    draw.ellipse((50, 30, 150, 130), fill=(150, 150, 150))
    
    # 画一个深灰色矩形作为身体
    draw.rectangle((75, 120, 125, 180), fill=(150, 150, 150))
    
    # 保存图片到静态目录
    image.save('music/static/images/avatars/default.png')
    # 同时保存一份到media目录
    image.save('media/avatars/default.png')
    
    print("默认头像已生成并保存到以下位置:")
    print("- music/static/images/avatars/default.png")
    print("- media/avatars/default.png")

if __name__ == "__main__":
    generate_default_avatar() 