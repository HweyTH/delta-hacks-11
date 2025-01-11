import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.pages.home_page import HomePage
from gui.pages.game_page import GamePage


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
