from django.test import TestCase
from django.contrib.auth.models import User
from music.models import Music, Profile, Comment, MusicDownload

class MusicModelTest(TestCase):
    """测试Music模型"""
    
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # 创建测试音乐
        self.music = Music.objects.create(
            title='测试音乐',
            artist='测试艺术家',
            album='测试专辑',
            release_date='2023-01-01',
            uploaded_by=self.user,
            category='pop'
        )
    
    def test_music_creation(self):
        """测试音乐创建"""
        self.assertEqual(self.music.title, '测试音乐')
        self.assertEqual(self.music.artist, '测试艺术家')
        self.assertEqual(self.music.uploaded_by, self.user)
        
    def test_music_str(self):
        """测试音乐字符串表示"""
        self.assertEqual(str(self.music), '测试音乐')


class ProfileModelTest(TestCase):
    """测试Profile模型"""
    
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Profile应该由信号自动创建
        self.profile = self.user.profile
        
    def test_profile_creation(self):
        """测试个人资料是否自动创建"""
        self.assertIsNotNone(self.profile)
        self.assertEqual(self.profile.user, self.user)
        
    def test_profile_str(self):
        """测试个人资料字符串表示"""
        self.assertEqual(str(self.profile), 'testuser') 