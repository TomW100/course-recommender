from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class CareerGoalsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Background image label
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("7.png")  # Replace with your background image file
        self.background_label.setScaledContents(True)

        # Add background to main layout
        self.main_layout.addWidget(self.background_label)

        # Overlay container (white box) for all content
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 10px;")
        self.overlay_container.setGeometry(100, 100, 600, 400)  # Default size for the white box

        # Overlay layout for all content
        self.overlay_layout = QVBoxLayout(self.overlay_container)
        self.overlay_layout.setContentsMargins(20, 20, 20, 20)
        self.overlay_layout.setSpacing(20)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(20)

        # Instructions
        self.instructions = QLabel("Please enter your career goals below:")
        self.instructions.setFont(QFont("Arial", 14, QFont.Bold))
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setStyleSheet("color: #40797d; font-weight: bold;")
        content_layout.addWidget(self.instructions)

        # Text box for career goals
        self.goals_textbox = QTextEdit()
        self.goals_textbox.setFont(QFont("Arial", 12))
        self.goals_textbox.setPlaceholderText("Type your career goals here...")
        self.goals_textbox.setStyleSheet(
            "border: 1px solid #00509E; border-radius: 4px; background-color: #f9f9f9; padding: 8px;"
        )
        content_layout.addWidget(self.goals_textbox, alignment=Qt.AlignCenter)

        # Add the content widget to the scroll area
        scroll_area.setWidget(content_widget)
        self.overlay_layout.addWidget(scroll_area)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setFont(QFont("Arial", 14))
        self.next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.next_button.clicked.connect(self.next_page)
        self.overlay_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        """Handle window resizing and dynamically adjust the white box."""
        self.update_overlay_position_and_size()
        super().resizeEvent(event)

    def update_overlay_position_and_size(self):
        """Keep the white box centered and maintain its size."""
        overlay_width = int(self.width() * 0.5)  # 50% of the window width
        overlay_height = int(self.height() * 0.4)  # 40% of the window height
        self.overlay_container.setGeometry(
            (self.width() - overlay_width) // 2,
            (self.height() - overlay_height) // 2,
            overlay_width,
            overlay_height,
        )

    def populate_career_goals(self, career_goals):
        """
        Populate the career goals text box with the provided data.
        """
        self.goals_textbox.setPlainText(career_goals)

    def next_page(self):
        """
        Handle navigation to the next page and pass career goals data.
        """
        career_goals = self.goals_textbox.toPlainText().strip()

        # Validate input
        if not career_goals:
            error_message = QMessageBox(self)
            error_message.setIcon(QMessageBox.Warning)
            error_message.setWindowTitle("Input Required")
            error_message.setText("Please enter at least one career goal before proceeding.")
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec_()
            return

        # Pass career goals data to the parent widget
        self.parent().move_to_next_section("career_goals", career_goals)


# Run the application for testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = CareerGoalsPage()
    window.resize(800, 600)  # Set the initial size
    window.show()
    sys.exit(app.exec_())
