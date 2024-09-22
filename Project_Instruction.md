## Инструкция по созданию и работе над проектом.

1. Начать новый проект и "подружить" его с GitHub.
2. Обновить приложение pip `pip install --upgrade pip`
3. Установить Джанго `pip install django`
4. Создаем проект `django-admin startproject monitoringapp`
5. Переходим в папку проекта `cd monitoringapp`
6. Запускаем MySQL командой `mysql -u root -p`
7. Ввести пароль БД `admin1977` (пароль задается в процессе установки и создания БД)
8. Запустить приложение  **MySQL Workbench**
9. В приложении создаем таблицу в БД для проекта
10. Переходим в PyCharm, в папке с проектом находим файл **settings.py**

    в файле находим раздел с Базой данных и вставляем код

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pd_monitoringapp',
        'USER': 'root',
        'PASSWORD': 'admin1977',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```
11. Устанавливаем клиент MySQL в Джанго `pip install django mysqlclient
`
12. Создаем базовые таблицы Джанго `python manage.py migrate`
13. Проверяем работоспособность Джанго, запускаем команду `python manage.py runserver
`
14. Если все работает, то при переходе на адрес  http://127.0.0.1:8000/ мы увидим изображение ракеты.
15. Для остановки работы сервера нажимаем в терминале Ctrl+C
16. Далее находясь в папке с проектом создаем еще одно приложение `django-admin startproject core`. Это будет ядром приложения, где будет размещаться основная логика.
17. Дополнительно в папке с приложением создаем папку `templates`. Здесь будут храниться все шаблоны проекта.
18. Еще нужно создать папку `static/core/images`. В этой папке будем хранить все изображения, которые будут задействованы в проекте.
19. Чтобы наш проект увидел новые папки и файлы в них, в файле **settings.py** нужно добавить следующий код:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Путь до основной папки с шаблонами
        'APP_DIRS': True,  # Оставляем для поиска шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Данный код прописывает путь, до папки с шаблонами.
Дополнительно в этом же файле прописываем код, который покажет проекту директорию, где лежат файлы с изображениями.

```
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Указываем путь к папке 'static'
]
```

20. Дополнительно, нужно системе показать новые пути для приложений. Для этого в папке с приложением, в файле `urls.py` дописываем следующий код
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Включаем маршруты из приложения 'core'
]
```
21. Внутри папки `core` создаем свой файл `urls.py`. В нем прописываем следующий код
```
# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),  # Путь для стартовой страницы
    path('priceadd/', views.price_add, name='price_add'),  # Путь для страницы ввода цен
    path('statistics/', views.statistics, name='statistics'),   # Путь для страницы вывода статистики
    path('about/', views.about_us, name='about_us'),    # Путь для страницы О нас
]
```
Данный код прописывает пути до шаблонов страниц сайта. На данном этапе были указаны пути на шаблоны для Главной страницы, Страницы для ввода цен, Страницы со статистикой и странице О нас. 
22. Кроме путей до шаблонов, нужны сами шаблоны. Шаблоны располагаются в папке `templates`, которая в свою очередь лежит в основной папке проекта. Внутри папки создано четыре html файла `about_us.html`, `price_add.html`, `start_page.html`, `statistics.html`
23. Внутри файлов был прописан следующий код:
```
{% load static %}
<!-- templates/start_page.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Стартовая страница</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .banner {
            width: 100%;
            height: 200px;
            background-color: lightblue; /* Цвет баннера (можно заменить картинкой) */
        }
        .logo {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="banner">
        <!-- Здесь можно вставить картинку баннера -->
    </div>
     <div class="logo">
        <img src="{% static 'core/images/logo.png' %}" alt="Логотип" width="150" height="150">
    </div>
    <h1>Мониторинг цен на продукты питания</h1>
    <p>Русский | Қазақша | English</p>
</body>
</html>

```
В коде, в верхней части прописали строчку, которая позволяет загружать файлы из папки с изображениями. У всех остальных страниц код ничем не отличается, кроме тега титула и заголовка в теле страницы. Пока это только болванки страниц.
24. Ну и чтобы уже окончательно система увидела страницы и смогла загрузить их в браузере, нужно в файле `views.py` в папке `core` прописать функции вызова подготовленных страниц:
``` 
from django.shortcuts import render

# core/views.py

def start_page(request):
    return render(request, 'start_page.html')  

def price_add(request):
    return render(request, 'price_add.html')

def statistics(request):
    return render(request, 'statistics.html')

def about_us(request):
    return render(request, 'about_us.html')

```
25. Поскольку все страницы сайта будут иметь единый дизайн, то каждая страница по сути кроме необходимого контента будет иметь один и тот же html код, а это лишний трафик. Поэтому было принято создать базовый шаблон и внутри каждой страницы прописать код, который будет наследовать шаблон дизайна из базового файла. Для этого был создан файл `base.html` в котором прописали следующий код:
``` 
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мониторинг цен{% endblock %}</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .banner {
            width: 100%;
            height: 150px;
            background-image: url("{% static 'core/images/banner2.jpg' %}");
            background-size: cover;
        }
        .menu {
            margin-top: 20px;
        }
        .menu a {
            margin: 0 15px;
            text-decoration: none;
            color: black;
            font-size: 18px;
        }
        .menu a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="banner">
        <!-- Баннер из картинки banner2.jpg -->
    </div>
    <div class="menu">
        <a href="{% url 'start_page' %}">Главная</a>
        <a href="{% url 'price_add' %}">Добавить цены</a>
        <a href="{% url 'statistics' %}">Статистика</a>
        <a href="{% url 'about_us' %}">О нас</a>
    </div>
    
    <div class="content">
        {% block content %}
        <!-- Контент страниц -->
        {% endblock %}
    </div>
</body>
</html>

```
Дополнительно в дизайн сайта добавили файл с изображением для баннера.
26. Для остальных страниц прописал код 
``` 
{% extends 'base.html' %}

{% block title %}Главная страница{% endblock %}

{% block content %}
    <h1>Мониторинг цен на продукты питания</h1>
    <p>Русский | Қазақша | English</p>
{% endblock %}
 
```
Этот код загружает базовый шаблон и внутри файла конкретной страницы теперь можно делать изменения и прописывать логику не нарушая общего дизайна. Данный код одинаковый для всех страниц, за исключением текстового сопровождения каждой страницы.
27. Для дальнейшей работы с сайтом, а именно взаимодействием с базой данных, нужно создать супер пользователя Джанго. Для этого вводим в терминале команду `python manage.py createsuperuser` и следуем инструкциям.
28. Поскольку подразумевается, что сайтом будут пользоваться множество людей, то само собой, что необходимы формы регистрации, авторизации пользователя и его личного кабинета. Для начала создаем файл шаблона `login.html` в котором пишем код
``` 
{% extends 'base.html' %}

{% block title %}Авторизация{% endblock %}

{% block content %}
    <h1>Авторизация</h1>
    <form method="POST">
        {% csrf_token %}
        <div>
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Войти</button>
    </form>
    <p>Еще нет аккаунта? <a href="{% url 'register' %}">Зарегистрируйтесь</a></p>
{% endblock %}

```
29. Далее создаем шаблон для страницы регистрации нового пользователя, для этого создаем файл `register.html` и в самом файле прописываем код:
``` 
{% extends 'base.html' %}

{% block title %}Регистрация{% endblock %}

{% block content %}
    <h1>Регистрация</h1>
    <form method="POST">
        {% csrf_token %}
        <div>
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <label for="password2">Подтвердите пароль:</label>
            <input type="password" id="password2" name="password2" required>
        </div>
        <button type="submit">Зарегистрироваться</button>
    </form>
{% endblock %}

```
30. Теперь создаем шаблон для страницы личного кабинета пользователя, который не обладает правами администратора или суперюзера. Для этого создаем файл `profile.html` в котором прописываем код:
``` 
{% extends 'base.html' %}

{% block title %}Личный кабинет{% endblock %}

{% block content %}
    <h1>Личный кабинет</h1>
    <p>Добро пожаловать, {{ user.username }}!</p>
    <p>Здесь вы можете просматривать свою информацию и изменять настройки профиля.</p>
    <p><a href="{% url 'logout' %}">Выйти</a></p>
{% endblock %}

```
31. Чтобы система увидела новые шаблоны, необходимо дополнить файл `urls.py` строчками кода:
``` 
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    # Другие маршруты...
]
```
так же следует дополнить файл `views.py` следующим кодом:
``` 
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def profile_view(request):
    return render(request, 'profile.html')
```
 На этом этапе формы еще ничего не могут, это пока только болванки с полями и кнопками. Кроме того форма профиля может выдавать ошибку ругаясь на строку кода `<p><a href="{% url 'logout' %}">Выйти</a></p>`. Чтобы просмотреть профиль, нужно на время просто удалить эту строку.
 32. Теперь нужно реализовть полноценнный функционал по регистрации пользователя. Для этого создадим форму регистрации, используя Django Form API. Форма будет включать поля для имени пользователя, email и пароля.
