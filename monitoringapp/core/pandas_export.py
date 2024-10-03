import pandas as pd
import mysql.connector

# Чтение Excel файла
file_path = '/home/storm/Документы/monitoring/all_products.csv'
df = pd.read_excel(file_path)


# Настройка подключения к MySQL
connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin1977',
    database='pd_monitoringapp'
)

cursor = connection.cursor()

# Перебор строк и добавление данных в MySQL
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO mp_prices_all (ID_product_id, ID_region_id, quantity, ID_measure_id, price, date, years_norm, price_for_kg, price_for_year, price_for_month, username_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Коммит транзакции и закрытие соединения
connection.commit()
cursor.close()
connection.close()
