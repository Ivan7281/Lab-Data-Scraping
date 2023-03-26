import scrapy
from Lab2.items import FacultyItem, DepartmentItem, StaffItem


class OnuXpathSpider(scrapy.Spider):
    name = "onu_xpath"
    allowed_domains = ["onu.edu.ua"]
    start_urls = ["https://onu.edu.ua/uk/structure/faculty"]

    def parse(self, response):
        fac_list = response.xpath('//table[contains(@class, "table")]').xpath('//tr')

        for tr in fac_list:
            fac_name = tr.xpath('.//a/text()').get()
            fac_url = f"https://onu.edu.ua{tr.xpath('.//a/@href').get()}"
            if fac_name:
                yield FacultyItem(
                    name=fac_name,
                    url=fac_url
                )
                yield scrapy.Request(
                    url=fac_url + "/kafedry-ta-inshi-strukturni-pidrozdily",
                    callback=self.parse_faculty,

                    meta={
                        "faculty": fac_name
                    }
                )


    def parse_faculty(self, response):
        dep_list = response.xpath('//article[contains(@class, "item-page")]').xpath('//p')
        for p in dep_list:
            dep_name = p.xpath('.//a/text()').get()
            dep_url = f"https://onu.edu.ua{p.xpath('.//a/@href').get()}"

            if dep_url[32:39] == "faculty" and dep_name:

                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                    faculty=response.meta.get("faculty")
                )
                yield scrapy.Request(
                    url=dep_url + "/spivrobitnyky",
                    callback=self.parse_department,
                    meta={
                        "department": dep_name
                    }
                )
            else:
                dep_name = p.xpath('.//strong/text()').get()
                if dep_url[32:39] == "faculty" and dep_name:

                    yield DepartmentItem(
                        name=dep_name,
                        url=dep_url,
                        faculty=response.meta.get("faculty")
                    )
                    yield scrapy.Request(
                        url=dep_url + "/spivrobitnyky",
                        callback=self.parse_department,
                        meta={
                            "department": dep_name
                        }
                    )
                else:
                    dep_name = p.xpath('.//span/text()').get()
                    if dep_url[32:39] == "faculty" and dep_name:

                        yield DepartmentItem(
                            name=dep_name,
                            url=dep_url,
                            faculty=response.meta.get("faculty")
                        )
                        yield scrapy.Request(
                            url=dep_url + "/spivrobitnyky",
                            callback=self.parse_department,
                            meta={
                                "department": dep_name
                            }
                        )

    def parse_department(self, response):
        staff_list = response.xpath('//table[contains(@class, "category")]').xpath('//tr')
        for tr in staff_list:
            name = tr.xpath('.//a/text()').get().strip()
            if name:
                yield StaffItem(
                    name=name,
                    department=response.meta.get("department")
                )