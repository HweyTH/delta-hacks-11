from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from stats import get_stats, visualize_stats
from functions import pil_to_pixmap


class ResultPage(QWidget):
    def __init__(self, navigate_to_home, parent=None):
        """
        Initializes the result page.

        Args:
            navigate_to_home (callable): A function to navigate to the home page.
        """
        super().__init__(parent)

        self.navigate_to_home = navigate_to_home  # Function to navigate back to the home page

        # Fetch stats using get_stats()
        avg_wpm, accuracy = get_stats()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        self.setStyleSheet("background-color: #1e1e2e; color: #e0e0e0;")

        # Logo (Clickable Label)
        logo_label = QLabel("SignStreak")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffc400;")
        logo_label.setFont(QFont("Arial", 20))
        logo_label.setCursor(Qt.PointingHandCursor)  # Fix 'cursor' warning
        logo_label.mousePressEvent = self.on_logo_click  # Add click event handler
        main_layout.addWidget(logo_label)

        # Stats Layout
        stats_layout = QVBoxLayout()

        # WPM and Accuracy
        wpm_label = QLabel(f"wpm\n{avg_wpm}")
        wpm_label.setAlignment(Qt.AlignLeft)
        wpm_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        stats_layout.addWidget(wpm_label)

        acc_label = QLabel(f"acc\n{accuracy}%")
        acc_label.setAlignment(Qt.AlignLeft)
        acc_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffc400;")
        stats_layout.addWidget(acc_label)

        # Visualization Plot
        pil_image = visualize_stats()
        pixmap = pil_to_pixmap(pil_image)
        plot_label = QLabel()
        plot_label.setPixmap(pixmap)
        stats_layout.addWidget(plot_label)

        # Add Stats Layout to Main Layout
        main_layout.addLayout(stats_layout)

        # Set Main Layout
        self.setLayout(main_layout)

    def on_logo_click(self, event):
        """Handle logo click to navigate back to the home page."""
        self.navigate_to_home()
