# MonitoringApp
## Пошаговые действия по созданию и работе над проектом.

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
25. Поскольку все страницы сайта будут иметь единый дизайн, то каждая страница по сути кроме необходимого контента будет иметь один и тот же html код, а это лишний трафик. Поэтому было принято решение, создать базовый шаблон и внутри каждой страницы прописать код, который будет наследовать шаблон дизайна из базового файла. Для этого был создан файл `base.html` в котором прописали следующий код:

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
38. Создадим формы для редактирования профиля и смены пароля.
Форма редактирования профиля. 
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
39. Обновим представление `profile_view` для обработки обеих форм.
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
40. Обновление шаблона `profile.html`.
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
44. После выхода из своей учетной записи, пользователь может явно или случайно пройти по ссылке ведущей в личный кабинет, но поскольку пользователь не авторизован, то выходит встроенная в Джанго проверка с ошибкой о том что запрашиваемый ресурс не найден. Я же хочу реализовать функцию, которая перенаправит пользователя на другую страницу, которая сохранит общий стиль сайта, но при этом уведомит пользователя, что он пытается получить доступ в ту часть сайта, где необходима авторизация.
Создание шаблона для неавторизованных пользователей. 
Создаю новый файл шаблона `login_required.html`, в который добавлю сообщение для пользователей, которые пытаются попасть в "Профиль" без авторизации.
В `templates/login_required.html` добавляю следующий код:
``` 
{% extends 'base.html' %}

{% block title %}Требуется авторизация{% endblock %}

{% block content %}
    <h1>Требуется авторизация</h1>
    <p>Данный раздел доступен только авторизованным пользователям. Зарегистрируйтесь и/или войдите на сайт, чтобы просматривать эту страницу.</p>
    <p>
        <a href="{% url 'login' %}">Войти</a> или 
        <a href="{% url 'register' %}">Зарегистрироваться</a>
    </p>
{% endblock %}

```
45. Далее нужно создать непосредственно функцию перенаправления на созданный шаблон. В файле `views.py` пишем код:
``` 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

```
46. Далее нужно настроить маршруты на новый шаблон для новой страницы, на которую будут перенаправляться неавторизованные пользователи. Для этого добавим немного кода в файл `urls.py`:

``` 
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('login-required/', views.login_required_view, name='login_required'),
    # Другие маршруты...
]
```
47. Ну и чтобы вся эта настройка заработала и дополнительно чтобы другие защищенные страницы также перенаправляли на эту страницу, нужно в настройках проекта указать, в файле `settings.py`:

``` 
LOGIN_URL = 'login_required'  # Страница, на которую перенаправляются неавторизованные пользователи
```
48. Поскольку в проекте подразумевается, что цены будут вносить только авторизованные пользователи, то необходимо прикрутить функцию переадресации для неавторизованных пользователей к странице ввода цен. Для этого в файле views.py добавим короткий код с декоратором:

``` 
@login_required(login_url='login_required')  # Переадресация на страницу для неавторизованных
def price_add(request):
    return render(request, 'price_add.html') 
```
В других файлах уже больше ничего добавлять не надо, так как мы это сделали еще ранее, когда настраивали переадресацию при входе в личный кабинет.  

49. На текущем этапе, внешний вид форм авторизации, регистрации и личного кабинета, выглядят, мягко сказать, не красиво. Поэтому имеет смысл чуть-чуть улучшить их дизайн.   
Начну с формы авторизации. В базовый шаблон формы `login.html`, вносим следующий код:

