from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
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
