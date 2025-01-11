from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ResultPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Create a label for the result
        result_label = QLabel("Results")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(result_label)

        # Set the layout for the page
        self.setLayout(layout)