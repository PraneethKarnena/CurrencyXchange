from io import BytesIO
import requests

from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from api_service import models


class ModelsTests(TransactionTestCase):

    def create_user(self):
        user = User.objects.create_user(
            username='praneeth.codes@gmail.com',
            email='praneeth.codes@gmail.com',
            password='admin@123',
        )
        return user

    def test_picture_upload(self):
        user = self.create_user()

        IMAGE_URL = 'https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=100&w=100'
        image_response = requests.get(IMAGE_URL)
        image = BytesIO(image_response.content)

        picture = models.PictureModel.objects.create(
            user=user,
            file=File(image),
        )

        self.assertTrue(isinstance(picture, models.PictureModel))

    def test_adding_money(self):
        user = self.create_user()
        wallet = models.WalletModel.objects.create(user=user, money=100.0)

        self.assertTrue(isinstance(wallet, models.WalletModel))

    def test_currency_conversion(self):
        conversion = models.CurrencyConversionModel.objects.create(
            from_currency='USD',
            to_currency='INR',
            to_amount=71.22,
        )

        self.assertTrue(isinstance(conversion, models.CurrencyConversionModel))


class ApiTests(APITestCase):

    def test_signup_signin(self):
        response = self.client.post(
            reverse('api_service:signup_api'),
            {
                'email': 'praneeth.codes@gmail.com',
                'password': 'admin@123',
                'confirm_password': 'admin@123',
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('api_service:signin_api'),
            {
                'email': 'praneeth.codes@gmail.com',
                'password': 'admin@123',
            },
        )
        self.assertEqual(response.status_code, 200)

    def create_user(self):
        user = User.objects.create_user(
            username='praneeth.codes@gmail.com',
            email='praneeth.codes@gmail.com',
            password='admin@123',
        )
        return user

    def test_picture_upload_viewing(self):
        user = self.create_user()
        token, _ = Token.objects.get_or_create(user=user)

        IMAGE_URL = 'https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=100&w=100'
        image_response = requests.get(IMAGE_URL)
        image = BytesIO(image_response.content)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(
            reverse('api_service:profile_picture_api'),
            {'file': image},
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)

        response = client.get(
            reverse('api_service:profile_picture_api'),
        )
        self.assertEqual(response.status_code, 200)

    def test_wallet_ops(self):
        user = self.create_user()
        token, _ = Token.objects.get_or_create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(
            reverse('api_service:wallet_api'),
        )
        self.assertEqual(response.status_code, 201)

        response = client.get(
            reverse('api_service:wallet_api'),
        )
        self.assertEqual(response.status_code, 200)

    def text_currency_conversion(self):
        user = self.create_user()
        token, _ = Token.objects.get_or_create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(
            reverse('api_service:currency_conversion_api'),
            {
                'from_currency': 'USD',
                'to_currency': 'INR',
            },
        )
        self.assertEqual(response.status_code, 200)