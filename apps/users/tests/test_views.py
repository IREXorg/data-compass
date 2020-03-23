from django.test import TestCase
from django.urls import reverse


class ProfileViewTest(TestCase):
    """Unit tests for ProfileView"""

    def test_profile_login_redirect(self):
        """Test if unauthenticated user will be redirected to login url"""
        url = reverse('users:profile-detail')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('account_login')}?next={url}")


class ProfileUpdateViewTest(TestCase):
    """Unit tests for ProfileUpdateView"""

    def test_profile_login_redirect(self):
        """Test if unauthenticated user will be redirected to login url"""
        url = reverse('users:profile-update')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('account_login')}?next={url}")
