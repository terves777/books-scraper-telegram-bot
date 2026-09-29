import asyncio
import csv
import time
from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.types import (
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Пускаем весь трафик бота напрямую через твой Happ (порт 10808)
session = AiohttpSession(proxy="socks5://127.0.0.1:10808")
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

# Кнопка меню
menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📥 Спарсить каталог в CSV")]],
    resize_keyboard=True,
)


def run_parser(pages_to_scrape: int = 2) -> str:
    """Синхронный сбор данных с сайта."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    filename = "books.csv"

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Страница", "Название", "Цена", "Наличие"])

        for page in range(1, pages_to_scrape + 1):
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"
            response = httpx.get(url, headers=headers, timeout=10.0)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            book_cards = soup.find_all("article", class_="product_pod")

            for card in book_cards:
                title = card.find("h3").find("a").get("title")
                price = card.find("p", class_="price_color").text.strip()
                avail = card.find("p", class_="instock availability").text.strip()
                writer.writerow([page, title, price, avail])

            time.sleep(0.5)

    return filename


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-парсер каталога.\n\n"
        "Нажми кнопку ниже, чтобы запустить сбор цен и выгрузить CSV:",
        reply_markup=menu_kb,
    )


@dp.message(F.text == "📥 Спарсить каталог в CSV")
async def handle_parse(message: Message):
    status_msg = await message.answer(
        "⏳ Запущен парсинг каталога... Подожди пару секунд."
    )

    file_path = await asyncio.to_thread(run_parser, 2)

    document = FSInputFile(file_path, filename="Каталог_книг.csv")
    await message.answer_document(
        document=document,
        caption="✅ Выгрузка завершена! Лови свежий CSV-отчет.",
    )
    await status_msg.delete()


async def main():
    print("Бот подключен через Happ (SOCKS5:10808) и слушает команды...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())