``` 
{% extends 'base.html' %}

{% block title %}Авторизация{% endblock %}

{% block content %}
    <h1>Авторизация</h1>

    <!-- Отображение сообщения об ошибке, если введены неверные данные -->
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}

    <form method="POST" class="login-form">
        {% csrf_token %}
        <div class="form-group">
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div class="form-group">
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit" class="login-button">Войти</button>
    </form>

    <p>Еще нет аккаунта? <a href="{% url 'register' %}">Зарегистрируйтесь</a></p>
{% endblock %}
```
50. Добавление стилей.   
Для улучшения дизайна формы, добавим следующие стили прямо в наш базовый шаблон `base.html`, чтобы они применялись ко всем формам авторизации.
Я вставил эти стили в `<style>` внутри `<head>` базового шаблона:
``` 
<style>
    .login-form {
        max-width: 400px;
        margin: 0 auto; /* Центрируем форму на странице */
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .form-group {
        margin-bottom: 20px;  /* Отступ между полями ввода */
        text-align: left;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-size: 16px;  /* Увеличим шрифт */
    }

    .form-group input {
        width: 100%;  /* Поля занимают всю ширину контейнера */
        padding: 10px;
        font-size: 16px;  /* Увеличим шрифт для удобства */
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;  /* Чтобы padding не влиял на ширину */
    }

    .login-button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        background-color: #add8e6;  /* Светло голубой цвет кнопки */
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .login-button:hover {
        background-color: #3543de; /* Синий цвет кнопки при наведении */
    }

    /* Для отступов внизу и центре */
    .login-form h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }

    .login-form p {
        margin-top: 20px;
        text-align: center;
    }

    /* Для отображения ошибок */
    .login-form p.error {
        color: red;
        text-align: center;
    }
</style>

```
Что изменилось:
*    Размер полей: Поля для ввода username и password занимают всю ширину контейнера (100%), имеют padding для большего пространства и шрифт 16px.
*    Отступы: Добавлены отступы между полями ввода и кнопкой — 20px через класс .form-group.
*    Кнопка "Войти": Стала занимать всю ширину контейнера, имеет padding для увеличения высоты, увеличен шрифт, и добавлены стили для hover-эффекта.
*    Центрирование формы: Форма центрирована по странице через margin: 0 auto, чтобы она выглядела аккуратно.
*    Оформление заголовка: Заголовок "Авторизация" центрирован и отделён от формы дополнительным отступом.
*    Сообщение об ошибке: Ошибки, если они есть, отображаются в центре страницы с красным цветом.

51. Теперь сделаем то же самое для формы регистрации. В шаблоне формы `register.html` меняем код:

``` 
{% extends 'base.html' %}

{% block title %}Регистрация{% endblock %}

{% block content %}
    <h1>Регистрация</h1>
    <form method="POST" class="registration-form">
        {% csrf_token %}
        {{ form.as_p }}  <!-- Используем стандартный вывод полей формы -->
        <button type="submit" class="register-button">Зарегистрироваться</button>
    </form>
    <p>Уже есть аккаунт? <a href="{% url 'login' %}">Войдите</a></p>
{% endblock %}
```
52. Так же добавляем стили для формы в базовый шаблон:

``` 
    .registration-form {
        max-width: 400px;
        margin: 0 auto; /* Центрируем форму на странице */
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .registration-form .form-group {
        margin-bottom: 20px;  /* Отступ между полями ввода */
        text-align: left;
    }

    .registration-form label {
        display: block;
        margin-bottom: 8px;
        font-size: 16px;  /* Увеличим шрифт */
    }

    .registration-form input {
        width: 100%;  /* Поля занимают всю ширину контейнера */
        padding: 10px;
        font-size: 16px;  /* Увеличим шрифт для удобства */
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;  /* Чтобы padding не влиял на ширину */
    }

    .register-button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        background-color: #add8e6;  /* Светло-голубой цвет кнопки */
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .register-button:hover {
        background-color: #3543de; /* Синий цвет кнопки при наведении */
    }

    /* Для отступов внизу и центре */
    .registration-form h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }

    .registration-form p {
        margin-top: 20px;
        text-align: left;
    }

    /* Для отображения ошибок */
    .registration-form p.error {
        color: red;
        text-align: center;
    }
```
Теперь форма выглядит так же как и форма авторизации.

53. Осталось точно так же подогнать под единый стиль форму Личного кабинета. Меняем шаблон формы `profile.html`:

``` 
{% extends 'base.html' %}

{% block title %}Профиль{% endblock %}

{% block content %}
    <h1>Профиль</h1>

    <!-- Форма для редактирования профиля -->
    <form method="POST" class="profile-form">
        {% csrf_token %}
        {{ profile_form.as_p }}
        <button type="submit" name="update_profile" class="save-button">Сохранить изменения</button>
    </form>

    <!-- Форма для смены пароля -->
    <h2>Изменить пароль</h2>
    <form method="POST" class="password-form">
        {% csrf_token %}
        {{ password_form.as_p }}
        <button type="submit" name="change_password" class="save-button">Изменить пароль</button>
    </form>
{% endblock %}
```
54. Так же в базовый шаблон добавляем стили:

