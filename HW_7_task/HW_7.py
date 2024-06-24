# Импорт необходимых библиотек
from selenium import webdriver  # Для управления веб-драйвером
from selenium.webdriver.chrome.options import Options  # Для настройки опций Chrome
from selenium.webdriver.common.by import By  # Для определения способа поиска элементов
from selenium.webdriver.support.ui import WebDriverWait  # Для ожидания загрузки элементов
from selenium.webdriver.support import expected_conditions as EC  # Для ожидания конкретных условий
import time  # Для задержки выполнения
import json  # Для работы с JSON

# Настройка User-Agent для WebDriver
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
chrome_options = Options()
# Установка User-Agent в опции браузера
chrome_options.add_argument(f'user-agent={user_agent}')

# Инициализация драйвера Chrome с заданными опциями
driver = webdriver.Chrome(options=chrome_options)

# URL сайта для скрапинга
books_url = "https://books.toscrape.com/"

try:
    # Переход по указанному URL
    driver.get(books_url)

    # Ожидание загрузки страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Скроллинг страницы для загрузки контента (можно также использовать другие методы скроллинга)
    page_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_pause_time = 2
    while True:
        # Прокрутка до конца страницы
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_pause_time)
        # Проверка, достигнут ли конец страницы
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == page_height:
            break
        page_height = new_height

    # Дополнительное ожидание после скроллинга страницы
    time.sleep(5)

    # Поиск заголовков книг и их цен
    books = driver.find_elements(By.XPATH, "//article[@class='product_pod']")
    
    # Отладочное сообщение для проверки количества найденных книг
    print(f"Найдено книг: {len(books)}")

    # Сбор данных о книгах
    books_data = []
    for book in books:
        try:
            title_element = book.find_element(By.XPATH, ".//h3/a")
            price_element = book.find_element(By.XPATH, ".//div[@class='product_price']/p[@class='price_color']")

            title = title_element.get_attribute("title")
            price = price_element.text

            # Отладочное сообщение для проверки извлеченных данных
            print(f"Название: {title}, Цена: {price}")

            books_data.append({"title": title, "price": price})
        except Exception as e:
            print("Произошла ошибка при извлечении данных:", e)

    # Запись данных в файл JSON
    with open('books_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_data, json_file, ensure_ascii=False, indent=4)

    # Вывод сообщения об успешном сохранении
    print("Данные сохранены в файл 'books_data.json'")

except Exception as e:
    # Вывод сообщения об ошибке
    print("Произошла ошибка:", e)

finally:
    # Закрытие драйвера браузера
    driver.quit()
