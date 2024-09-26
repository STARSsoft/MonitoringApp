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
from decimal import Decimal  # Импортируем Decimal для работы с числами
from django.http import JsonResponse
from .models import Product, UnitOfMeasurement, Region, Price


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
    language = request.LANGUAGE_CODE
    if request.method == 'POST':
        form = PriceForm(request.POST, language=language)

        if form.is_valid():
            price = form.save(commit=False)

            price.username = request.user  # Устанавливаем текущего пользователя
            price.date = timezone.now()  # Устанавливаем текущую дату

            # Получаем объект продукта
            selected_product = form.cleaned_data.get('ID_product')
            price.ID_product = selected_product
            price.years_norm = selected_product.years_norm

            # Получаем данные из формы
            quantity = form.cleaned_data.get('quantity')
            price_value = form.cleaned_data.get('price')
            ID_measure = form.cleaned_data.get('ID_measure')

            # Вычисляем цену за кг, за год и за месяц
            price.price_for_kg, price.price_for_year, price.price_for_month = calculate_prices(
                quantity, price_value, ID_measure, selected_product.years_norm
            )

            # Сохраняем запись
            price.save()
            return JsonResponse({'status': 'success', 'message': 'Price saved successfully'})

        return JsonResponse({'status': 'error', 'errors': form.errors})

    else:
        form = PriceForm(language=language)

    return render(request, 'price_add.html', {'form': form})

def calculate_prices(quantity, price, measure, years_norm):
    quantity = Decimal(quantity)
    price = Decimal(price)
    years_norm = Decimal(years_norm)

    if measure.ID_unit == 1:  # Килограмм
        price_for_kg = price / quantity
    elif measure.ID_unit == 2:  # Грамм
        price_for_kg = price / (quantity / Decimal(1000))
    elif measure.ID_unit == 3:  # Штук
        price_for_kg = price / quantity
    elif measure.ID_unit == 4:  # Пучок
        price_for_kg = price / (quantity * Decimal(150) / Decimal(1000))
    elif measure.ID_unit == 5:  # Упаковка
        price_for_kg = price / (years_norm * Decimal(1000))
    elif measure.ID_unit == 6:  # Булка
        price_for_kg = price / (quantity * Decimal(400) / Decimal(1000))
    elif measure.ID_unit == 7:  # Литр
        price_for_kg = price / quantity
    elif measure.ID_unit == 8:  # Бутылка
        price_for_kg = price / (quantity * Decimal(160) / Decimal(1000))

    price_for_year = price_for_kg * years_norm
    price_for_month = price_for_year / Decimal(12)

    return price_for_kg, price_for_year, price_for_month


# Страница для внесения цен списком
@login_required
def price_add_list(request):
    language = request.LANGUAGE_CODE  # Получаем текущий язык

    if request.method == 'POST':
        region_id = request.POST.get('region')
        if region_id == '---':
            return JsonResponse({'status': 'error', 'message': 'Выберите регион'})

        # Получаем регион по ID
        try:
            region = Region.objects.get(ID_region=region_id)
        except Region.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Регион не найден'})

        # Фильтрация заполненных строк (только с ценой и количеством)
        products_to_save = []
        for product in Product.objects.all():
            quantity = request.POST.get(f'quantity_{product.ID_product}')
            price = request.POST.get(f'price_{product.ID_product}')
            measure_id = request.POST.get(f'measure_{product.ID_product}')

            if quantity and price:
                try:
                    quantity = Decimal(quantity)
                    price = Decimal(price)
                    measure = UnitOfMeasurement.objects.get(pk=measure_id)

                    # Заполняем данные для сохранения
                    products_to_save.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'measure': measure
                    })
                except (ValueError, UnitOfMeasurement.DoesNotExist):
                    return JsonResponse({'status': 'error', 'message': 'Некорректные данные'})

        if not products_to_save:
            return JsonResponse({'status': 'error', 'message': 'Заполните хотя бы одну строку с ценой и количеством'})

        # Сохраняем данные в базу
        for entry in products_to_save:
            Price.objects.create(
                ID_product=entry['product'],
                ID_region=region,
                quantity=entry['quantity'],
                ID_measure=entry['measure'],
                price=entry['price'],
                username=request.user,
                date=timezone.now(),
                years_norm=entry['product'].years_norm,
                price_for_kg=calculate_price_for_kg(entry['price'], entry['quantity'], entry['measure'], entry['product']),
                price_for_year=calculate_price_for_year(entry['price'], entry['quantity'], entry['product'], entry['measure']),
                price_for_month=calculate_price_for_month(entry['price'], entry['quantity'], entry['product'], entry['measure']),
            )

        return JsonResponse({'status': 'success'})

    # Подготовка данных для отображения на разных языках
    products = Product.objects.all()
    regions = Region.objects.all()

    # Подбираем нужные поля на основе выбранного языка
    if language == 'kk':
        products_data = [{'id': p.ID_product, 'name': p.product_KZ, 'measure_default': p.measure_default, 'measures': get_measures(p, 'kk')} for p in products]
        regions_data = [{'id': r.ID_region, 'name': r.region_KZ} for r in regions]
    elif language == 'en':
        products_data = [{'id': p.ID_product, 'name': p.product_EN, 'measure_default': p.measure_default, 'measures': get_measures(p, 'en')} for p in products]
        regions_data = [{'id': r.ID_region, 'name': r.region_EN} for r in regions]
    else:
        products_data = [{'id': p.ID_product, 'name': p.product_RU, 'measure_default': p.measure_default, 'measures': get_measures(p, 'ru')} for p in products]
        regions_data = [{'id': r.ID_region, 'name': r.region_RU} for r in regions]

    return render(request, 'price_add_list.html', {
        'products': products_data,
        'regions': regions_data,
    })


