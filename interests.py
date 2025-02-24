import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QScrollArea, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

class InterestsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_interests = []  # List to store user-entered interests

        # Main layout to hold everything
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background image label
        self.background_label = QLabel(self)
        self.original_pixmap = QPixmap("1.png")  # Replace with your image file

        # Light white box container
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 20px;")

        # Overlay layout for all content
        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setAlignment(Qt.AlignCenter)
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        # Input Section
        input_layout = QHBoxLayout()
        self.interest_input = QLineEdit()
        self.interest_input.setPlaceholderText("Type your interest here and press Add")
        self.interest_input.setFixedWidth(400)
        input_layout.addWidget(self.interest_input, alignment=Qt.AlignCenter)

        self.add_button = QPushButton("Add")
        self.add_button.setFixedWidth(100)
        self.add_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 8px; border-radius: 5px;"
        )
        self.add_button.clicked.connect(self.add_interest)
        input_layout.addWidget(self.add_button)

        overlay_layout.addLayout(input_layout)

        # Selected Interests Display
        self.selected_label = QLabel("Your Interests:")
        self.selected_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.selected_label.setStyleSheet("color: #40797d;")
        overlay_layout.addWidget(self.selected_label)

        self.selected_list = QListWidget()
        self.selected_list.setFixedWidth(400)
        overlay_layout.addWidget(self.selected_list, alignment=Qt.AlignCenter)

        # Remove Button
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setFixedWidth(200)
        self.remove_button.setStyleSheet(
            "background-color: #d9534f; color: white; font-weight: bold; padding: 8px; border-radius: 5px;"
        )
        self.remove_button.clicked.connect(self.remove_selected_interest)
        overlay_layout.addWidget(self.remove_button, alignment=Qt.AlignCenter)

        # Next Button
        self.next_button = QPushButton("Next")
        self.next_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.next_button.setFixedWidth(200)
        self.next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.next_button.clicked.connect(self.next_page)
        overlay_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        # Add the overlay container and background
        main_layout.addWidget(self.background_label)
        self.update_overlay_position_and_size()

    def resizeEvent(self, event):
        self.resize_background_image()
        self.update_overlay_position_and_size()
        super().resizeEvent(event)

    def resize_background_image(self):
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setFixedSize(self.size())

    def update_overlay_position_and_size(self):
        if self.overlay_container:
            new_width = int(self.width() * 0.5)
            new_height = int(self.height() * 0.8)
            self.overlay_container.resize(new_width, new_height)
            self.overlay_container.move(
                (self.width() - new_width) // 2,
                (self.height() - new_height) // 2
            )

    def add_interest(self):
        interest = self.interest_input.text().strip()
        if interest:
            self.selected_interests.append(interest)
            self.selected_list.addItem(interest)
            self.interest_input.clear()

    def remove_selected_interest(self):
        selected_items = self.selected_list.selectedItems()
        for item in selected_items:
            self.selected_interests.remove(item.text())
            self.selected_list.takeItem(self.selected_list.row(item))

    def populate_interests(self, interests):
        self.selected_interests = interests
        self.selected_list.clear()
        for interest in interests:
            self.selected_list.addItem(interest)

    def next_page(self):
        self.parent().move_to_next_section("interests", self.selected_interests)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InterestsPage()
    window.show()
    sys.exit(app.exec_())
