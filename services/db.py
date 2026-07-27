import aiosqlite
from datetime import date

DB_PATH = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                generations_today INTEGER DEFAULT 0,
                last_gen_date TEXT,
                selected_style TEXT DEFAULT 'realistic',
                is_premium INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def get_user(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return None


async def register_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username),
        )
        await db.commit()


async def can_generate(user_id: int) -> bool:
    user = await get_user(user_id)
    if not user:
        return False
    if user["is_premium"]:
        return True
    today = date.today().isoformat()
    if user["last_gen_date"] != today:
        return True
    return user["generations_today"] < 5


async def increment_generation(user_id: int):
    from config import FREE_DAILY_LIMIT

    user = await get_user(user_id)
    today = date.today().isoformat()

    async with aiosqlite.connect(DB_PATH) as db:
        if user["last_gen_date"] != today:
            await db.execute(
                "UPDATE users SET generations_today = 1, last_gen_date = ? WHERE user_id = ?",
                (today, user_id),
            )
        else:
            await db.execute(
                "UPDATE users SET generations_today = generations_today + 1 WHERE user_id = ?",
                (user_id,),
            )
        await db.commit()


async def get_generations_left(user_id: int) -> int:
    user = await get_user(user_id)
    if not user:
        return 0
    if user["is_premium"]:
        return -1
    today = date.today().isoformat()
    if user["last_gen_date"] != today:
        return 5
    return max(0, 5 - user["generations_today"])


async def set_style(user_id: int, style: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET selected_style = ? WHERE user_id = ?",
            (style, user_id),
        )
        await db.commit()


async def set_premium(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET is_premium = 1 WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()
