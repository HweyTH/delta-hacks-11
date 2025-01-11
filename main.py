import sys

class MyThread(QThread):
    frame_signal = Signal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            _,frame = self.cap.read()
            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)
    
    def cvimage_to_label(self,image):
        image = imutils.resize(image,width = 640)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = QImage(image,
                       image.shape[1],
                       image.shape[0],
                       QImage.Format_RGB888)
        return image



class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integrated Navigation App")
        self.setFixedSize(800, 600)

        # Set up the stacked widget for navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.home_page = HomePage(self.navigate_to_game_page)
        self.game_page = GamePage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.game_page)

        # Show the home page initially
        self.stacked_widget.setCurrentWidget(self.home_page)

    def navigate_to_game_page(self):
        """Navigate to the Game Page."""
        self.stacked_widget.setCurrentWidget(self.game_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
