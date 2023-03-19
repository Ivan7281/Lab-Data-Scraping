import scrapy
from bs4 import BeautifulSoup
from lab2.items import CatalogItem, ListingItem, SmartfonItem

class FoxtrotSpider(scrapy.Spider):
    name = "foxtrot"
    allowed_domains = ["foxtrot.com.ua"]
    start_urls = ["http://foxtrot.com.ua/uk/shop/mobilnye_telefony_smartfon.html"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        shop_list = soup.find(class_="listing__body-wrap")

        for article in shop_list.find_all("article"):
            a = article.find("a")
            card_title = a.find(string=True, recursive=False)
            card_url = f"http://foxtrot.com.ua{a.get('href')}"

            yield CatalogItem(
                title=card_title,
                url=card_url
            )

            yield scrapy.Request(
                url=card_url,
                callback=self.parse_catalog,
                meta={
                    "catalog": card_title
                }
            )

    def parse_catalog(self, response):
        soup = BeautifulSoup(response.body,  "html.parser")
        listing = soup.find(class_="listing__body-wrap")

        if listing:
            for article in listing.find_all("article"):
                title_list = article.a.find(string=True, recursive=False)
                url_list = f"http://foxtrot.com.ua{article.a.get('href')}"

                yield ListingItem(
                    title=title_list,
                    url=url_list,
                    catalog=response.meta.get("catalog")
                )

                yield scrapy.Request(
                    url=url_list+"smartfon",
                    callback=self.parse_listing,
                    meta={
                        "listing": title_list
                    }
                )

    def parse_listing(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
