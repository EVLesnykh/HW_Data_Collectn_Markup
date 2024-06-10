import requests  # библиотека для выполнения HTTP-запросов
from lxml import html  # библиотека для парсинга HTML
import pandas as pd  # библиотека для обработки и анализа данных в Python

# Целевой URL, откуда будут скрейпиться данные
url = 'https://finance.yahoo.com/trending-tickers/'

# Функция для скрейпинга табличных данных одной страницы
def scrape_page_data(url):
    # Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

    # Создаем объект дерева HTML из содержимого ответа
    tree = html.fromstring(response.content)

    # Используем XPath для выбора всех строк таблицы с классом 'W(100%)'
    table_rows = tree.xpath("//table[@class='W(100%)']/tbody/tr")

    # Создаем пустой список для хранения данных
    data_list = []

    # Итерируемся по строкам таблицы и извлекаем необходимые данные
    for row in table_rows:
        columns = row.xpath(".//td/text()")
        data = {
            'Symbol': row.xpath(".//td[1]/a/text()")[0].strip(),  # Извлекаем и очищаем значение столбца 'Symbol'
            'Name': columns[0].strip(),  # Извлекаем и очищаем значение столбца 'Name'
            'Last_price': row.xpath(".//td[3]/fin-streamer/text()")[0].strip(),  # Извлекаем и очищаем значение столбца 'Last_price'
            'Marker_time': row.xpath(".//td[4]/fin-streamer/text()")[0].strip(),  # Извлекаем и очищаем значение столбца 'Marker_time'
            'Change': row.xpath(".//td[5]/fin-streamer/span/text()")[0].strip(),  # Извлекаем и очищаем значение столбца 'Change'
            '%Change': row.xpath(".//td[6]/fin-streamer/span/text()")[0].strip(),  # Извлекаем и очищаем значение столбца '%Change'
            'Volume': row.xpath(".//td[7]/fin-streamer/text()")[0].strip(),  # Извлекаем и очищаем значение столбца 'Volume'
            'Marker_Cap': ''.join(row.xpath(".//td[8]/text()")).strip() if row.xpath(".//td[8]/text()") else 'нет данных'  # Извлекаем и очищаем значение столбца 'Marker_Cap'
        }
        data_list.append(data)
    
    for i in data_list:
        print(i)

    # Создание DataFrame
    df = pd.DataFrame(data_list)

    # Получение данных
    data_list = scrape_page_data(url)

    # Создание DataFrame
    df = pd.DataFrame(data_list)

    # Путь к файлу CSV
    csv_file_path = "HW_4_task_table.csv"

    # Запись DataFrame в файл CSV
    df.to_csv(csv_file_path, index=False)

    print("Данные записаны в файл под именем HW_4_task_table.csv")
