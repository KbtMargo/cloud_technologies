# check_tables.py
import asyncio

from sqlalchemy import inspect

from src.database.base import engine


async def check_table_structure():
    async with engine.connect() as conn:
        # Отримуємо інспектор для перегляду структури БД
        inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn))

        # Отримуємо список таблиць
        tables = await conn.run_sync(lambda sync_conn: inspector.get_table_names())
        print("📊 Таблиці в базі даних:", tables)

        # Перевіряємо структуру dog_photos
        if "dog_photos" in tables:
            print("\n🔍 Структура таблиці dog_photos:")
            columns = await conn.run_sync(lambda sync_conn: inspector.get_columns("dog_photos"))
            for column in columns:
                print(
                    f"  {column['name']}: {column['type']} | Nullable: {column['nullable']} | Default: {column.get('default', 'None')}"
                )


if __name__ == "__main__":
    asyncio.run(check_table_structure())