Создадим файл `forms.py` в приложении и пропишем следующий код:
``` 
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        """Проверка совпадения двух паролей."""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_email(self):
        """Проверка уникальности email."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
 
```
33. Настройка представления для регистрации

В представлении обработаем данные формы, создадим нового пользователя и перенаправим на страницу авторизации после успешной регистрации.
Обновим `views.py` для обработки регистрации
``` 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя, но не сохраняем пароль напрямую
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            # Можно автоматически логинить пользователя после регистрации
            # login(request, new_user)

            # Переадресация на страницу авторизации
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

```
34. Изменение шаблона register.html

Теперь изменим шаблон register.html, чтобы он использовал форму UserRegistrationForm и отобразил поле для email.
Обновленный шаблон register.html
``` 
{% extends 'base.html' %}

{% block title %}Регистрация{% endblock %}

{% block content %}
    <h1>Регистрация</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Зарегистрироваться</button>
    </form>
    <p>Уже есть аккаунт? <a href="{% url 'login' %}">Войдите</a></p>
{% endblock %}

```
35. Обновление URL-адресов

Обновить маршрут для страницы регистрации в urls.py.
``` 
urlpatterns = [
    path('register/', views.register_view, name='register'),
    # Другие маршруты...
]
```
36. Теперь нужно реализовать функцию авторизации зарегистрированного пользователя. Начать можно с создания представления для авторизации

