from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from music.models import Music, Profile, Comment

class UserViewsTest(TestCase):
    """测试用户相关视图"""
    
    def setUp(self):
        # 创建客户端
        self.client = Client()
        
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
    def test_login_view(self):
        """测试登录视图"""
        # 获取登录页面
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # 测试登录
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('music_list'))
        
    def test_register_view(self):
        """测试注册视图"""
        # 获取注册页面
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
        # 测试注册新用户
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)


class MusicViewsTest(TestCase):
    """测试音乐相关视图"""
    
    def setUp(self):
        # 创建客户端
        self.client = Client()
        
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
        
        # 登录用户
        self.client.login(username='testuser', password='testpassword')
        
    def test_music_list_view(self):
        """测试音乐列表视图"""
        response = self.client.get(reverse('music_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试音乐')
        
    def test_music_detail_view(self):
        """测试音乐详情视图"""
        response = self.client.get(reverse('music_detail', args=[self.music.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试音乐')
        self.assertContains(response, '测试艺术家') 