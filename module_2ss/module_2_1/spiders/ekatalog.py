import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from module_2_1.SeleniumRequest import SeleniumRequest
from module_2_1.items import Module21Item


class EkatalogSpider(scrapy.Spider):
    name = "ekatalog"
    allowed_domains = ["ek.ua"]
    start_urls = [f"https://ek.ua/ua/list/161/{page}/" for page in range(0, 1)]

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
        form_list = response.xpath('//form[contains(@id, "list_form")]').xpath(
            './/div[contains(@class, "model-short-div")][not(contains(@class, "list-more"))]')

        for item in form_list:
            form = item.xpath('//td[@class="model-hot-prices-td"]')
            img = item.xpath('.//img[contains(@id, "img_he")]/@src').get()

            for page in form:
                store_name = page.xpath('.//div[@class="sn-div"]//u/text()').get()
                price = page.xpath('.//td[@class="model-shop-price"]/a/text()').get()

                if store_name and price and img:
                    yield Module21Item(
                        img=img,
                        store_name=store_name,
                        price=price
                    )