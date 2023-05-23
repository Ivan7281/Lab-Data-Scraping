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
                wait_time=5000,
                execute=self.close_banner
            )

    def close_banner(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH,
                                                                '//button[@aria-label="Дивитися «Airbnb Кімнати»"]')))
        later_button = driver.find_element(By.XPATH,
                                           '//button[@aria-label="Закрити"]')
        later_button.click()
        # "//button[contains(@aria-label,'Закрити')] aria-label="Закрити" l1j9v1wn ci31uza dir dir-ltr"
        # l1j9v1wn ci31uza dir dir-ltr c4mnd7m dir dir-ltr type="button"

    def parse(self, response):
        room_list = response.xpath('//main/div/div/div/div/div/div[1]').xpath(
            '//div[@class="c4mnd7m dir dir-ltr"]')
        for room in room_list:
            name = room.xpath(".//div[@data-testid='listing-card-title']/text()").get()
            url = room.xpath('.//a[contains(@aria-labelledby, "title")]/@href').get()
            price = room.xpath('.//span/div[@aria-hidden="true"]/span[@class="_tyxjp1"]/text()[1]').get()
            yield Lab5Item(
                price=price,
                name=name,
                url=url
            )
