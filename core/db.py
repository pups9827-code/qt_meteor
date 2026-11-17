import json
import sqlite3
from datetime import date


def create_database():
    # Подключаемся к базе. Если файла нет, SQLite создаст его.
    db = sqlite3.connect("weather.db")

    # Создаём таблицу, если она ещё не существует.
    db.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            date TEXT PRIMARY KEY,
            data TEXT
        )
    """)

    # Закрываем соединение с базой.
    db.close()


def save_observations(records):
    # Открываем базу.
    db = sqlite3.connect("weather.db")

    # По очереди сохраняем каждое наблюдение.
    for record in records:
        # Копируем запись, чтобы не менять исходные данные.
        data = record.copy()

        # Превращаем дату в строку, чтобы записать её в JSON.
        data["date"] = str(data["date"])

        # Сохраняем дату и всю запись.
        # Если такая дата уже есть, старая запись заменится.
        db.execute(
            "INSERT OR REPLACE INTO observations VALUES (?, ?)",
            (data["date"], json.dumps(data, ensure_ascii=False))
        )

    # Сохраняем изменения в файле базы.
    db.commit()

    # Закрываем соединение.
    db.close()


def get_observations():
    # Открываем базу.
    db = sqlite3.connect("weather.db")

    # Получаем все записи, отсортированные по дате.
    rows = db.execute(
        "SELECT data FROM observations ORDER BY date"
    ).fetchall()

    db.close()

    records = []

    for row in rows:
        # Превращаем JSON-текст обратно в словарь Python.
        record = json.loads(row[0])

        # Превращаем дату из строки обратно в дату Python.
        record["date"] = date.fromisoformat(record["date"])

        records.append(record)

    return records
