import scrapy
from module_2.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from module_2.items import Module2Item

class EkatalogSpider(scrapy.Spider):
    name = "ekatalog"
    allowed_domains = ["ek.ua"]
    start_urls = [f"https://ek.ua/ua/list/90/{page}" for page in range(0, 2)]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=50,
                execute=self.close_banner
            )

    def close_banner(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, './/td[@class="model-shop-price"]/a')))

    def parse(self, response):
        form_list = response.xpath('//form[@id="list_form1"]').xpath(
            '//form[@id="list_form1"]/div[contains(@id, "he8")]')
        for item in form_list:
            form = item.xpath('//table[@class="model-hot-prices"]')
            for page in form:
                store_name = page.xpath('.//div[@class="sn-div"]//u/text()').get()
                price = page.xpath('.//td[@class="model-shop-price"]/a/text()').get()

                yield Module2Item(
                    store_name=store_name,
                    price=price
                )
