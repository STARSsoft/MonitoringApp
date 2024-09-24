# monitoringapp/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from core import views
from django.contrib.auth import views as auth_views

# Подключаем URL для смены языка через стандартный обработчик
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Включаем обработку изменения языка
]

# Многоязычные маршруты
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.start_page, name='start_page'),
    path('priceadd/', views.price_add, name='price_add'),
    path('statistics/', views.statistics, name='statistics'),
    path('about/', views.about_us, name='about_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login-required/', views.login_required_view, name='login_required'),
)
