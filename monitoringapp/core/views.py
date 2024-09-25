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
from decimal import Decimal  # Импортируем Decimal для работы с числами

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

# @login_required
# def add_price(request):
#     language = request.LANGUAGE_CODE  # Получаем текущий язык
#     if request.method == 'POST':
#         form = PriceForm(request.POST, language=language)
#         if form.is_valid():
#             price = form.save(commit=False)
#             price.username = request.user
#             price.date = timezone.now()
#             price.save()
#             return redirect('price_add')
#     else:
#         form = PriceForm(language=language)
#
#     return render(request, 'price_add.html', {'form': form})


@login_required
def add_price(request):
    language = request.LANGUAGE_CODE  # Получаем текущий язык
    if request.method == 'POST':
        form = PriceForm(request.POST, language=language)
        if form.is_valid():
            price = form.save(commit=False)  # Не сохраняем сразу, чтобы добавить дополнительные данные

            price.username = request.user  # Устанавливаем текущего пользователя
            price.date = timezone.now()  # Устанавливаем текущую дату

            # Явно получаем объект продукта
            selected_product = form.cleaned_data.get('ID_product')
            price.ID_product = selected_product  # Назначаем объект продукта
            price.years_norm = selected_product.years_norm  # Присваиваем years_norm из продукта

            # Получаем другие данные из формы
            quantity = form.cleaned_data.get('quantity')
            price_value = form.cleaned_data.get('price')
            ID_measure = form.cleaned_data.get('ID_measure')

            if quantity and price_value and ID_measure:
                # Приводим количество к Decimal для совместимости
                quantity = Decimal(quantity)

                # Выполняем расчеты в зависимости от выбранной единицы измерения
                if ID_measure.ID_unit == 1:  # Килограмм
                    price.price_for_kg = price_value / quantity
                elif ID_measure.ID_unit == 2:  # Грамм
                    price.price_for_kg = price_value / (quantity / Decimal(1000))
                elif ID_measure.ID_unit == 3:  # Штук
                    price.price_for_kg = price_value / quantity
                elif ID_measure.ID_unit == 4:  # Пучок
                    price.price_for_kg = price_value / (quantity * Decimal(150) / Decimal(1000))
                elif ID_measure.ID_unit == 5:  # Упаковка
                    price.price_for_kg = price_value / (selected_product.years_norm * Decimal(1000))
                elif ID_measure.ID_unit == 6:  # Булка
                    price.price_for_kg = price_value / (quantity * Decimal(400) / Decimal(1000))
                elif ID_measure.ID_unit == 7:  # Литр
                    price.price_for_kg = price_value / quantity
                elif ID_measure.ID_unit == 8:  # Бутылка
                    price.price_for_kg = price_value / (quantity * Decimal(160) / Decimal(1000))

                # Рассчитываем цену за год и за месяц
                price.price_for_year = price.price_for_kg * Decimal(price.years_norm)
                price.price_for_month = price.price_for_year / Decimal(12)

            # Сохраняем данные в БД
            price.save()
            return redirect('thanks')  # Отправляем на страницу благодарности
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

def thanks(request):
    return render(request, 'thanks.html')