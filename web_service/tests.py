from django.test import SimpleTestCase
from django.urls import reverse


class WebServiceTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get(reverse('web_service:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_signin_page_status_code(self):
        response = self.client.get(reverse('web_service:signin_page'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_status_code(self):
        response = self.client.get(reverse('web_service:signup_page'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page_status_code(self):
        response = self.client.get(reverse('web_service:dashboard_page'))
        self.assertEqual(response.status_code, 200)