# 📚 Telegram Books Catalog Scraper Bot

Асинхронный Telegram-бот на Python (`aiogram 3`) со встроенным веб-парсером интернет-каталога книг и автоматической генерацией отчетов в формате CSV.

## 🚀 Стек технологий
* **Python 3.12+**
* **aiogram 3.x** — асинхронный фреймворк для взаимодействия с Telegram Bot API
* **httpx** — HTTP-клиент для сбора данных
* **BeautifulSoup4** — парсинг и структурирование HTML-дерева
* **SOCKS5 Proxy (aiohttp-socks)** — стабильное сетевое туннелирование

## 📌 Функционал
* Парсинг многостраничного каталога (пагинация) с заголовками, ценами и наличием товаров.
* Неблокирующий сбор данных через фоновые потоки (`asyncio.to_thread`).
* Экспорт результатов в валидный CSV с поддержкой UTF-8 (`utf-8-sig`) для корректного открытия в Excel и Google Sheets.
* Мгновенная доставка сгенерированного документа пользователю прямо в чат Telegram.

## 🛠 Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/твой_ник/web_catalog_parser_bot.git](https://github.com/твой_ник/web_catalog_parser_bot.git)
   cd web_catalog_parser_botpython -m venv venv
