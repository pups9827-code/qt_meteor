from PyQt6.QtWidgets import QMainWindow

from core.weather_worker import WeatherWorker
from ui.pages.home import HomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Журнал погоды")
        self.resize(1000, 650)

        self.home = HomePage()
        self.setCentralWidget(self.home)

        self.home.forecast_label.setText("Загружаем прогноз...")
        self.weather_worker = WeatherWorker()
        self.weather_worker.loaded.connect(self.show_forecast)
        self.weather_worker.failed.connect(self.show_weather_error)
        self.weather_worker.start()

    def show_forecast(self, data):
        hourly = data["hourly"]
        time = hourly["time"][0].replace("T", " ")
        temperature = hourly["temperature_2m"][0]
        self.home.forecast_label.setText(
            f"Прогноз на {time}\n"
            f"Температура: {temperature} °C\n"
            f"Часовой пояс: {data['timezone']}"
        )

    def show_weather_error(self, message):
        self.home.forecast_label.setText(f"Не удалось загрузить прогноз:\n{message}")