``` 
<style>
    /* Стили для формы профиля и смены пароля */
    .profile-form, .password-form {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 40px;
    }

    /* Заголовки по центру */
    .profile-form h1, .password-form h2 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }

    /* Лейблы и текст внутри форм по левому краю */
    .profile-form .form-group, .password-form .form-group {
        margin-bottom: 20px;
        text-align: left;
    }

    .profile-form label, .password-form label {
        display: block;
        margin-bottom: 8px;
        font-size: 16px;
        text-align: left;
    }

    .profile-form input, .password-form input {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    /* Выровняем маркированные списки по левому краю */
    .password-form ul {
        padding-left: 20px;  /* Отступ для маркированного списка */
        text-align: left;     /* Выравниваем текст внутри списка по левому краю */
        list-style: disc;     /* Убедимся, что используется маркированный стиль списка */
    }

    .password-form ul li {
        margin-bottom: 10px;  /* Отступ между элементами списка */
    }

    /* Кнопки по центру */
    .save-button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        background-color: #add8e6;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-align: center;
    }

    .save-button:hover {
        background-color: #3543de;
    }
</style>
```
55. В ходе разработки, была протестирована страница личного кабинета и выяснилось, что форма не записывает обновленные данные в базу данных. Поэтому в файл представлений `views.py` были внесены некоторые изменения для формы личного кабинета:

``` 
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
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()  # Сохраняем новый пароль
                update_session_auth_hash(request, user)  # Обновляем сессию, чтобы не разлогинило
                return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
```
56. Необходимо подготовить сайт к локализации. Для этого во всех шаблонах, где явно вносится текст на русском языке нужно внести изменения. 
Внесенные изменения на примере файла `about_us.html`:

``` 
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "О нас" %}{% endblock %}

{% block content %}
    <H1>{% trans "Страница с информацией о нас" %}</H1>
{% endblock %}

```
В каждом шаблоне загружаем модуль `{% load i18n %}` который отвечает за локализацию. Так же во всех тегах, где есть выводимый в браузере текст, ставим модули перевода `{% trans "Тут любой текст" %}`  

57. Когда все файлы подготовлены к локализации, необходимо скомпилировать файлы переводов.  
Для этого в терминале вводим команды:

``` 
django-admin makemessages -l ru
django-admin makemessages -l en
django-admin makemessages -l kk
```
Django создаст файлы перевода формата .po в папке locale  

58. В файлах django.po нужно перевести на соответсвующий язык все строки, которые система смогла найти на сайте.  
Например:

``` 
#: monitoringapp/core/views.py:91 monitoringapp/templates/start_page.html:4
msgid "Главная страница"
msgstr "Home Page"
```
59. После того как все переводы сделаны, нужно ввести в терминале команду:
``` 
django-admin compilemessages
```
В папке locale скомпилируются новые файлы переводов с расширением .mo  

60. Чтобы пользователи могли переключать языки, нужно вывести соответствующий инструмент на сайт. В базовый шаблон в разделе с меню добавляю следующий код:

``` 
<form action="{% url 'set_language' %}" method="post" style="margin-left: 20px;">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ request.path }}">
        <select name="language" onchange="this.form.submit()" style="padding: 5px; font-size: 16px;">
            <option value="ru" {% if request.LANGUAGE_CODE == 'ru' %}selected{% endif %}>Русский</option>
            <option value="en" {% if request.LANGUAGE_CODE == 'en' %}selected{% endif %}>English</option>
            <option value="kk" {% if request.LANGUAGE_CODE == 'kk' %}selected{% endif %}>Қазақша</option>
        </select>
</form>
```
61. Так же важно определить новые пути до всех файлов проекта. Поэтому вносим изменения в файл urls.py, который находится в папке monitoringapp, а не в папке core:
``` 
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
```
62. Ну и самое главное, в настройках сайта, в файле settings.py нужно внести следующие изменения:
``` 
from django.utils.translation import gettext_lazy as _

# Язык по умолчанию
LANGUAGE_CODE = 'ru'  # По умолчанию русский

# Поддерживаемые языки
LANGUAGES = [
    ('ru', _('Русский')),
    ('en', _('English')),
    ('kk', _('Қазақша')),
]

USE_I18N = True  # Включаем интернационализацию (i18n)
USE_L10N = True  # Включаем локализацию
USE_TZ = True  # Часовые пояса

# Путь для хранения файлов локализации
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Путь для файлов перевода
]

```
Это настройки, которые задают язык для сайта по умолчанию, включают поддерживаемые языки, включают функционал локализации и прописывают путь до файлов локализации.

