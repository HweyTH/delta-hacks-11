from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap

class HomePage(QWidget):
    def __init__(self, navigate_to_game_page, parent=None):
        super().__init__(parent)

        self.navigate_to_game_page = navigate_to_game_page

        # Set the background color of the entire window (including space around the widgets)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(152, 134, 159))  # Purple background for the entire window
        self.setPalette(palette)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Logo in the top-right corner
        logo_label = QLabel()
        logo_pixmap = QPixmap("path_to_logo.png")  # Replace with the path to your logo image
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize the logo
        logo_label.setStyleSheet("margin: 10px;")  # Add some margin around the logo


        # Layout to position the logo
        logo_layout = QHBoxLayout()
        logo_layout.addStretch()  # Push the logo to the right
        logo_layout.addWidget(logo_label)

        # Add logo layout to the main layout
        main_layout.addLayout(logo_layout)

        # Welcome label
        welcome_label = QLabel("Welcome to Sign Streak!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold; padding-bottom: 30px;")
        main_layout.addWidget(welcome_label)

        # Time selection
        time_selection_layout = QHBoxLayout()
        time_label = QLabel("Select Time:")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("font-size: 18px; color: white;")
        time_selection_layout.addWidget(time_label)

        self.time_dropdown = QComboBox()
        self.time_dropdown.addItems(["Select Time", "1 Second", "30 Seconds", "1 Minute", "2 Minutes", "3 Minutes", "5 Minutes"])
        self.time_dropdown.setCurrentIndex(0)
        time_selection_layout.addWidget(self.time_dropdown)


        main_layout.addLayout(time_selection_layout)


        # Open Camera Button (Initially Disabled)
        self.open_camera_btn = QPushButton("Open Camera")
        self.open_camera_btn.setEnabled(False)  # Disabled initially
        self.open_camera_btn.clicked.connect(self.open_camera)
        self.open_camera_btn.setStyleSheet("color: white; background-color: #3B2251; font-size: 18px; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(self.open_camera_btn)

        # Set the layout for the page
        self.setLayout(main_layout)

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
        time_in_seconds = self.convert_time_to_seconds(selected_time)
        print(f"Starting game with time: {time_in_seconds} seconds")
        self.navigate_to_game_page(time_in_seconds)

    def convert_time_to_seconds(self, selected_time):
        """Convert the selected time to seconds."""
        if selected_time == "30 Seconds":
            return 30
        elif selected_time == "1 Second":
            return 1
        elif selected_time == "1 Minute":
            return 60
        elif selected_time == "2 Minutes":
            return 120
        elif selected_time == "3 Minutes":
            return 180
        elif selected_time == "5 Minutes":
            return 300
        else:
            return 60  # Default to 60 seconds if no valid selection
