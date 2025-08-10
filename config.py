# config.py
# №1: Загружаем .env и даём константы для всего проекта.

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # №2: Подтянуть переменные из .env в окружение процесса

BOT_TOKEN: str | None = getenv("BOT_TOKEN")  # №3: Токен бота
#DB_PATH: Path = Path("/app/data/bot.db")     # №4: БД хранится в томе /app/data (см. docker-compose.yml)
DB_PATH: Path = Path("bot.db")