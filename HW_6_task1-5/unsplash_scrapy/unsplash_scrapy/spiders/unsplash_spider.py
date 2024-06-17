import scrapy
from unsplash_scrapy.items import UnsplashImageItem  

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com']

    def parse(self, response):
        # перемещаемся по категориям
        categories = response.css('a[href*="/t/"]::attr(href)').getall()
        for category in categories:
            yield response.follow(category, self.parse_category)

    def parse_category(self, response):
        # переход к страницам отдельных фотографий
        photos = response.css('a[href*="/photos/"]::attr(href)').getall()
        for photo in photos:
            yield response.follow(photo, self.parse_photo)

        # переход к следующей странице категории
        next_page = response.css('a[title="Next page"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_photo(self, response):
        # сбор данных фотографий
        item = UnsplashImageItem()
        item['image_url'] = response.css('meta[property="og:image"]::attr(content)').get()
        item['image_title'] = response.css('meta[property="og:title"]::attr(content)').get()
        item['image_category'] = response.css('meta[property="og:description"]::attr(content)').get().split(' on ')[1]
        yield item
        