from django.urls import path

from web_service import views


urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('signin/', views.signin_view, name='signin_page'),
    path('signup/', views.signup_view, name='signup_page'),
    path('dashboard/', views.dashboard_view, name='dashboard_page'),
]