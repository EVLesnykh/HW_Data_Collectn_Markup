import scrapy

class TrendingTickersScrapyItem(scrapy.Item):
    Symbol = scrapy.Field()
    Name = scrapy.Field()
    Last_price = scrapy.Field()
    Market_time = scrapy.Field()
    Change = scrapy.Field()
    PercentChange = scrapy.Field()  
    Volume = scrapy.Field()
    Market_Cap = scrapy.Field()