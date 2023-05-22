# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotlineItem(scrapy.Item):
    product_name = scrapy.Field()
    store_name = scrapy.Field()
    price = scrapy.Field()