Так же в этом же файле необходимо дополнить раздел с middleware
``` 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Часть которая отвечает за локализацию
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
63. Базовый функционал сайта настроен. По мере наполнения сайта контентом, необходимо будет проводить операции по локализации контента. 
Теперь, наступила пора перейти к настройке главной части, то ради чего задумывался весь сайт.
Для начала необходимо настроить форму внесения цен на продукты питания пользователями. Задумывается два варианта внесения цен: единичный и списком.   
Настраиваем первый вариант внесения цен - единичный. Суть формы, когда пользователь выбирает только один товар, добавляет на него цену и отправляет в базу данных.
Данная форма будет иметь возможность не только загружать списки необходимых данных из БД, но и предлагать пользователю единицу измерения на продукт по умолчанию и в выпадающем списке предлагать только те единицы измерения, которые подходят для данного типа продуктов, чтобы пользователи намеренно или случайно не выбрали например для картошки, единицу измерения бутылка. Для реализации динамической подстановки данных, придется прибегнуть к JavaScript и Ajax.  
Создаем форму шаблона:
``` 
{% extends 'base.html' %}
{% load i18n %}

{% block title %}{% trans "Добавить цены" %}{% endblock %}

{% block content %}
    <h1>{% trans "Добавить цены" %}</h1>
    <form id="price-form" method="POST" class="styled-form">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="save-button">{% trans "Сохранить" %}</button>
    </form>

    <br/>
    <h2><a href="{% url 'price_add_list' %}">{% trans "Внести цены списком" %}</a></h2>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const productSelect = document.querySelector('#id_ID_product');
            const measureSelect = document.querySelector('#id_ID_measure');
            const form = document.querySelector('#price-form');

            // Функция для обновления единиц измерения
            function updateMeasurements(measures, defaultMeasure) {
                measureSelect.innerHTML = '';

                measures.forEach(measure => {
                    const option = document.createElement('option');
                    option.value = measure.id;
                    option.textContent = measure.name;
                    if (measure.id === defaultMeasure) {
                        option.selected = true;
                    }
                    measureSelect.appendChild(option);
                });
            }

            // Обработка изменения продукта
            productSelect.addEventListener('change', function () {
                const productId = this.value;
                const url = `{% url 'get_measurements' 0 %}`.replace('0', productId);

                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        if (data.measures) {
                            updateMeasurements(data.measures, data.default_measure);
                        }
                    })
                    .catch(error => console.error('Error fetching measurements:', error));
            });

            // Обработка отправки формы через Ajax
            form.addEventListener('submit', function (event) {
                event.preventDefault();

                const formData = new FormData(form);

                fetch("{% url 'price_add' %}", {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Цена успешно сохранена!');
                            window.location.href = "{% url 'thanks' %}";
                        } else if (data.status === 'error') {
                            alert('Ошибка при сохранении цены: ' + JSON.stringify(data.errors));
                        }
                    })
                    .catch(error => console.error('Error submitting form:', error));
            });
        });
    </script>
{% endblock %}

```
64. Чтобы форма была выполнена в едином стиле с остальными формами сайт, добавляем в базовый шаблон настройки CSS стилей:

``` 
/* Стили для формы добавления цен */
.styled-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.styled-form label {
    display: block;
    margin-bottom: 5px;
    font-size: 16px;
    text-align: left;
}

