from datetime import timedelta
import requests

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics

from api_service import models
from api_service import serializers


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    """ Sign up the user """
    response_status = data = None
    try:
        email = request.data['email']
        password = request.data['password']
        confirm_password = request.data['confirm_password']

        # Passwords do not match
        if password != confirm_password:
            raise Exception('Passwords do not match!')

        user, created = User.objects.get_or_create(username=email, email=email)

        # User already in the database
        if not created:
            raise Exception('User already exists!')

        # Save the password to the database
        user.set_password(password)
        user.save()

        data = {'success': True, 'message': 'User created successfully!'}
        response_status = status.HTTP_200_OK

    except Exception as e:
        data = {'success': False, 'message': str(e)}
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=response_status)


@api_view(['POST'])
@permission_classes([AllowAny])
def signin_api(request):
    """ Sign in the user """
    response_status = data = None
    try:
        email = request.data['email']
        password = request.data['password']

        user_exists = User.objects.filter(username=email).exists()

        # No such user
        if not user_exists:
            raise Exception('User does not exist!')

        # Authenticate
        user = authenticate(username=email, password=password)

        # Invalid password
        if user is None:
            raise Exception('Invalid password!')

        # User authenticated successfully, send Token
        token, _ = Token.objects.get_or_create(user=user)

        data = {'success': True, 'token': token.key}
        response_status = status.HTTP_200_OK

    except Exception as e:
        data = {'success': False, 'message': str(e)}
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=response_status)


class ProfilePictureListView(generics.ListCreateAPIView):

    serializer_class = serializers.ProfilePictureSerializer

    def get_queryset(self):
        queryset = models.PictureModel.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # Remove previous profile pictures before adding one
        _ = models.PictureModel.objects.filter(user=self.request.user).delete()
        serializer.save(user=self.request.user)


class WalletListView(generics.ListCreateAPIView):

    serializer_class = serializers.WalletSerializer

    def get_queryset(self):
        queryset = models.WalletModel.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        wallet_exists = models.WalletModel.objects.filter(user=self.request.user).exists()
        if wallet_exists:
            wallet = models.WalletModel.objects.get(user=self.request.user)
            wallet_money = wallet.money
            wallet.delete()
            serializer.save(user=self.request.user, money=(wallet_money + float(self.request.data['money'])))
            return

        serializer.save(user=self.request.user)


@api_view(['POST',])
def currency_conversion_api(request):
    """ Convert the currency """
    response_status = data = None
    try:

        from_currency = request.data['from_currency']
        to_currency = request.data['to_currency']

        if to_currency == from_currency:
            raise Exception('Currencies are same!')

        CACHE_TIME_HOURS = 1

        conversion = models.CurrencyConversionModel.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            updated_at__gt=(timezone.now()-timedelta(hours=CACHE_TIME_HOURS))
        )

        conversion_object = None
        if conversion:
            conversion_object = conversion[0]
        else:
            _ = models.CurrencyConversionModel.objects.filter(from_currency=from_currency,
            to_currency=to_currency,).delete()

            response = call_conversion_api(from_currency, to_currency)
            conversion = models.CurrencyConversionModel.objects.create(
                from_currency=from_currency,
                to_currency=to_currency,
                to_amount=response['rates'][to_currency]
            )
            conversion_object = conversion

        conversion_serializer = serializers.CurrencyConversionSerializer(conversion_object, many=False)

        data = {'success': True, 'data': conversion_serializer.data}
        response_status = status.HTTP_200_OK

    except Exception as e:
        data = {'success': False, 'message': str(e)}
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=response_status)


def call_conversion_api(from_currency, to_currency):
    """ Call the 3rd-party conversion API """
    API_URL = f'https://api.exchangeratesapi.io/latest?symbols={to_currency}&base={from_currency}'

    response = requests.get(API_URL).json()
    return response