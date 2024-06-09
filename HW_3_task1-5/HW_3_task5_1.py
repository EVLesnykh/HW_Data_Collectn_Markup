from clickhouse_driver import Client
import json

client = Client('localhost')

def update_database():
    client.execute('CREATE DATABASE IF NOT EXISTS books_Scrapy')
    client.execute('''
    CREATE TABLE IF NOT EXISTS books.info (
        id UInt64,
        name String,
        price Float32,
        availability Int32,
        description String
    ) ENGINE = MergeTree()
    ORDER BY id
    ''')
    with open('C:\\Users\\lesny\\OneDrive\\Рабочий стол\\GIT_EDUCATION\\HW_3_task1_5\\books.json', 'r') as file:
        data = json.load(file)
    insert_query = "INSERT INTO books.info (id, name, price, availability, description) VALUES"
    values = []
    for i in range(len(data)):
        id = i + 1
        name = data[i]['Name']
        price = data[i]['Price']
        availability = data[i]['Availability']
        description = data[i]['Description']
        values.append((id, name, price, availability, description))
    client.execute(insert_query, values)
print("Данные записаны успешно")
