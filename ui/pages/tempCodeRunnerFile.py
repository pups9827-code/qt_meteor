import sys

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class PrecipitationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Журнал погоды - осадков")
        self.resize(800, 500)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("осадки"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrecipitationPage()
    window.show()
    sys.exit(app.exec())

