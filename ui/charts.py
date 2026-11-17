from ui.temperature_chart import draw_temperature
from ui.veter import draw_wind
from ui.davlenie import draw_pressure
from ui.vlajnoct import draw_humidity
from ui.yv_index import draw_uv_index
from ui.oblachnoct import draw_cloudiness
from ui.ocadki import draw_precipitation


def draw_charts(charts, dates, records, style_chart):
    by_date = {record["date"]: record for record in records}
    indicators = {
        "Ветер": ("wind", draw_wind),
        "Давление": ("pressure", draw_pressure),
        "Влажность": ("humidity", draw_humidity),
        "УФ-индекс": ("uv", draw_uv_index),
        "Облачность": ("cloudiness", draw_cloudiness),
        "Осадки": ("precipitation", draw_precipitation),
    }

    for name, axes in charts.items():
        axes.clear()
        style_chart(axes, name)

        if name == "Заметки":
            notes = [
                f"{record['date']:%d.%m}: {record['notes']}"
                for record in records if record["notes"]
            ]
            axes.set_xticks([])
            axes.set_yticks([])
            axes.text(
                0.05, 0.95, "\n".join(notes) or "Заметок нет",
                transform=axes.transAxes, va="top", color="white",
                fontsize=8, wrap=True,
            )
        elif name == "Температура":
            minimums = [by_date.get(day, {}).get("temperature_min") for day in dates]
            maximums = [by_date.get(day, {}).get("temperature_max") for day in dates]
            draw_temperature(axes, dates, minimums, maximums)
        else:
            field, draw_chart = indicators[name]
            values = [by_date.get(day, {}).get(field) for day in dates]
            values = [float("nan") if value is None else value for value in values]
            draw_chart(axes, dates, values)
