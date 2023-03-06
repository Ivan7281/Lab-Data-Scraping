from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://www.foxtrot.com.ua"
URL = f"{BASE_URL}/uk/shop/mobilnye_telefony_smartfon.html"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

LAST_PAGE = 11

FILE_NAME = "telefony.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for page in range(1, LAST_PAGE):
        site = get(URL, headers=HEADERS, params={"page": page})
        soup = BeautifulSoup(site.content, "html.parser")

        catalog = soup.find(name="div", class_="listing__body-wrap").find_all(class_="card js-card sc-product")

        for item in catalog:
            title = item.find(name="a", class_="card__title").find(string=True, recursive=False).strip()
            price = item.find(class_="card-price").find(string=True, recursive=False).strip()

            print(f"Назва: {title}")
            print(f"Ціна: {price}")

            file.write(f"Назва: {title}\n")
            file.write(f"Ціна: {price}\n")
