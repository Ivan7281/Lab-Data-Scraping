import scrapy
from module.items import HotlineItem


class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.ua"]
    start_urls = [f"https://hotline.ua/ua/bt/holodilniki/?p={page}" for page in range(1, 4)]

    def parse(self, response):
        catalog = response.xpath('//div[contains(@class, "list-body__content")]').xpath('//div[contains(@class, "list-item ")]')

        for item in catalog:
            url = item.xpath('.//a[contains(@class, "list-item__title")]/@href').get()

            yield scrapy.Request(
                url=f"https://hotline.ua" + url,
                callback=self.parse_hotline
            )

    def parse_hotline(self, response):
        product_name = response.xpath('.//h1[contains(@class, "title__main")]/text()').get()
        store_name = response.xpath('.//div[1][@class="list__item row flex"]//a[@data-eventcategory="Pages Product Prices" and @class="shop__title"]/text()').get()
        price = response.xpath('.//div[1][@class="list__item row flex"]//span[@data-eventcategory="Pages Product Prices"]/span[@class="price__value"]/text()').get()

        yield HotlineItem(
            store_name=store_name,
            product_name=product_name,
            price=price
        )
