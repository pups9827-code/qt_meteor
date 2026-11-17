from PyQt6.QtWidgets import (
    QLabel, QMessageBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QComboBox, QTextEdit, QDialog
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from datetime import timedelta
from core.importt import load_observations
from ui.charts import draw_charts
from core.db import create_database, save_observations, get_observations


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # Основная раскладка: панель слева, графики справа.
        main_layout = QHBoxLayout(self)

        sidebar = QWidget()
        sidebar.setFixedWidth(190)
        sidebar_layout = QVBoxLayout(sidebar)

        sidebar_layout.addWidget(QLabel("Журнал погоды"))

        # Создаём базу, если её ещё нет.
        create_database()

        # Загружаем ранее сохранённые наблюдения.
        self.observations = get_observations()

        import_button = QPushButton("Импорт JSON")
        import_button.clicked.connect(self.import_json)
        sidebar_layout.addWidget(import_button)

        sidebar_layout.addWidget(QLabel("Период"))

        self.period = QComboBox()

        # Второй аргумент — значение, связанное с пунктом списка.
        self.period.addItem("Неделя", 7)
        self.period.addItem("Месяц — 30 дней", 30)
        sidebar_layout.addWidget(self.period)

        # При смене периода перерисовываем графики.
        self.period.currentIndexChanged.connect(self.update_charts)

        forecast_button = QPushButton("Открыть прогноз")
        forecast_button.clicked.connect(self.show_forecast)
        sidebar_layout.addWidget(forecast_button)

        # Печать подключим, когда сделаем формирование отчёта.
        print_button = QPushButton("Распечатать")
        print_button.setEnabled(False)
        sidebar_layout.addWidget(print_button)

        journal_button = QPushButton("История наблюдений")

        # При нажатии открываем окно с историей.
        journal_button.clicked.connect(self.show_history)

        sidebar_layout.addWidget(journal_button)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        content_layout = QVBoxLayout()
        # Сохраняем заголовок, чтобы менять его после импорта.
        self.period_label = QLabel("Импортируйте наблюдения из JSON")
        content_layout.addWidget(self.period_label)
        main_layout.addLayout(content_layout, 1)

        # Главное окно по-прежнему записывает сюда прогноз.
        # Надпись не размещаем на экране: покажем её в диалоге.
        self.forecast_label = QLabel("Прогноз ещё загружается", self)
        self.forecast_label.hide()

        self.figure = Figure(
            figsize=(9, 7),
            layout="constrained",
            facecolor="#202020",
        )
        self.canvas = FigureCanvasQTAgg(self.figure)
        content_layout.addWidget(self.canvas, 1)

        self.charts = {}

        indicators = [
            ("Температура", "°C"),
            ("Ветер", "м/с"),
            ("Давление", "мм рт. ст."),
            ("Влажность", "%"),
            ("УФ-индекс", ""),
            ("Облачность", "%"),
            ("Осадки", ""),
            ("Заметки", ""),
        ]

        for position, (name, unit) in enumerate(indicators, start=1):
            # 4 ряда, 2 столбца, номер текущей плашки.
            axes = self.figure.add_subplot(4, 2, position)
            self.style_chart(axes, name)

            if unit:
                axes.set_ylabel(unit, color="#cccccc", fontsize=8)

            axes.set_xticks([])
            axes.set_yticks([])

            message = (
                "Заметок нет"
                if name == "Заметки"
                else "Нет наблюдений"
            )

            axes.text(
                0.5, 0.5, message,
                transform=axes.transAxes,
                ha="center", va="center",
                color="#cccccc", fontsize=9,
                wrap=True,
            )

            self.charts[name] = axes

        # Рисуем сохранённые наблюдения.
        self.update_charts()

    def style_chart(self, axes, name):
        axes.set_facecolor("#292525")
        axes.set_title(name, color="white", fontsize=11)
        axes.tick_params(colors="#cccccc", labelsize=8)
        for border in axes.spines.values():
            border.set_color("#555555")


    def show_history(self):
        # Создаём окно.
        window = QDialog(self)
        window.setWindowTitle("История наблюдений")
        window.resize(500, 600)

        layout = QVBoxLayout(window)

        # Создаём поле для просмотра текста.
        history = QTextEdit()
        history.setReadOnly(True)

        # Получаем сохранённые записи из базы.
        records = get_observations()

        for record in records:
            # Собираем текст для одного дня.
            text = (
                f"Дата: {record['date']}\n"
                f"Температура: от {record.get('temperature_min')} "
                f"до {record.get('temperature_max')} °C\n"
                f"Ветер: {record.get('wind')} м/с\n"
                f"Давление: {record.get('pressure')} мм рт. ст.\n"
                f"Влажность: {record.get('humidity')} %\n"
                f"УФ-индекс: {record.get('uv')}\n"
                f"Облачность: {record.get('cloudiness')} %\n"
                f"Осадки: {record.get('precipitation')} мм\n"
                f"Заметки: {record.get('notes', '')}\n"
            )

            # Добавляем запись в окно.
            history.append(text)

        # Если в базе пока нет записей, показываем сообщение.
        if not records:
            history.setPlainText("Наблюдений пока нет.")

        layout.addWidget(history)

        # Показываем окно.
        window.exec()

    def show_forecast(self):
        # Показываем прогноз, который загрузило главное окно.
        QMessageBox.information(
            self,
            "Прогноз погоды",
            self.forecast_label.text(),
        )

    def import_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл наблюдений",
            "",
            "JSON (*.json)",
        )

        # Если нажали «Отмена», просто выходим из метода.
        if not path:
            return

        # Читаем выбранный JSON.
        records = load_observations(path)

        # Сохраняем данные в базу.
        save_observations(records)

        # Получаем все сохранённые наблюдения и обновляем графики.
        self.observations = get_observations()
        self.update_charts()

    def update_charts(self):
        # Пока файл не загружен, рисовать нечего.
        if not self.observations:
            return

        days = self.period.currentData()

        # Выбираем последние 7 или 30 дней от последней даты файла.
        end = self.observations[-1]["date"]
        start = end - timedelta(days=days - 1)

        self.period_label.setText(
            f"Наблюдения: {start:%d.%m.%Y} — {end:%d.%m.%Y}"
        )

        records = [
            record
            for record in self.observations
            if start <= record["date"] <= end
        ]

        # Все дни периода нужны, чтобы пропущенные дни
        # не соединялись линией как непрерывные наблюдения.
        dates = [
            start + timedelta(days=offset)
            for offset in range(days)
        ]

        draw_charts(self.charts, dates, records, self.style_chart)
        self.canvas.draw_idle()
