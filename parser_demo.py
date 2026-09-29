import csv
import time
import httpx
from bs4 import BeautifulSoup


def parse_multipage_books(pages_to_scrape: int = 3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    filename = "books.csv"
    total_count = 0

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Страница", "Название", "Цена", "Наличие"])

        for page in range(1, pages_to_scrape + 1):
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"
            print(f"Парсим страницу {page}: {url}...")

            try:
                response = httpx.get(url, headers=headers, timeout=10.0)
            except Exception as e:
                print(f"Ошибка соединения на странице {page}: {e}")
                continue

            if response.status_code != 200:
                print(f"Страница {page} не найдена или ошибка {response.status_code}. Завершаем.")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            book_cards = soup.find_all("article", class_="product_pod")

            for card in book_cards:
                title = card.find("h3").find("a").get("title")
                price = card.find("p", class_="price_color").text.strip()
                availability = card.find("p", class_="instock availability").text.strip()

                writer.writerow([page, title, price, availability])
                total_count += 1

            time.sleep(1)

    print(f"\nВсе готово! Успешно спарсили {pages_to_scrape} стр. Всего собрано: {total_count} товаров.")


if __name__ == "__main__":
    parse_multipage_books(pages_to_scrape=3)