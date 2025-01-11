from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class GamePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up layout
        layout = QVBoxLayout()

        # Title Label
        label = QLabel("Game Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)

        # Set the layout for the page
        self.setLayout(layout)
