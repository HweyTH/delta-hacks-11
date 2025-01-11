from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class SelectTimePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the background color to black
        self.setStyleSheet("background-color: black;")

        # Create a label with the text "Select Time"
        label = QLabel("Select Time")
        label.setStyleSheet("color: white; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)

        # Create buttons for time selection
        self.time_buttons = {
            "30 Seconds": QPushButton("30 Seconds"),
            "1 Minute": QPushButton("1 Minute"),
            "2 Minutes": QPushButton("2 Minutes"),
            "3 Minutes": QPushButton("3 Minutes"),
            "5 Minutes": QPushButton("5 Minutes"),
        }

        for button in self.time_buttons.values():
            button.setStyleSheet("color: white; background-color: gray; font-size: 18px;")
            button.clicked.connect(self.handle_time_selection)  # Connect button clicks to handler

        # Layout for buttons
        button_layout = QHBoxLayout()
        for button in self.time_buttons.values():
            button_layout.addWidget(button)

        # Create a vertical layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(button_layout)

        # Set the layout for the page
        self.setLayout(layout)

    def handle_time_selection(self):
        # Determine which button was clicked and handle it
        sender = self.sender()
        selected_time = sender.text()
        print(f"Selected Time: {selected_time}")  # You can replace this with actual functionality