# Вспомогательная функция для получения доступных единиц измерения
def get_measures(product, language):
    measures = []
    measure_names = {
        'kk': {
            1: 'Килограмм',
            2: 'Грамм',
            3: 'Дана',
            4: 'Байлам',
            5: 'Қаптама',
            6: 'Орама',
            7: 'Литр',
            8: 'Бөтелке',
        },
        'ru': {
            1: 'Килограмм',
            2: 'Грамм',
            3: 'Штук',
            4: 'Пучок',
            5: 'Упаковка',
            6: 'Булка',
            7: 'Литр',
            8: 'Бутылка',
        },
        'en': {
            1: 'Kilogram',
            2: 'Gram',
            3: 'Piece',
            4: 'Bunch',
            5: 'Pack',
            6: 'Loaf',
            7: 'Liter',
            8: 'Bottle',
        }
    }

    if product.measure_1:
        measures.append({'id': 1, 'name': measure_names[language][1]})
    if product.measure_2:
        measures.append({'id': 2, 'name': measure_names[language][2]})
    if product.measure_3:
        measures.append({'id': 3, 'name': measure_names[language][3]})
    if product.measure_4:
        measures.append({'id': 4, 'name': measure_names[language][4]})
    if product.measure_5:
        measures.append({'id': 5, 'name': measure_names[language][5]})
    if product.measure_6:
        measures.append({'id': 6, 'name': measure_names[language][6]})
    if product.measure_7:
        measures.append({'id': 7, 'name': measure_names[language][7]})
    if product.measure_8:
        measures.append({'id': 8, 'name': measure_names[language][8]})

    return measures

@login_required
def get_measurements(request, product_id):
    try:
        # Получаем выбранный продукт по его ID
        product = Product.objects.get(pk=product_id)

        # Определяем текущий язык
        language = request.LANGUAGE_CODE

        # Функция для получения наименования единицы измерения в зависимости от языка
        def get_measurement_name(unit, lang):
            if lang == 'kk':
                return unit.name_unit_KZ
            elif lang == 'en':
                return unit.name_unit_EN
            return unit.name_unit_RU  # По умолчанию русский

        # Список доступных единиц измерения
        available_measures = []

        if product.measure_1:
            unit = UnitOfMeasurement.objects.get(pk=1)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_2:
            unit = UnitOfMeasurement.objects.get(pk=2)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_3:
            unit = UnitOfMeasurement.objects.get(pk=3)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_4:
            unit = UnitOfMeasurement.objects.get(pk=4)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_5:
            unit = UnitOfMeasurement.objects.get(pk=5)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_6:
            unit = UnitOfMeasurement.objects.get(pk=6)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_7:
            unit = UnitOfMeasurement.objects.get(pk=7)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})
        if product.measure_8:
            unit = UnitOfMeasurement.objects.get(pk=8)
            available_measures.append({'id': unit.ID_unit, 'name': get_measurement_name(unit, language)})

        # Устанавливаем единицу измерения по умолчанию
        default_measure = product.measure_default

        return JsonResponse({
            'measures': available_measures,
            'default_measure': default_measure
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


# Функция для расчета цены за килограмм
def calculate_price_for_kg(price, quantity, measure, product):
    if measure.ID_unit == 1:  # Килограмм
        return price / quantity
    elif measure.ID_unit == 2:  # Грамм
        return price / (quantity / Decimal(1000))
    elif measure.ID_unit == 3:  # Штук
        return price / quantity
    elif measure.ID_unit == 4:  # Пучок
        return price / (quantity * Decimal(150) / Decimal(1000))
    elif measure.ID_unit == 5:  # Упаковка
        return price / (product.years_norm * Decimal(1000))
    elif measure.ID_unit == 6:  # Булка
        return price / (quantity * Decimal(400) / Decimal(1000))
    elif measure.ID_unit == 7:  # Литр
        return price / quantity
    elif measure.ID_unit == 8:  # Бутылка
        return price / (quantity * Decimal(160) / Decimal(1000))
    else:
        return Decimal(0)  # Если единица измерения не определена, возвращаем 0

# Функция для расчета цены за год
def calculate_price_for_year(price, quantity, product, measure):
    price_for_kg = calculate_price_for_kg(price, quantity, measure, product)
    return price_for_kg * Decimal(product.years_norm)

# Функция для расчета цены за месяц
def calculate_price_for_month(price, quantity, product, measure):
    price_for_year = calculate_price_for_year(price, quantity, product, measure)
    return price_for_year / Decimal(12)


# Остальные представления
def statistics(request):
    return render(request, 'statistics.html')

def about_us(request):
    return render(request, 'about_us.html')

def thanks(request):
    return render(request, 'thanks.html')
