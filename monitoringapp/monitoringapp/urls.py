# monitoringapp/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from core import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import set_language
from django.urls import path

# Подключаем URL для смены языка через стандартный обработчик
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Включаем обработку изменения языка
]

# Многоязычные маршруты
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.start_page, name='start_page'),
    path('priceadd/', views.add_price, name='price_add'),  # Исправляем на 'add_price'
    path('statistics/', views.statistics, name='statistics'),
    path('about/', views.about_us, name='about_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login-required/', views.login_required_view, name='login_required'),
    path('priceadd-list/', views.price_add_list, name='price_add_list'),
    path('set-language/', set_language, name='set_language'),
    path('thanks/', views.thanks, name='thanks'),
    path('get-measurements/<int:product_id>/', views.get_measurements, name='get_measurements'),
    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
)
