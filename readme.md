# 🌦️ Журнал погоды

Приложение на Python для просмотра прогноза и анализа своих погодных наблюдений.

## Возможности

- Импорт наблюдений из JSON и сохранение в SQLite.
- Графики температуры, ветра, давления, влажности, УФ-индекса, облачности и осадков.
- Просмотр заметок и истории наблюдений.
- Выбор периода: неделя или 30 дней.
- Загрузка прогноза Open-Meteo для заданных в коде координат.

## Технологии

Python · PyQt6 · Matplotlib · SQLite · Open-Meteo

## Запуск

```bash
git clone https://github.com/pups9827-code/qt_meteor.git
cd qt_meteor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

В Windows вместо команды активации используйте `.venv\Scripts\activate`. Для загрузки прогноза нужен интернет. Файл базы `weather.db` создаётся автоматически в рабочей папке.

## Пример файла наблюдений

Выберите JSON-файл через кнопку «Импорт JSON». Пример одной записи:

```json
[
  {
    "date": "2026-11-17",
    "temperature_min": -2,
    "temperature_max": 3,
    "wind": 4,
    "pressure": 750,
    "humidity": 75,
    "uv": 1,
    "cloudiness": 80,
    "precipitation": 0,
    "notes": "Облачно"
  }
]
```

Кнопка печати пока отключена — формирование отчёта ещё не реализовано.
