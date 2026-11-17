import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.dates import date2num, DateFormatter
from matplotlib.lines import Line2D


# Цветовые переходы от холодной температуры к тёплой.
TEMPERATURE_COLORS = LinearSegmentedColormap.from_list(
    "temperature",
    [
        "#9254ff",  # −20
        "#427bff",  # −10
        "#39d3ef",  #   0
        "#63d452",  # +10
        "#ffe144",  # +20
        "#ff923b",  # +30
        "#ed36b7",  # +40
    ],
)

# Одинаковая температура всегда получает одинаковый цвет.
TEMPERATURE_SCALE = Normalize(vmin=-20, vmax=40, clip=True)


def draw_temperature(axes, dates, minimums, maximums):
    # Matplotlib хранит даты как числа.
    x = date2num(dates)

    lines = [
        (maximums, "solid", "o", 4),
        (minimums, "dashed", "v", 3),
    ]

    for values, style, marker, width in lines:
        # None превращается в NaN — пропущенное измерение.
        y = np.array(values, dtype=float)

        # Рисуем каждый промежуток между соседними днями.
        for index in range(len(x) - 1):
            # Через отсутствующее измерение линию не проводим.
            if not np.isfinite(y[index:index + 2]).all():
                continue

            t = np.linspace(0, 1, 40)

            # Плавный переход без выхода за значения соседних дней.
            smooth = t * t * (3 - 2 * t)

            curve_x = x[index] + (x[index + 1] - x[index]) * t
            curve_y = y[index] + (y[index + 1] - y[index]) * smooth

            points = np.column_stack([curve_x, curve_y])

            # Делим кривую на маленькие отрезки.
            segments = np.stack(
                [points[:-1], points[1:]],
                axis=1,
            )

            # Каждому отрезку назначаем цвет по его температуре.
            collection = LineCollection(
                segments,
                cmap=TEMPERATURE_COLORS,
                norm=TEMPERATURE_SCALE,
                linewidths=width,
                linestyles=style,
            )
            collection.set_array(
                (curve_y[:-1] + curve_y[1:]) / 2
            )
            collection.set_capstyle("round")

            axes.add_collection(collection)

        # Точки показывают настоящие измерения из файла.
        known = np.isfinite(y)

        axes.scatter(
            x[known],
            y[known],
            c=y[known],
            cmap=TEMPERATURE_COLORS,
            norm=TEMPERATURE_SCALE,
            marker=marker,
            s=24,
            zorder=3,
        )

    axes.xaxis_date()
    axes.xaxis.set_major_formatter(DateFormatter("%d.%m"))
    axes.autoscale_view()
    axes.set_ylabel("°C", color="white", fontsize=8)
    axes.grid(True, alpha=0.15)

    # Обозначения помогают отличить минимум от максимума.
    axes.legend(
        handles=[
            Line2D(
                [], [], color="white",
                marker="o", linestyle="-", label="Макс.",
            ),
            Line2D(
                [], [], color="white",
                marker="v", linestyle="--", label="Мин.",
            ),
        ],
        labelcolor="white",
        frameon=False,
        fontsize=8,
        loc="upper left",
    )
