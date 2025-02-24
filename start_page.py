from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout to hold everything
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background image label
        self.background_label = QLabel(self)
        self.original_pixmap = QPixmap("back17.png")  # Replace with your image file

        # Light white box container
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 20px;")

        # Overlay layout for title and button
        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setAlignment(Qt.AlignTop)
        overlay_layout.setContentsMargins(20, 20, 20, 20)
        overlay_layout.setSpacing(80)  # Further increased spacing to move the button down

        # Button
        self.start_button = QPushButton("Get Your Recommendation")
        self.start_button.setFont(QFont("Arial", 25, QFont.Bold))
        self.start_button.setStyleSheet(
            "background-color: #40797d; color: white; padding: 15px; border-radius: 5px;"
        )
        overlay_layout.addStretch()  # Add more stretch space above the button
        overlay_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        overlay_layout.addStretch()  # Add stretch space below the button
        self.start_button.clicked.connect(self.show_options_dialog)

        # Add the overlay container and background
        main_layout.addWidget(self.background_label)
        self.update_overlay_position_and_size()

    def resizeEvent(self, event):
        """Handle window resizing and dynamically adjust the background and overlay."""
        self.resize_background_image()
        self.update_overlay_position_and_size()
        super().resizeEvent(event)

    def resize_background_image(self):
        """Resize the background image to fit the window while maintaining aspect ratio."""
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setFixedSize(self.size())

    def update_overlay_position_and_size(self):
        """Update the position and size of the overlay box dynamically."""
        if self.overlay_container:
            new_width = int(self.width() * 0.5)  # 50% of the window width
            new_height = int(self.height() * 0.5)  # Further increased height for more spacing
            self.overlay_container.resize(new_width, new_height)
            self.overlay_container.move(
                (self.width() - new_width) // 2,
                (self.height() - new_height) // 2 + 80  # Moved further down by increasing the offset
            )

    def show_options_dialog(self):
        """Show a dialog with options to proceed with the process or provide a paragraph."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Your Recommendation Path")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(400, 200)

        layout = QVBoxLayout(dialog)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Option 1: Seven-stage process
        stages_button = QPushButton("7-Stage Recommendation Process")
        stages_button.setFont(QFont("Arial", 14))
        stages_button.setStyleSheet("background-color: #40797d; color: white; padding: 10px; border-radius: 5px;")
        stages_button.clicked.connect(lambda: self.navigate_to_7_stages(dialog))
        layout.addWidget(stages_button, alignment=Qt.AlignCenter)

        # Option 2: Write a paragraph
        paragraph_button = QPushButton("Write a Paragraph")
        paragraph_button.setFont(QFont("Arial", 14))
        paragraph_button.setStyleSheet("background-color: #40797d; color: white; padding: 10px; border-radius: 5px;")
        paragraph_button.clicked.connect(lambda: self.navigate_to_paragraph(dialog))
        layout.addWidget(paragraph_button, alignment=Qt.AlignCenter)

        dialog.exec_()

    def navigate_to_7_stages(self, dialog):
        """Navigate to the first step of the 7-stage process."""
        dialog.accept()
        self.parent().setCurrentWidget(self.parent().interests_page)

    def navigate_to_paragraph(self, dialog):
        """Navigate to the paragraph input page."""
        dialog.accept()
        self.parent().setCurrentWidget(self.parent().paragraph_input_page)