Мы будем использовать функцию authenticate и login из Django для обработки авторизации. Функция authenticate проверяет данные пользователя, а login — авторизует его.
Для этого необходимо обновить файл `views.py`:
``` 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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

```
37. Обновление шаблона авторизации

Далее необходимо обновить шаблон авторизации, чтобы он мог отображать сообщение об ошибке в случае неудачной попытки входа (например, если логин или пароль введены неправильно).
Добавляю в шаблон `login.html` следующий код
``` 
{% extends 'base.html' %}

{% block title %}Авторизация{% endblock %}

{% block content %}
    <h1>Авторизация</h1>

    <!-- Отображение сообщения об ошибке, если введены неверные данные -->
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}

    <form method="POST">
        {% csrf_token %}
        <div>
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Войти</button>
    </form>

    <p>Еще нет аккаунта? <a href="{% url 'register' %}">Зарегистрируйтесь</a></p>
{% endblock %}

```
38. Создадим формы для редактирования профиля и смены пароля
Форма редактирования профиля

В `forms.py` создадим форму, которая позволит пользователю изменять его личные данные (имя, фамилия, email). Мы будем использовать встроенную модель `User` в Django.
``` 
from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Email обязательно для заполнения
```
39. Обновим представление `profile_view` для обработки обеих форм

Теперь мы создадим представление, которое будет обрабатывать как редактирование профиля, так и смену пароля.
Необходимо внести изменения в файл `views.py`
``` 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Обработка формы профиля
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Чтобы пользователь не был разлогинен после смены пароля
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

```
40. Обновление шаблона `profile.html`

