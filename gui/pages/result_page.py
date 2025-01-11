from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from stats import get_stats  # Import the get_stats function


class ResultPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Fetch stats using get_stats()
        avg_wpm, accuracy = get_stats()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        self.setStyleSheet("background-color: #1e1e2e; color: #e0e0e0;")

        # Header (Title)
        header = QLabel("Results")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #e0e0e0;")
        main_layout.addWidget(header)

        # Stats Layout
        stats_layout = QVBoxLayout()

        # WPM and Accuracy
        wpm_label = QLabel(f"wpm\n{avg_wpm}")
        wpm_label.setAlignment(Qt.AlignLeft)
        wpm_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        stats_layout.addWidget(wpm_label)

        acc_label = QLabel(f"acc\n{accuracy}%")
        acc_label.setAlignment(Qt.AlignLeft)
        acc_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        stats_layout.addWidget(acc_label)

        # Add Stats Layout to Main Layout
        main_layout.addLayout(stats_layout)

        # Set Main Layout
        self.setLayout(main_layout)
