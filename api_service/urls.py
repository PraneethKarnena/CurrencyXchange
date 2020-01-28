from django.urls import path

from api_service import views

urlpatterns = [
    path('signup/', views.signup_api, name='signup_api'),
]