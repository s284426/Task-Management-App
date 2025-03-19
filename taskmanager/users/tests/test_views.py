from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    # Registration
    def test_admin_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newadmin',
            'email': 'admin@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'is_superuser': True
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newadmin').exists())
        self.assertTrue(User.objects.get(username='newadmin').is_superuser)

    # Profile Update
    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'New bio'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertRedirects(response, reverse('profile'))

    # Logout
    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))