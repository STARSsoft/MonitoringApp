# core/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.start_page, name='start_page'),  # Путь для стартовой страницы
    path('priceadd/', views.price_add, name='price_add'),  # Путь для страницы ввода цен
    path('statistics/', views.statistics, name='statistics'),   # Путь для страницы вывода статистики
    path('about/', views.about_us, name='about_us'),    # Путь для страницы О нас
    path('login/', views.login_view, name='login'),     # Путь для страницы авторизации
    path('register/', views.register_view, name='register'),    # Путь для страницы регистрации
    path('profile/', views.profile_view, name='profile'),       # Путь для страницы личного кабинета
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Путь для деавторизации
    path('login-required/', views.login_required_view, name='login_required'),
    path('priceadd-list/', views.price_add_list, name='price_add_list'),  # Для списочной формы

]



