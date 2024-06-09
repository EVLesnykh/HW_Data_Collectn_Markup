from pymongo import MongoClient

client = MongoClient()

db = client['books_Scrape']
collection = db['books']

# Поиск книги по названию и вывод всей информации о ней:
book_by_name = collection.find_one({'name': 'The Black Maria'})
print(book_by_name)

# Подсчет количества книг, цена которых  больше 30 фунтов:
price_filter = {'price': {'$gt': 30}}
count_price = collection.count_documents(price_filter)
print(f'Количество книг, цена которых больше 30 фунтов: {count_price}')

# Расчет общей стоимости всех книг в БД:
pipeline = [
    {
        '$group': {
            '_id': None, 
            'total': {
                '$sum': '$price'
            }
        }
    }
]

result = collection.aggregate(pipeline)

total_sum = 0
for doc in result:
    total_sum = doc['total']
    
print(f'Общая стоимость всех книг в коллекции: {total_sum}')