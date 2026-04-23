from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import PlatformUser
from apps.platforms.models import Platform, PlatformSetting


class AuthFlowsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.platform_a = Platform.objects.create(name='Plataforma A', slug='plataforma-a', is_active=True)
        PlatformSetting.objects.create(
            platform=self.platform_a,
            max_devices=2,
            allow_inactive_login=False,
        )

        self.platform_b = Platform.objects.create(name='Plataforma B', slug='plataforma-b', is_active=True)
        PlatformSetting.objects.create(
            platform=self.platform_b,
            max_devices=5,
            allow_inactive_login=True,
        )

    @patch('apps.notifications.handlers.logger.info')
    def test_register_success_triggers_notification(self, logger_info):
        resp = self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'User@Email.com',
                'password': 'StrongPass123',
                'first_name': 'A',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['email'], 'user@email.com')
        self.assertTrue(PlatformUser.objects.filter(platform=self.platform_a, email='user@email.com').exists())
        logger_info.assert_called()

    def test_same_email_allowed_in_different_platform(self):
        self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'same@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )

        resp = self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-b',
                'email': 'same@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, 201)

    def test_same_email_rejected_within_same_platform(self):
        self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'dup@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )

        resp = self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'dup@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, 400)

    def test_login_success_with_correct_platform(self):
        self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'login@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )

        resp = self.client.post(
            '/api/auth/login/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'login@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_login_fails_with_incorrect_platform(self):
        self.client.post(
            '/api/auth/register/',
            {
                'platform_slug': 'plataforma-a',
                'email': 'wrongplatform@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )

        resp = self.client.post(
            '/api/auth/login/',
            {
                'platform_slug': 'plataforma-b',
                'email': 'wrongplatform@email.com',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(resp.status_code, 400)
