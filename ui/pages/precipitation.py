import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QButtonGroup, QComboBox
)


class PrecipitationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Журнал погоды - осадков")
        self.resize(800, 500)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("осадки"))

        choices = QHBoxLayout()
        self.choice_group = QButtonGroup(self)
        self.choice_group = QButtonGroup(self)

        for name in ("нет", "дождь", "снег", "другое"):
            button = QPushButton(name)
            button.setCheckable(True)
            button.setStyleSheet(
                "QPushButton:checked {"
                "background-color: #D6B369;"
                "color: #1E1E1E;"
                "border: 1px solid #D6B369;"
                "}"
            )
            self.choice_group.addButton(button)
            choices.addWidget(button)

        layout.addLayout(choices)
        layout.addWidget(QLabel("Сила осадков"))

        self.intensity = QComboBox()
        self.intensity.addItems(
            ["Не указана", "Слабые", "Умеренные", "Сильные"]
        )
        layout.addWidget(self.intensity)
        layout.addStretch()
