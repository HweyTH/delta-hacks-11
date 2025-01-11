from gui.pages.select_time_page import SelectTimePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize pages
        self.home_page = HomePage()
        self.game_page = GamePage()
        self.select_time_page = SelectTimePage()  # Add Select Time Page

        # Navigation logic (example)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.game_page)
        self.stacked_widget.addWidget(self.select_time_page)

        self.setCentralWidget(self.stacked_widget)

    def navigate_to_select_time_page(self):
        self.stacked_widget.setCurrentWidget(self.select_time_page)
