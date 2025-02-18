from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from graduation_code.music.models import Profile

class ProfileTestCase(TestCase):
    def test_avatar_upload(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(
            user=user,
            avatar=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        )
        self.assertTrue(profile.avatar.name.startswith('avatars/'))

    def test_invalid_avatar_upload(self):
        user = User.objects.create_user(username='testuser', password='12345')
        with self.assertRaises(ValidationError):
            Profile.objects.create(
                user=user,
                avatar=SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
            )
