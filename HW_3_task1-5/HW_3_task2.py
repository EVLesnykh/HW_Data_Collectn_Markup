import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Создание базы данных и коллекции
db = client['books_Scrape']
collection = db['books']

# Чтение файла JSON
with open('C:\\Users\\Андрей\\Desktop\\git_education\\HW_Data_Collectn_Markup\\HW_3_task1-5\\books.json', 'r') as file:
    data = json.load(file) 

# Вставка данных в коллекцию MongoDB
collection.insert_many(data)
print("Данные с 5-ти первых страниц сайта успешно загружены")
  
# Закрытие соединения с MongoDB
print(f'В коллекции {collection.name} теперь {collection.count_documents({})} книг ')
