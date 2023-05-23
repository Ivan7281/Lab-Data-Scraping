# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class Lab5Pipeline:
    def process_item(self, item, spider):
        return item


class PricePipeline:
    def process_item(self, item, spider):
        try:
            item["price"] = float((item.get("price").replace("₴", "")).replace("\xa0", ""))
            return item
        except:
            raise DropItem(f"Bad price in {item}")

