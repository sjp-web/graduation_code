from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def optimize_upload(uploaded_file, max_size=(500, 500), quality=85):
    """
    优化上传的图片文件
    参数：
        uploaded_file: 上传的图片文件
        max_size: 最大尺寸（宽，高）
        quality: 压缩质量（1-100）
    返回：
        BytesIO对象包含优化后的图片数据
    """
    try:
        img = Image.open(uploaded_file)
        
        # 转换颜色模式
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 调整尺寸
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 优化保存
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        print(f"图片优化失败: {str(e)}")
        return None 