Теперь обновим шаблон для отображения форм редактирования профиля и смены пароля.
Обновлённый `profile.html`:
``` 
{% extends 'base.html' %}

{% block title %}Личный кабинет{% endblock %}

{% block content %}
    <h1>Личный кабинет</h1>
    <p>Добро пожаловать, {{ user.username }}!</p>

    <!-- Форма для редактирования профиля -->
    <h2>Редактирование профиля</h2>
    <form method="POST">
        {% csrf_token %}
        {{ profile_form.as_p }}
        <button type="submit" name="update_profile">Обновить профиль</button>
    </form>

    <!-- Форма для смены пароля -->
    <h2>Изменить пароль</h2>
    <form method="POST">
        {% csrf_token %}
        {{ password_form.as_p }}
        <button type="submit" name="change_password">Изменить пароль</button>
    </form>

    <!-- Форма для выхода из аккаунта -->
    <h2>Выйти</h2>
    <form method="POST" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">Выйти</button>
    </form>

{% endblock %}

```
41. Настройка URL для выхода из профиля. 
Пользователю может потребоваться необходимость выйти со своей учетной записи, поэтому нужно дополнительно реализовать функцию выхода с учетной записи.
Прописываем в файл `urls.py` следующий код:
``` 
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Другие маршруты...
]

```
42. Теперь нужно настроить редирект, который будет отправлять пользователя на главную страницу сайта, после того как пользователь выйдет со своей учетной записи.
Чтобы после разлогинивания пользователь автоматически перенаправлялся на главную страницу, можем указать это в настройках `settings.py`:
``` 
LOGOUT_REDIRECT_URL = 'start_page'
```
43. У нас есть теперь функции авторизации, регистрации, входа в личный кабинет и выхода, но на сайте это нигде явно не указано. Пользователь не может знать что нужно вписать в адресной строке браузера, чтобы попасть в нужное место. Для этого необходимо в меню сайта добавить кнопку для авторизации на сайте. Кроме того, необходимо сделать так, чтобы пользователь понимал, что он авторизован. Я решил сделать так, что после авторизации кнопка в меню "Войти" сменяется на никнэйм пользователя. При этом никнэйм превращается в выпадающее меню. В данном меню будет два пункта, вход в личный кабинет и выход с сайта. Реализовать это было решено через стили CSS непосредственно в коде самого шаблона.
При этом еще дополнительно улучшил визуальный стиль сайта, задав для всего контента поле в 1200 пикселей.
``` 
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мониторинг цен{% endblock %}</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }

        /* Общий контейнер для сайта */
        .container {
            max-width: 1200px; /* Ширина сайта 1200px */
            margin: 0 auto;  /* Центрирование сайта, с пустым пространством слева и справа */
        }

        .banner {
            width: 1200px;
            height: 150px;
            background-image: url("{% static 'core/images/banner2.jpg' %}");
            background-size: cover;
            max-width: 100%;
        }

        .banner-container {
            display: flex;
            justify-content: center; /* Центрирование по горизонтали */
        }

        .menu {
            background-color: #add8e6; /* Светло-голубой фон */
            padding: 10px;
            margin-top: 20px;
            border-radius: 5px; /* Слегка закругленные углы */
            display: flex;
            justify-content: center; /* Центрирование по горизонтали */
            align-items: center;
        }

        .menu a {
            margin: 0 15px;
            text-decoration: none;
            color: black;
            font-size: 18px;
        }

        .menu a:hover {
            text-decoration: underline;
        }

        .auth-button {
            margin-left: auto;  /* Отодвигает кнопку авторизации в конец меню */
            position: relative;  /* Для позиционирования выпадающего меню */
        }

        .user-icon {
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
        }

        /* Стили для выпадающего меню */
        .dropdown-menu {
            display: none;  /* По умолчанию скрыто */
            flex-direction: column;
            position: absolute;
            top: 100%;
            right: 0;
            background-color: #fff;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
            z-index: 1;
            min-width: 150px;
            padding: 5px;
            border-radius: 5px;
            text-align: left; /* Выровняем текст влево */
        }

        .auth-button:hover .dropdown-menu {
            display: block;  /* Показываем при наведении */
        }

        .dropdown-menu a, .dropdown-menu form {
            display: block;
            padding: 5px 0;
            color: black;
            text-decoration: none;
            font-size: 16px;  /* Устанавливаем одинаковый размер шрифта */
            text-align: left;  /* Выравниваем текст по левому краю */
        }

        .dropdown-menu a:hover, .dropdown-menu form button:hover {
            text-decoration: underline;
        }

        .dropdown-menu form button {
            border: none;
            background: none;
            padding: 0;
            font-size: 16px;
            color: black;
            cursor: pointer;
            text-align: left;  /* Выравниваем текст по левому краю */
        }
    </style>
</head>
<body>
    <div class="banner-container">
        <div class="banner"></div>
    </div>

    <!-- Основной контейнер сайта с шириной 1200px -->
    <div class="container">
        <div class="menu">
            <a href="{% url 'start_page' %}">Главная</a>
            <a href="{% url 'price_add' %}">Добавить цены</a>
            <a href="{% url 'statistics' %}">Статистика</a>
            <a href="{% url 'about_us' %}">О нас</a>

            <!-- Кнопка авторизации или личного кабинета -->
            <div class="auth-button">
                {% if user.is_authenticated %}
                    <a href="#">
                        <img src="{% static 'core/images/user.png' %}" alt="Пользователь" class="user-icon">
                        {{ user.username }}
                    </a>

                    <!-- Выпадающее меню -->
                    <div class="dropdown-menu">
                        <a href="{% url 'profile' %}">Профиль</a>
                        <form method="POST" action="{% url 'logout' %}">
                            {% csrf_token %}
                         <div> &nbsp;&nbsp;  <button type="submit">Выйти</button></div>
                        </form>
                    </div>
                {% else %}
                    <a href="{% url 'login' %}">Войти</a>
                {% endif %}
            </div>
        </div>

        <div class="content">
            {% block content %}
            <!-- Контент страниц -->
            {% endblock %}
        </div>
    </div>
</body>
</html>

```