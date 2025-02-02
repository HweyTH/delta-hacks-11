from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PlayerHandler import PlayerHandler
from functions import color_text
import cv2, imutils

detected_letter_f_string = 'Detected Letter: {}'

class GamePage(QWidget):
    def __init__(self, parent=None, selected_time=60, navigate_to_result_page=None):
        super().__init__(parent)
        self.player_handler = PlayerHandler(selected_time)
        self.selected_time = selected_time
        self.navigate_to_result_page = navigate_to_result_page

        # Set the background color to black
        self.setStyleSheet("background-color: black;")

        # Create a label for the camera feed
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("border: 2px solid white;")
        self.camera_label.setAlignment(Qt.AlignCenter)

        # Create a label for the word
        self.word_label = QLabel("Start Signing!")
        self.word_label.setStyleSheet("color: white; font-size: 24px;")
        self.word_label.setAlignment(Qt.AlignCenter)

        self.detected_letter_label = QLabel(detected_letter_f_string.format(''))
        self.detected_letter_label.size()
        self.detected_letter_label.setStyleSheet("color: white; font-size: 24px;")
        self.detected_letter_label.setAlignment(Qt.AlignCenter)
        
        # Create a label for the timer
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("color: white; font-size: 18px;")
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Create the start button
        self.start_button = QPushButton("Start Recording")
        self.start_button.setStyleSheet("color: white; background-color: green; font-size: 18px;")
        self.start_button.clicked.connect(self.start_recording)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)

        # Create a vertical layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.word_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.detected_letter_label)
        layout.addLayout(button_layout)

        # Set the layout for the page
        self.setLayout(layout)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.timer = self.startTimer(30)  # Update the camera feed every 30 ms

        # Initialize countdown timer
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer)
        self.time_left = self.selected_time  # Set countdown time based on selected time

        self.input_image = None

    def timerEvent(self, event):
        ret, frame = self.cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.input_image = image
            self.camera_label.setPixmap(QPixmap.fromImage(image))

    def start_recording(self):
        print("Start Recording")
        self.time_left = self.selected_time  # Reset countdown time
        self.word_label.setText(self.player_handler.current_word)  # Display first word
        self.countdown_timer.start(1000)  # Start countdown timer

    def update_timer(self):
        green_span = "<span style='color: green;'>{}</span>"
        red_span = "<span style='color: red;'>{}</span>"
        grey_span = "<span style='color: grey;'>{}</span>"

        self.detected_letter_label.setText(detected_letter_f_string.format(''))
        if self.time_left > 0:
            self.time_left -= 1
            self.player_handler.update_wpm()
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.setText(f"{minutes:02}:{seconds:02}")

            # Process the frame and update the UI
            detected_letter, result = self.player_handler.process_frame(self.input_image)
            if result == 'green': letter_label_text = detected_letter_f_string.format(green_span.format(detected_letter))
            elif result == 'red': letter_label_text = detected_letter_f_string.format(red_span.format(detected_letter))
            else: letter_label_text = detected_letter_f_string.format(grey_span.format(detected_letter))
            self.detected_letter_label.setText(letter_label_text)
            text = color_text(
                self.player_handler.current_word,
                self.player_handler.letter_index,
                self.player_handler.typed_colors,
            )
            self.word_label.setText(text)

        else:
            self.player_handler.save_stats()
            self.countdown_timer.stop()
            if self.navigate_to_result_page:
                self.navigate_to_result_page()
            
