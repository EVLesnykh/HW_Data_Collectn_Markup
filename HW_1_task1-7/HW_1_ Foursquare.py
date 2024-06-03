import requests
import json
import logging

# Ваши учетные данные API
client_id = ""
client_secret = ""

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"
city = input('Введите название города: ')
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": "cinema"
}
headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

# Отправка запроса API и получение ответа
try:
    response = requests.get(endpoint, params=params, headers=headers)

    # Проверка успешности запроса API
    logging.info(f"Статус запроса: {response.status_code}")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        try:
            print("Название:", venue["name"])
            print("Адрес:", venue["location"]["address"])
            if "rating" in venue:
                print("Рейтинг:", venue["rating"])
            else:
                print("Рейтинг: не обнаружен")
            print("\n")
        except Exception as e:
            logging.error(e)
except Exception as e:
    logging.error(e)
    