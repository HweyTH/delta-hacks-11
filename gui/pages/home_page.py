from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, navigate_to_game_page, parent=None):
        super().__init__(parent)

        self.navigate_to_game_page = navigate_to_game_page

        # Set up layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Time Selection (Centered with Dropdown)
        time_selection_layout = QHBoxLayout()
        time_label = QLabel("Select Time:")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("font-size: 18px;")
        time_selection_layout.addWidget(time_label)

        self.time_dropdown = QComboBox()
        self.time_dropdown.addItems(["Select Time", "30 Seconds", "1 Minute", "2 Minutes", "3 Minutes", "5 Minutes"])
        self.time_dropdown.setCurrentIndex(0)
        time_selection_layout.addWidget(self.time_dropdown)

        layout.addLayout(time_selection_layout)

        # Open Camera Button (Initially Disabled)
        self.open_camera_btn = QPushButton("Open Camera")
        self.open_camera_btn.setEnabled(False)  # Disabled initially
        self.open_camera_btn.clicked.connect(self.open_camera)
        layout.addWidget(self.open_camera_btn)

        # Set the layout for the page
        self.setLayout(layout)

        # Enable "Open Camera" Button only when a valid time is selected
        self.time_dropdown.currentIndexChanged.connect(self.enable_camera_button)

    def enable_camera_button(self):
        """Enable the Open Camera button only when a valid time is selected."""
        selected_time = self.time_dropdown.currentText()
        if selected_time != "Select Time":
            self.open_camera_btn.setEnabled(True)
        else:
            self.open_camera_btn.setEnabled(False)

    def open_camera(self):
        """Navigate to the Game Page."""
        selected_time = self.time_dropdown.currentText()
        print(f"Starting game with time: {selected_time}")
        self.navigate_to_game_page()
