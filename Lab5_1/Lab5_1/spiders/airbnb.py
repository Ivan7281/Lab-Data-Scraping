import scrapy
from Lab5_1.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from Lab5_1.items import Lab51Item


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com.ua"]
    start_urls = ["https://www.airbnb.com.ua/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10
            )

    def parse(self, response):
        for item in response.css('div.c4mnd7m'):
            url = item.css('a.l1j9v1wn::attr(href)').get()
            yield Lab51Item(
                url=url
            )
