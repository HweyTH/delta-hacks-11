import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.pages.home_page import HomePage
from gui.pages.game_page import GamePage
from gui.pages.result_page import ResultPage


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integrated Navigation App")
        self.setFixedSize(800, 600)

        # Set up the stacked widget for navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.home_page = HomePage(self.navigate_to_game_page)
        self.stacked_widget.addWidget(self.home_page)

        # Show the home page initially
        self.stacked_widget.setCurrentWidget(self.home_page)

    def navigate_to_game_page(self, selected_time):
        """Navigate to the Game Page with the selected time."""
        self.game_page = GamePage(self, selected_time, self.navigate_to_result_page)
        self.stacked_widget.addWidget(self.game_page)
        self.stacked_widget.setCurrentWidget(self.game_page)

    def navigate_to_result_page(self):
        """Navigate to the Result Page."""
        self.result_page = ResultPage(self)
        self.stacked_widget.addWidget(self.result_page)
        self.stacked_widget.setCurrentWidget(self.result_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())