import scrapy
from trending_tickers_scrapy.items import TrendingTickersScrapyItem

# Класс FinanceSpiderSpider в фреймворке Scrapy
# используется для создания паука (spider), который выполняет 
# сканирование и извлечение данных с веб-сайта
class FinanceSpiderSpider(scrapy.Spider):
    name = "finance_spider" # имя паука
    allowed_domains = ["finance.yahoo.com"] # разрешенный домен для паука 
    start_urls = ["https://finance.yahoo.com/trending-tickers/"]  # точка входа
    
    # Функция для парсинга страницы
    def parse(self, response):
        for row in response.xpath("//table[@class='W(100%)']/tbody/tr"): # извлечение данных из HTML-кода страницы
            symbol = row.xpath(".//td[1]/a/text()").get(default='').strip()
            name = row.xpath(".//td[2]/text()").get(default='').strip()
            last_price = row.xpath(".//td[3]/fin-streamer/text()").get(default='').strip()
            market_time = row.xpath(".//td[4]/fin-streamer/text()").get(default='').strip()
            change = row.xpath(".//td[5]/fin-streamer/span/text()").get(default='').strip()
            percent_change = row.xpath(".//td[6]/fin-streamer/span/text()").get(default='').strip()
            volume = row.xpath(".//td[7]/fin-streamer/text()").get(default='').strip()
            market_cap = ''.join(row.xpath(".//td[8]/text()").getall()).strip() if row.xpath(".//td[8]/text()") else 'нет данных'

            # Заполняем Item
            item = TrendingTickersScrapyItem(
                Symbol=symbol,
                Name=name,
                Last_price=last_price,
                Market_time=market_time,
                Change=change,
                PercentChange=percent_change,
                Volume=volume,
                Market_Cap=market_cap
            )

            # Отправляем данные в Pipeline
            yield item
