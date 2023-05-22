import scrapy
from bs4 import BeautifulSoup
from Lab6.items import FacultyItem, DepartmentItem, StaffItem

class OnuSpider(scrapy.Spider):
    name = "onu"
    allowed_domains = ["onu.edu.ua"]
    start_urls = ["https://onu.edu.ua/uk/structure/faculty"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        fac_list = soup.find(class_="table table-striped table-hover")
        for tr in fac_list.find_all("tr"):
            a = tr.find("a")
            if a:
                fac_name = a.find(string=True, recursive=False)
                fac_url = f"https://onu.edu.ua{a.get('href')}"
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
        soup = BeautifulSoup(response.body, "html.parser")
        dep_list = soup.find(name="article", class_="item-page")

        for p in dep_list.find_all("p"):
            a = p.find("a")
            strong = p.find("strong")
            span = p.find("span")
            dep_name = a.find(string=True, recursive=False)
            dep_url = f"https://onu.edu.ua{a.get('href')}"

            if dep_url[32:39] == "faculty" and dep_name:
                yield DepartmentItem(
                    name=dep_name,
                    url=dep_url,
                    faculty=response.meta.get("faculty")
                )

                yield scrapy.Request(
                    url=dep_url + "/staff",
                    callback=self.parse_department,
                    meta={
                        "department": dep_name
                    }
                )
            else:
                dep_name = strong.find(string=True, recursive=False)
                if dep_url[32:39] == "faculty" and dep_name:

                    yield DepartmentItem(
                        name=dep_name,
                        url=dep_url,
                        faculty=response.meta.get("faculty")
                    )
                    yield scrapy.Request(
                        url=dep_url + "/staff",
                        callback=self.parse_department,
                        meta={
                            "department": dep_name
                        }
                    )
                else:
                    dep_name = span.find(string=True, recursive=False)
                    if dep_url[32:39] == "faculty" and dep_name:

                        yield DepartmentItem(
                            name=dep_name,
                            url=dep_url,
                            faculty=response.meta.get("faculty")
                        )
                        yield scrapy.Request(
                            url=dep_url + "/staff",
                            callback=self.parse_department,
                            meta={
                                "department": dep_name
                            }
                        )

    def parse_department(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        staff_list = soup.find(name="table", class_="category")

        for tr in staff_list.find_all("tr"):
            a = tr.find("a")
            name = a.find(string=True, recursive=False).strip()
            if name:
                yield StaffItem(
                    name=name,
                    department=response.meta.get("department")
                )
