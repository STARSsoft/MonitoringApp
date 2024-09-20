from django.shortcuts import render

# core/views.py

# Функция для запуска главной страницы
def start_page(request):
    return render(request, 'start_page.html')

# Функция для запуска страницы ввода цен
def price_add(request):
    return render(request, 'price_add.html')

# Функция для запуска страницы статистики
def statistics(request):
    return render(request, 'statistics.html')

# Функция для запуска страницы О нас
def about_us(request):
    return render(request, 'about_us.html')

# Функция запуска страницы авторизации пользователя
def login_view(request):
    return render(request, 'login.html')

# Функция запуска страницы регистрации пользователя
def register_view(request):
    return render(request, 'register.html')

# Функция запуска страницы личного кабинета пользователя
def profile_view(request):
    return render(request, 'profile.html')

