from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QScrollArea, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class StrengthsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_strengths = []  # List to store selected strengths

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Background image label
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("10.png")  # Replace with your background image file
        self.background_label.setScaledContents(True)

        # Add background to the main layout
        self.main_layout.addWidget(self.background_label)

        # Overlay container (white box) for all content
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 10px;")

        # Overlay layout for all content
        self.overlay_layout = QVBoxLayout(self.overlay_container)
        self.overlay_layout.setContentsMargins(20, 20, 20, 20)
        self.overlay_layout.setSpacing(20)

        # Instructions
        self.instructions = QLabel("Click on your strengths below to select them or type them into the box below.")
        self.instructions.setFont(QFont("Arial", 14, QFont.Bold))
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setStyleSheet("color: #40797d; font-weight: bold;")
        self.overlay_layout.addWidget(self.instructions)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable Content Container
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignTop)
        container_layout.setSpacing(20)

        # Strengths Grid
        self.strengths_grid = QGridLayout()
        self.strengths_grid.setSpacing(10)

        # List of 40 strengths for 10x4 grid
        strengths = [
            "Leadership", "Teamwork", "Problem-Solving", "Creativity", "Adaptability",
            "Empathy", "Communication", "Critical Thinking", "Time Management", "Collaboration",
            "Resilience", "Decision-Making", "Conflict Resolution", "Organisational Skills", 
            "Attention to Detail", "Strategic Thinking", "Flexibility", "Public Speaking", "Negotiation",
            "Self-Motivation", "Emotional Intelligence", "Technical Skills", "Analytical Thinking", "Project Management",
            "Coaching", "Customer Focus", "Research Skills", "Networking", "Interpersonal Skills",
            "Innovative Thinking", "Goal-Oriented", "Initiative", "Multitasking", "Active Listening",
            "Planning", "Problem Analysis", "Dependability", "Resourcefulness", "Mentoring", "Risk Management"
        ]

        # Add buttons to the grid
        for i, strength in enumerate(strengths):
            button = QPushButton(strength)
            button.setStyleSheet(
                "background-color: #97cfd1; color: black; font-weight: bold; padding: 8px; border-radius: 5px;"
            )
            # Use a function closure to bind the current strength to the button click event
            button.clicked.connect(self.create_button_callback(strength, button))
            row, col = divmod(i, 4)  # Calculate row and column for 10x4 grid
            self.strengths_grid.addWidget(button, row, col)

        container_layout.addLayout(self.strengths_grid)
        scroll_area.setWidget(container_widget)
        self.overlay_layout.addWidget(scroll_area)

        # Textbox for typing strengths
        self.textbox_label = QLabel("Type additional strengths:")
        self.textbox_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.textbox_label.setAlignment(Qt.AlignCenter)
        self.textbox_label.setStyleSheet("color: #40797d; font-weight: bold;")
        self.overlay_layout.addWidget(self.textbox_label)

        self.textbox = QLineEdit()
        self.textbox.setFont(QFont("Arial", 12))
        self.textbox.setPlaceholderText("Enter strengths separated by commas...")
        self.overlay_layout.addWidget(self.textbox)

        # Next Button
        self.next_button = QPushButton("Next")
        self.next_button.setFont(QFont("Arial", 14))
        self.next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.next_button.clicked.connect(self.next_page)
        self.overlay_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        """Handle window resizing and dynamically adjust the background and overlay box."""
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
        """Update the position and size of the overlay box dynamically."""
        if self.overlay_container:
            new_width = int(self.width() * 0.5)  # 60% of the window width
            new_height = int(self.height() * 0.6)  # 70% of the window height
            self.overlay_container.setGeometry(
                (self.width() - new_width) // 2,
                (self.height() - new_height) // 2,
                new_width,
                new_height
            )

    def create_button_callback(self, strength, button):
        """Create a callback function for the button click event."""
        def callback():
            if strength in self.selected_strengths:
                self.selected_strengths.remove(strength)
                button.setStyleSheet(
                    "background-color: #97cfd1; color: black; font-weight: bold; padding: 8px; border-radius: 5px;"
                )
            else:
                self.selected_strengths.append(strength)
                button.setStyleSheet(
                    "background-color: #40797d; color: white; font-weight: bold; padding: 8px; border-radius: 5px;"
                )
        return callback

    def next_page(self):
        """
        Save strengths and go to the next page.
        """
        # Collect typed strengths from the textbox
        typed_strengths = [s.strip() for s in self.textbox.text().split(",") if s.strip()]
        all_strengths = list(set(self.selected_strengths + typed_strengths))  # Combine and remove duplicates

        if not all_strengths:
            QMessageBox.warning(self, "No Selection", "Please select or type at least one strength before proceeding.")
            return

        # Pass selected strengths to the parent widget
        self.parent().move_to_next_section("strengths", all_strengths)


# Run the application for testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = StrengthsPage()
    window.resize(800, 600)  # Set the initial size
    window.show()
    sys.exit(app.exec_())
