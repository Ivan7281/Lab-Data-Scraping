import scrapy
from bs4 import BeautifulSoup
from module.items import HotlineItem

class HotlineSpider(scrapy.Spider):
    name = "hotline"
    allowed_domains = ["hotline.ua"]
    start_urls = [f"https://hotline.ua/ua/bt/holodilniki/?p={page}" for page in range(1, 5)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        catalog = soup.find(name="div", class_="list-body__content").find_all(class_="list-item")
        for item in catalog:
            name = item.find(name="a", class_="list-item__title").find(string=True, recursive=False).strip()
            title = item.find(
                name="div", class_="list-item__specifications-text").find(string=True, recursive=False).strip()
            price = item.find(class_="price__value").find(string=True, recursive=False)
            url = item.find(name="a", class_="list-item__title").get("href")
            yield HotlineItem(
                name=name,
                price=price,
                url=url,
                title=title
            )
