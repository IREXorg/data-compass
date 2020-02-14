from django.test import TestCase
from django.urls import reverse


class ProfileViewTest(TestCase):
    """Unit tests for ProfileView"""

    def test_profile_login_redirect(self):
        """Test if unauthenticated user will be redirected to login url"""
        profile_url = reverse('users:profile-detail')
        response = self.client.get(profile_url)
        self.assertRedirects(response, f"{reverse('account_login')}?next={profile_url}")
