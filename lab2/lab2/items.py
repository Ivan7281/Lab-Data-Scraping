# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CatalogItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()

class ListingItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    catalog = scrapy.Field()

class SmartfonItem(scrapy.Item):
    title = scrapy.Field()
    catalog = scrapy.Field()
    pass
