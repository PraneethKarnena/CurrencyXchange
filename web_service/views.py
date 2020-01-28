from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def home_view(request):
    """ Home page - return simple home template """
    return render(request, 'web_service/home.html')