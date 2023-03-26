import scrapy
from bs4 import BeautifulSoup
from Lab3.items import FoxtrotItem


class FoxtrotSpider(scrapy.Spider):
    name = "foxtrot"
    allowed_domains = ["foxtrot.com.ua"]
    start_urls = [
        f"https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_smartfon.html?page={page}" for page in range(1, 6)]

    def parse(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        catalog = soup.find(
            name="div", class_="listing__body-wrap").find_all(class_="card js-card sc-product")
        for item in catalog:
            name = item.find(name="a", class_="card__title").find(string=True, recursive=False).strip()
            url = item.find(name="a", class_="card__title").get("href")
            price = item.find(class_="card-price").find(string=True, recursive=False).strip()
            yield FoxtrotItem(
                name=name,
                price=price,
                url=url,
            )
