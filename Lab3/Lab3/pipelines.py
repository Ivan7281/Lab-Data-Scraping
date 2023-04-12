# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from mysql.connector import connect


class MySqlPipeline:
    def open_spider(self, spider):
        self.connection = connect(
            host="localhost",
            user="root",
            password="",
            database="scrapy"
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL ")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(50) NOT NULL,
            price FLOAT DEFAULT 0,
            url VARCHAR(500)
        );""")
        spider.logger.info("DB is ready ")

    def process_item(self, item, spider):
        if self.is_duplicate(item):
            self.cursor.execute("""
                                    UPDATE items
                                    SET price = %s
                                    WHERE name = %s
                                    """,
                                [item.get("price"), item.get("name")]
                                )
        else:
            self.cursor.execute(
                "INSERT INTO items (name, price, url) VALUES (%s, %s, %s);",
                [item.get("name"), item.get("price"), item.get("url")])

        self.connection.commit()
        return item

    def is_duplicate(self, item):
        self.cursor.execute(
            "SELECT COUNT(id) FROM items WHERE name = %s;",
            [item.get("name")])
        count = self.cursor.fetchone()[0]
        return count > 0

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")


class PricePipeline:
    def process_item(self, item, spider):
        try:
            item["price"] = float((item.get("price").replace("₴", "")).replace(" ", ""))
            return item
        except:
            raise DropItem(f"Bad price in {item}")





