# main.py
# №1: Главный файл бота на aiogram v3.
# №2: Сейчас наша цель — локальный запуск, инициализация БД и простая команда /start.
# №3: Логику диалога/аудио добавим шагом №2 (когда скажешь "продолжаем").

import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from database import init_db, upsert_user

# №4: Базовый лог — полезно видеть, что происходит
logging.basicConfig(level=logging.INFO)

# №5: Проверяем наличие токена в окружении (его загружает config.py из .env)
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env. Заполни файл .env и перезапусти.")

# №6: Создаём экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    №7: Обработчик /start.
    - Инициализирует пользователя в БД (upsert по tg_id).
    - Отвечает простым приветствием.
    Возвращает: None.
    """
    tg_id = message.from_user.id                        # №8: телеграмный ID
    name = message.from_user.full_name                  # №9: имя / ФИО из Telegram
    username = message.from_user.username               # №10: @username или None

    # №11: Регистрируем/обновляем пользователя
    user_id = await upsert_user(tg_id=tg_id, name=name, username=username)

    # №12: Отправляем ответ
    await message.answer(
        f"Привет, {name}!\n"
        f"Твоя запись в БД есть (user_id={user_id}).\n"
        f"Бот локально работает на aiogram + SQLite.\n"
        f"Готов двигаться дальше, когда скажешь 🙂"
    )

async def on_startup() -> None:
    """
    №13: Хук старта приложения:
    - Инициализируем БД (создаём таблицы, если нет).
    """
    await init_db()
    logging.info("База данных инициализирована.")

async def main() -> None:
    """
    №14: Точка входа:
    - on_startup()
    - запуск long polling.
    """
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    # №15: Запускаем асинхронный main
    asyncio.run(main())
