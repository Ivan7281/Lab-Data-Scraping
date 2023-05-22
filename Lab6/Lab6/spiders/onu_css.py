import scrapy
from Lab6.items import FacultyItem, DepartmentItem, StaffItem


class OnuCssSpider(scrapy.Spider):
    name = "onu_css"
    allowed_domains = ["onu.edu.ua"]
    start_urls = ["https://onu.edu.ua/uk/structure/faculty"]

    def parse(self, response):
        fac_list = response.css('table.table').css('tr')

        for tr in fac_list:
            fac_name = tr.css('a::text').get()
            fac_url = f"https://onu.edu.ua{tr.css('a::attr(href)').get()}"

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
        dep_list = response.css('article.item-page').css('p')

        for p in dep_list:
            dep_name = p.css('a::text').get()
            dep_url = f"https://onu.edu.ua{p.css('a::attr(href)').get()}"

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
                dep_name = p.css('strong::text').get()
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
                    dep_name = p.css('span::text').get()
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
        staff_list = response.css('table.category').css('tr')
        for tr in staff_list:
            name = tr.css('a::text').get().strip()
            if name:
                yield StaffItem(
                    name=name,
                    department=response.meta.get("department")
                )
