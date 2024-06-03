import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
from pprint import pprint

url = "http://books.toscrape.com/catalogue/"                    
ua = UserAgent()
headers = {"User-Agent": ua.chrome}                               
params ={'page' : 1}
session = requests.session()

all_books = []

while params['page'] <= 5: # Загрузим и соответственно выведим информацию только для 5 страниц из 50
    response = session.get(url + f"page-{params['page']}.html") 
    print(response.status_code)
    if response.status_code != 200:
        break                                                  
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', {'class':'product_pod'})
    
    if not books:
        break
        
    for book in books:
        book_info = {}
        # Скрейпим название, цену, количество товара в наличии, описание:
        # Название
        name_info = book.find('img', {'class':'thumbnail'})
        book_info['name'] = name_info.get('alt')
        # Цена
        price_info = book.find('p', {'class':'price_color'})
        book_info['price'] = float(price_info.getText()[2:])

        # Описание
        url_info = book.find('a', {'title':book_info['name']})
        book_url = url_info.get('href')
        book_response = session.get(url + book_url) 
        if book_response.status_code == 200:
            book_details_soup = BeautifulSoup(book_response.text, 'html.parser')
            # количество книг в наличии
            available_info = int(str(book_details_soup.find('p', {'class': 'instock availability'})).split()[7][1:])
            book_info['available'] = available_info
            # описание
            desc_info = str(book_details_soup.find('p', {'class':None}))
            book_info['description'] = desc_info

        all_books.append(book_info)
    print(f"Пройдена {params['page']} страница")
        
    params['page'] += 1

# Запись данных и сохранение в .json
with open('books.json', 'w') as f:                      
    print(json.dumps(all_books, indent=4), file=f)