import scrapy
from module_2.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from module_2.items import Module2Item

class EkatalogSpider(scrapy.Spider):
    name = "ekatalog"
    allowed_domains = ["ek.ua"]
    start_urls = [f"https://ek.ua/ua/list/90/{page}" for page in range(0, 7)]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=5000,
                execute=self.element
            )

    def element(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, './/td[@class="model-shop-price"]/a')))

    def parse(self, response):
        form_list = response.xpath('//form[@id="list_form1"]').xpath(
            '//form[@id="list_form1"]/div[contains(@id, "he8")][not(contains(@class, "list-more"))]')

        for item in form_list:
            form = item.xpath('.//table[@class="model-hot-prices"]')
            img = item.xpath('.//img[contains(@id, "img_he8")]/@src').get()

            for page in form:
                store_name = page.xpath('.//div[@class="sn-div"]//u/text()').get()
                price = page.xpath('.//td[@class="model-shop-price"]/a/text()').get()

                yield Module2Item(
                    img=img,
                    store_name=store_name,
                    price=price
                )
