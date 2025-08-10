# database.py
# №1: Асинхронная работа с SQLite через aiosqlite (не блокируем event loop).

import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DB_PATH

def _now_str() -> str:
    # №2: Удобная утилита для отметки времени в ISO без TZ
    return datetime.utcnow().isoformat(sep=" ", timespec="seconds")

async def init_db(db_path: Path = DB_PATH) -> None:
    """
    №3: Создать таблицы users и tracks, если их нет.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        # №4: Таблица пользователей
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id      INTEGER NOT NULL UNIQUE,
                name       TEXT,
                username   TEXT,
                created_at TIMESTAMP NOT NULL
            );
            """
        )
        # №5: Таблица треков (пока используется позже, но создадим сразу)
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                tg_file_id TEXT    NOT NULL,
                file_name  TEXT,
                mime_type  TEXT,
                duration   INTEGER,
                local_path TEXT,
                created_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
        await db.commit()

async def upsert_user(tg_id: int, name: Optional[str], username: Optional[str]) -> int:
    """
    №6: Добавить нового пользователя или обновить его имя/username.
    Возвращает внутренний user_id.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        cur = await db.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        row = await cur.fetchone()
        await cur.close()

        if row is None:
            cur = await db.execute(
                "INSERT INTO users (tg_id, name, username, created_at) VALUES (?, ?, ?, ?)",
                (tg_id, name, username, _now_str()),
            )
            await db.commit()
            return cur.lastrowid
        else:
            user_id = int(row[0])
            await db.execute(
                "UPDATE users SET name = COALESCE(?, name), username = COALESCE(?, username) WHERE id = ?",
                (name, username, user_id),
            )
            await db.commit()
            return user_id

async def get_user_id_by_tgid(tg_id: int) -> Optional[int]:
    """
    №7: Вернуть user_id по телеграмному tg_id (или None).
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        cur = await db.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        row = await cur.fetchone()
        await cur.close()
        return int(row[0]) if row else None
