from django.test import TestCase, Client
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage_tech(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_author(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)
