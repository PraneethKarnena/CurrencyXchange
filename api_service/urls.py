from django.urls import path

from api_service import views

urlpatterns = [
    path('signup/', views.signup_api, name='signup_api'),
    path('signin/', views.signin_api, name='signin_api'),

    path('profile-picture/', views.ProfilePictureListView.as_view(), name='profile_picture_api'),
    path('wallet/', views.WalletListView.as_view(), name='wallet_api'),
    path('convert-currency/', views.currency_conversion_api, name='currency_conversion_api'),
]