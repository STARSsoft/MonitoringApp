# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Price(models.Model):
    ID_product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Продукт
    ID_region = models.ForeignKey('Region', on_delete=models.CASCADE)  # Регион
    quantity = models.FloatField()  # Количество
    ID_measure = models.ForeignKey('UnitOfMeasurement', on_delete=models.CASCADE)  # Единица измерения
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь
    date = models.DateTimeField(default=timezone.now)  # Дата
    years_norm = models.FloatField()  # Годовые нормы потребления
    price_for_kg = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за кг
    price_for_year = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за год
    price_for_month = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за месяц

    class Meta:
        db_table = 'mp_prices_all'  # Привязка к существующей таблице

    def __str__(self):
        return f"Цена для {self.ID_product} в {self.ID_region}"

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
