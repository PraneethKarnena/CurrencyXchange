from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def home_view(request):
    """ Home page - return simple home template """
    return render(request, 'web_service/home.html')


@require_http_methods(['GET'])
def signin_view(request):
    """ Sign in page - return page with email and password fields """
    return render(request, 'web_service/signin.html')


@require_http_methods(['GET'])
def signup_view(request):
    """ Sign up page - return page with email, confirm_password and password fields """
    return render(request, 'web_service/signup.html')