from PyQt6.QtCore import QThread, pyqtSignal

from core.weather_api import get_forecast

class WeatherWorker(QThread):
    loaded = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def run(self):
        try:
            data = get_forecast(55.664538, 37.453783)
        except Exception as error:
                self.failed.emit(str(error))
        else:
             self.loaded.emit(data)
