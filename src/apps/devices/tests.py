from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import PlatformUser
from apps.devices.models import Device
from apps.platforms.models import Platform, PlatformSetting


class DeviceFlowsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.platform = Platform.objects.create(name='Plataforma A', slug='plataforma-a', is_active=True)
        PlatformSetting.objects.create(platform=self.platform, max_devices=2, allow_inactive_login=False)

        self.user1 = PlatformUser(platform=self.platform, email='u1@email.com')
        self.user1.set_password('StrongPass123')
        self.user1.save()

        self.user2 = PlatformUser(platform=self.platform, email='u2@email.com')
        self.user2.set_password('StrongPass123')
        self.user2.save()

        login = self.client.post(
            '/api/auth/login/',
            {'platform_slug': 'plataforma-a', 'email': 'u1@email.com', 'password': 'StrongPass123'},
            format='json',
        )
        self.access = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_devices_list_returns_only_authenticated_users_devices(self):
        Device.objects.create(platform_user=self.user1, name='d1', ip_address='127.0.0.1', is_active=True)
        Device.objects.create(platform_user=self.user2, name='d2', ip_address='127.0.0.2', is_active=True)

        resp = self.client.get('/api/devices/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], 'd1')

    def test_create_device_respects_max_devices(self):
        resp1 = self.client.post(
            '/api/devices/',
            {'name': 'd1', 'ip_address': '10.0.0.1', 'is_active': True},
            format='json',
        )
        self.assertEqual(resp1.status_code, 201)

        resp2 = self.client.post(
            '/api/devices/',
            {'name': 'd2', 'ip_address': '10.0.0.2', 'is_active': True},
            format='json',
        )
        self.assertEqual(resp2.status_code, 201)

        resp3 = self.client.post(
            '/api/devices/',
            {'name': 'd3', 'ip_address': '10.0.0.3', 'is_active': True},
            format='json',
        )
        self.assertEqual(resp3.status_code, 400)