.styled-form input {
    width: 97%;
    padding: 5px;
    margin-bottom: 7px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.styled-form select {
    width: 100%;
    padding: 10px;
    margin-bottom: 7px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.styled-form button {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    background-color: #add8e6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.styled-form button:hover {
    background-color: #3543de;
}
```
65. Создаю модель формы в файле 'models.py'

``` 
# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Модель для продуктов
class Product(models.Model):
    ID_product = models.AutoField(primary_key=True)  # Явный первичный ключ
    product_KZ = models.CharField(max_length=255)
    product_RU = models.CharField(max_length=255)
    product_EN = models.CharField(max_length=255)
    measure_1 = models.BooleanField(default=False)  # Соответствует ID 1
    measure_2 = models.BooleanField(default=False)  # Соответствует ID 2
    measure_3 = models.BooleanField(default=False)  # И так далее...
    measure_4 = models.BooleanField(default=False)
    measure_5 = models.BooleanField(default=False)
    measure_6 = models.BooleanField(default=False)
    measure_7 = models.BooleanField(default=False)
    measure_8 = models.BooleanField(default=False)
    measure_default = models.PositiveIntegerField()  # Значение от 1 до 8
    years_norm = models.FloatField()

    class Meta:
        db_table = 'mp_products'  # Привязка к существующей таблице

    def __str__(self):
        return self.product_RU  # Выводим название продукта на русском

# Модель для регионов
class Region(models.Model):
    ID_region = models.AutoField(primary_key=True)  # Явный первичный ключ
    region_KZ = models.CharField(max_length=255)
    region_RU = models.CharField(max_length=255)
    region_EN = models.CharField(max_length=255)

    class Meta:
        db_table = 'mp_regions'  # Привязка к существующей таблице

    def __str__(self):
        return self.region_RU  # Выводим название региона на русском

# Модель для единиц измерения
class UnitOfMeasurement(models.Model):
    ID_unit = models.AutoField(primary_key=True)  # Явный первичный ключ
    name_unit_KZ = models.CharField(max_length=255)
    name_unit_RU = models.CharField(max_length=255)
    name_unit_EN = models.CharField(max_length=255)

    class Meta:
        db_table = 'mp_unit_of_measurement'  # Привязка к существующей таблице

    def __str__(self):
        return self.name_unit_RU  # Выводим название единицы измерения на русском
```
Данная модель загружает из базы данных все данные для заполнения формы, которые пользователь видит в выпадающих списках.

66. Но прежде чем пользователь сможет заносить данные, нужно создать представление формы, где будут загружаться из базы данных наименование региона, продукта и единицы измерения.  
Файл 'views.py'

``` 

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


def get_measurements(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        measures = []

        if product.measure_1:
            measures.append({'id': 1, 'name': 'Килограмм'})
        if product.measure_2:
            measures.append({'id': 2, 'name': 'Грамм'})
        if product.measure_3:
            measures.append({'id': 3, 'name': 'Штук'})
        if product.measure_4:
            measures.append({'id': 4, 'name': 'Пучок'})
        if product.measure_5:
            measures.append({'id': 5, 'name': 'Упаковка'})
        if product.measure_6:
            measures.append({'id': 6, 'name': 'Булка'})
        if product.measure_7:
            measures.append({'id': 7, 'name': 'Литр'})
        if product.measure_8:
            measures.append({'id': 8, 'name': 'Бутылка'})

        default_measure = product.measure_default

        return JsonResponse({
            'measures': measures,
            'default_measure': default_measure
        })

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


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

def price_add_list(request):
    # Здесь логика для добавления цен списком
    return render(request, 'price_add_list.html')  # Позже доработать шаблон price_add_list.html
```
Тут форма передает такие данные как имя пользователя, текущую дату. При этом при отправке данных в базу данных, проводим пересчет полученных данных в килограммы, с учетом годовых норм потребления продуктов получаем годовые цены на продукт, и в конце пересчитываем это на месячную норму.

Функция 'price_add_list' пока как заглушка. К ней вернемся позже.  

67. Ну и чтобы форма могла не только выбирать из базы данных в выпадающие списки наименование регионов, единиц измерения и наименования продуктов, создадим форму, которая будет подгружать необходимые данные на нужном языке в зависимости от выбранного языка.  
Вносим новые данные в файл 'forms.py'

``` 
from .models import Price, Product, Region, UnitOfMeasurement

 class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['ID_region', 'ID_product', 'ID_measure', 'quantity', 'price']
        labels = {
            'ID_region': _('Регион'),
            'ID_product': _('Продукт'),
            'ID_measure': _('Единица измерения'),
            'quantity': _('Количество'),
            'price': _('Цена'),
        }

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'ru')
        selected_product = kwargs.pop('selected_product', None)
        super().__init__(*args, **kwargs)

        if language == 'kk':
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_KZ
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_KZ
        elif language == 'en':
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_EN
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_EN
        else:
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_RU
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_RU

        if selected_product:
            available_measures = get_available_measures(selected_product)
            self.fields['ID_measure'].queryset = UnitOfMeasurement.objects.filter(
                ID_unit__in=[measure['id'] for measure in available_measures]
            )

```
Как это работает:
> Динамическое обновление единиц измерения: при выборе продукта с помощью JavaScript и Ajax отправляется запрос на сервер, и в ответ сервер возвращает список доступных единиц измерения.
> Сбор данных и отправка через Ajax: все поля формы проверяются на стороне клиента, после чего данные отправляются на сервер для сохранения.
> Обработка результата: сервер обрабатывает данные, возвращает результат сохранения, и в зависимости от него либо отображается сообщение об успехе, либо об ошибке.

Описание работы:
> Когда пользователь выбирает продукт в форме, вызывается функция 'get_measurements' на сервере, которая возвращает список доступных единиц измерения для выбранного продукта.
> После этого JavaScript обновляет выпадающий список единиц измерения на странице.
> Когда пользователь завершает заполнение формы и нажимает кнопку "Сохранить", данные отправляются через Ajax-запрос на сервер.
> Если сервер успешно обработал данные, выводится сообщение об успешном сохранении, а затем происходит перенаправление на страницу благодарности.

68. 
