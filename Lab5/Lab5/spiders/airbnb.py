import scrapy
from Lab5.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from Lab5.items import Lab5Item


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com.ua"]
    start_urls = ["https://www.airbnb.com.ua/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=500,
                execute=self.close_banner
            )

    def close_banner(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label,"Закрити")]')))
        later_button = driver.find_element(By.XPATH, '//button[contains(@aria-label,"Закрити")]')
        later_button.click()
        # "//button[contains(@aria-label,'Закрити')] aria-label="Закрити" l1j9v1wn ci31uza dir dir-ltr"
        # l1j9v1wn ci31uza dir dir-ltr c4mnd7m dir dir-ltr

    def parse(self, response):
        room_list = response.xpath('//div[contains(@class,"c61fd4t d479qfo dir dir-ltr")]').xpath(
            "//div[@class='c4mnd7m dir dir-ltr']")
        for room in room_list:
            name = room.xpath(".//div[@class='t1jojoys dir dir-ltr']/text()").get()
            url = room.xpath(".//a[@class='l1j9v1wn bn2bl2p dir dir-ltr']/@href").get()
            price = room.xpath(".//span[@class='_tyxjp1']/text()").get()
            yield Lab5Item(
                name=name,
                url=url,
                price=price
            )
