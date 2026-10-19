import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from ui.pages.precipitation import PrecipitationPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Журнал погоды")
        self.resize(1000, 650)
        central = QWidget()
        layout = QVBoxLayout(central)


        layout.addWidget(QLabel("Журнал погоды"))
        open_report = QPushButton("Заполнить отчёт")
        layout.addWidget(open_report)
        layout.addStretch()

        report = QWidget()
        report_layout = QVBoxLayout(report)

        report_layout.addWidget(QLabel("Выбери показатель"))
        for name in ("темпиратура",
                     "Ветер",
                     "Давление",
                     "Влажность",
                     "Уф-индекс",
                     "облачность",
                     "осадки",
                     "заметки",):
            botton = QPushButton(name)
            report_layout.addWidget(botton)
            if name == "осадки":
                botton.clicked.connect(
                    lambda: self.pages.setCurrentWidget(
                        self.precipitation_page
                    )
                )
        back_botton = QPushButton("Назад")
        report_layout.addWidget(back_botton)
        report_layout.addStretch()

        self.pages = QStackedWidget()
        self.pages.addWidget(central)
        self.pages.addWidget(report)
        self.precipitation_page = PrecipitationPage()
        self.pages.addWidget(self.precipitation_page)

        back_to_report = QPushButton("Назад к показателям")
        self.precipitation_page.layout().insertWidget(0, back_to_report)

        back_to_report.clicked.connect(
            lambda: self.pages.setCurrentWidget(report)
        )
        self.setCentralWidget(self.pages)

        open_report.clicked.connect(
            lambda: self.pages.setCurrentWidget(report))

        back_botton.clicked.connect(
            lambda: self.pages.setCurrentWidget(central))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())