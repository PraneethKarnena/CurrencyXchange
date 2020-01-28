from django.urls import path

from web_service import views


urlpatterns = [
    path('', views.home_view, name='home_page'),
]