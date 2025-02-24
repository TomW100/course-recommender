from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class ParagraphPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Background image label
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("12.png")  # Replace with your background image file
        self.background_label.setScaledContents(True)

        # Add background to the main layout
        self.main_layout.addWidget(self.background_label)

        # Overlay container (white box) for all content
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 10px;")
        self.overlay_container.setGeometry(100, 100, 600, 400)  # Default size for the white box

        # Overlay layout for all content
        self.overlay_layout = QVBoxLayout(self.overlay_container)
        self.overlay_layout.setContentsMargins(20, 20, 20, 20)
        self.overlay_layout.setSpacing(20)

        # Instructions
        self.instructions = QLabel("Write a paragraph about yourself:")
        self.instructions.setFont(QFont("Arial", 14, QFont.Bold))
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setStyleSheet("color: #40797d; font-weight: bold;")
        self.overlay_layout.addWidget(self.instructions)

        # Text box for paragraph input
        self.paragraph_textbox = QTextEdit()
        self.paragraph_textbox.setFont(QFont("Arial", 12))
        self.paragraph_textbox.setPlaceholderText("Describe your interests, career goals, and strengths...")
        self.paragraph_textbox.setFixedHeight(250)  # Slightly larger text box height
        self.paragraph_textbox.setStyleSheet(
            "border: 1px solid black; border-radius: 4px; background-color: #f9f9f9; padding: 8px; color: black;"
        )
        self.overlay_layout.addWidget(self.paragraph_textbox, alignment=Qt.AlignCenter)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFont(QFont("Arial", 14))
        self.submit_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.submit_button.clicked.connect(self.submit_paragraph)
        self.overlay_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        """Handle window resizing and dynamically adjust the background and white box."""
        self.resize_background_image()
        self.update_overlay_position_and_size()
        super().resizeEvent(event)

    def resize_background_image(self):
        """Resize the background image to cover the entire window."""
        if not self.background_pixmap.isNull():
            self.background_label.setPixmap(
                self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            )
            self.background_label.setGeometry(0, 0, self.width(), self.height())

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

    def submit_paragraph(self):
        """Handle paragraph submission."""
        paragraph_text = self.paragraph_textbox.toPlainText().strip()
        if not paragraph_text:
            # Display an error message if the text box is empty
            error_message = QMessageBox(self)
            error_message.setIcon(QMessageBox.Warning)
            error_message.setWindowTitle("Input Required")
            error_message.setText("Please write something about yourself before submitting.")
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec_()
        else:
            # Pass the paragraph text to the parent for processing
            self.parent().data["paragraph"] = paragraph_text
            self.parent().paragraph_results_page.display_results(paragraph_text)
            self.parent().setCurrentWidget(self.parent().paragraph_results_page)
