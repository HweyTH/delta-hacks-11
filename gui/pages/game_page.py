from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2, imutils

class GamePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the background color to black
        self.setStyleSheet("background-color: black;")

        # Create a label for the camera feed
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("border: 2px solid white;")
        self.camera_label.setAlignment(Qt.AlignCenter)

# the start button
        self.start_button = QPushButton("Start Recording")
        self.start_button.setStyleSheet("color: white; background-color: green; font-size: 18px;")
        self.start_button.clicked.connect(self.start_recording)

# the stop button
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setStyleSheet("color: white; background-color: red; font-size: 18px;")
        self.stop_button.clicked.connect(self.stop_recording)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Create a vertical layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addLayout(button_layout)

        # Set the layout for the page
        self.setLayout(layout)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.timer = self.startTimer(30)  # Update the camera feed every 30 ms

    def timerEvent(self, event):
        ret, frame = self.cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(image))

    def start_recording(self):
        print("Start Recording")  # Replace with actual recording functionality

    def stop_recording(self):
        print("Stop Recording")  # Replace with actual recording functionality

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)
