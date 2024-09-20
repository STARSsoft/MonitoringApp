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
25. 