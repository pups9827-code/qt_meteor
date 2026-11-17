import json
from datetime import date


def load_observations(path):
    # Читаем JSON из выбранного файла.
    # Читаем JSON в кодировке UTF-8.
    with open(path, encoding="utf-8") as file:
        records = json.load(file)

    for record in records:
        # Превращаем строку в дату для фильтрации по периоду.
        record["date"] = date.fromisoformat(record["date"])

        # Если заметка отсутствует, используем пустую строку.
        record["notes"] = record.get("notes", "")

    # Располагаем наблюдения от старых к новым.
    return sorted(records, key=lambda record: record["date"])
