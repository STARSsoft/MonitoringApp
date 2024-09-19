# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),  # Путь для стартовой страницы
]
