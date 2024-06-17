# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class UnsplashImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['image_url'])

    def item_completed(self, results, item, info):
        if results:
            item['image_path'] = [x['path'] for ok, x in results if ok]
        if not item['image_path']:
            raise DropItem("Image download failed")
        return item

class UnsplashScrapyPipeline:
    def process_item(self, item, spider):
        return item
    