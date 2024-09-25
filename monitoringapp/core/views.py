# core/views.py

from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext as _
from django.utils import timezone  # Добавляем импорт timezone
from .forms import UserProfileForm, CustomPasswordChangeForm  # Импортируем кастомные формы
from .forms import PriceForm
from django.contrib.auth.decorators import login_required

# Страница для ввода цен
@login_required(login_url='login_required')  # Переадресация на страницу для неавторизованных
def price_add(request):
    return render(request, 'price_add.html')

# Личный кабинет
@login_required(login_url='login_required')  # Переадресация на специальную страницу
def profile_view(request):
    if request.method == 'POST':
        # Логика обработки профиля
        ...
    else:
        return render(request, 'profile.html')

# Страница для неавторизованных пользователей
def login_required_view(request):
    return render(request, 'login_required.html')

def register_view(request):
    print("Регистрация: представление вызвано!")  # Текст для проверки
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверяем, что пользователь существует и пароль верен
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Авторизуем пользователя и переадресуем на главную страницу
            login(request, user)
            return redirect('start_page')  # Переадресация на главную страницу
        else:
            # Если неверный логин или пароль
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'login.html')




@login_required
def profile_view(request):
    # Обработка формы редактирования профиля
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()  # Сохраняем изменения в профиль
                return redirect('profile')  # Перенаправляем обратно в профиль

        # Обработка формы смены пароля
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)  # Используем кастомную форму
            if password_form.is_valid():
                user = password_form.save()  # Сохраняем новый пароль
                update_session_auth_hash(request, user)  # Обновляем сессию, чтобы не разлогинило
                return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)  # Используем кастомную форму

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })



def start_page(request):
    translated_text = _("Главная страница")
    return render(request, 'start_page.html', {'translated_text': translated_text})

@login_required
def add_price(request):
    language = request.LANGUAGE_CODE  # Получаем текущий язык
    if request.method == 'POST':
        form = PriceForm(request.POST, language=language)
        if form.is_valid():
            price = form.save(commit=False)
            price.username = request.user
            price.date = timezone.now()
            price.save()
            return redirect('price_add')
    else:
        form = PriceForm(language=language)

    return render(request, 'price_add.html', {'form': form})


def price_add_list(request):
    # Здесь логика для добавления цен списком
    return render(request, 'price_add_list.html')  # Вы должны создать шаблон price_add_list.html


# Остальные представления


def statistics(request):
    return render(request, 'statistics.html')

def about_us(request):
    return render(request, 'about_us.html')
