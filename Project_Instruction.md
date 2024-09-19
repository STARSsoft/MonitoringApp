# Инструкция по созданию и работе над проектом.

1. Начать новый проект и "подружить" его с GitHub.
2. Обновить приложение pip `pip install --upgrade pip`
3. Установить Джанго `pip install django`
4. Создаем проект `django-admin startproject monitoringapp`
5. Переходим в папку проекта `cd monitoringapp`
6. Запускаем MySQL командой `mysql -u root -p`
7. Ввести пароль БД `admin1977`
8. Запустить приложение  **MySQL Workbench**
9. В приложении создаем таблицу в БД для проекта
10. Переходим в PyCharm, в папке с проектом находим файл **settings.py**

    в файле находим раздел с Базой данных и вставляем код

`
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
`
11. Устанавливаем клиент MySQL в Джанго `pip install django mysqlclient
`
12. Создаем базовые таблицы Джанго `python manage.py migrate`
13. 