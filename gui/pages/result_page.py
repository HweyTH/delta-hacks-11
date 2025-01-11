from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class ResultPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        stats_layout = QHBoxLayout()

        # Left Column - WPM and Accuracy
        left_stats = QVBoxLayout()
        wpm_label = QLabel("wpm\n26")
        wpm_label.setAlignment(Qt.AlignLeft)
        wpm_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        left_stats.addWidget(wpm_label)

        acc_label = QLabel("acc\n79%")
        acc_label.setAlignment(Qt.AlignLeft)
        acc_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        left_stats.addWidget(acc_label)

        stats_layout.addLayout(left_stats)

        # Center - Graph (Placeholder for now)
        graph_label = QLabel("Graph Placeholder")
        graph_label.setFixedSize(600, 200)
        graph_label.setAlignment(Qt.AlignCenter)
        graph_label.setStyleSheet("background-color: #252535; border-radius: 10px; color: #888888;")
        stats_layout.addWidget(graph_label)

        # Add Stats Layout to Main Layout
        main_layout.addLayout(stats_layout)

        # Details Section
        details_layout = QHBoxLayout()

        details_left = QVBoxLayout()
        test_type_label = QLabel("test type\ntime 30\nenglish")
        test_type_label.setAlignment(Qt.AlignLeft)
        test_type_label.setStyleSheet("font-size: 16px; color: #888888;")
        details_left.addWidget(test_type_label)

        details_layout.addLayout(details_left)

        details_center = QVBoxLayout()
        raw_label = QLabel("raw\n28")
        raw_label.setAlignment(Qt.AlignCenter)
        raw_label.setStyleSheet("font-size: 16px; color: #888888;")
        details_center.addWidget(raw_label)

        details_layout.addLayout(details_center)

        details_right = QVBoxLayout()
        char_label = QLabel("characters\n64/1/0/1")
        char_label.setAlignment(Qt.AlignRight)
        char_label.setStyleSheet("font-size: 16px; color: #888888;")
        details_right.addWidget(char_label)

        details_layout.addLayout(details_right)

        # Add Details Layout to Main Layout
        main_layout.addLayout(details_layout)

        # Time Section
        time_label = QLabel("time\n30s")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("font-size: 16px; color: #888888;")
        main_layout.addWidget(time_label)

        # Set Main Layout
        self.setLayout(main_layout)
