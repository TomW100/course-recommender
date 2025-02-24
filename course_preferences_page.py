from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QScrollArea, QGroupBox, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CoursePreferencesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.selected_preferences = {"durations": [], "qualifications": []}

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(30)

        # Spacer at the top for centering and pushing everything down
        self.main_layout.addSpacerItem(QSpacerItem(20, 250, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Spacer below title for better spacing
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Scroll Area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(450, 350)  # Adjust size for better layout
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(50)  # Increase spacing between sections

        # Add duration options
        self.duration_group = QGroupBox("Preferred Course Durations")
        self.duration_group.setFont(QFont("Arial", 16, QFont.Bold))
        self.duration_group.setStyleSheet("color: #40797d;")
        duration_layout = QVBoxLayout(self.duration_group)

        # Spacer inside the group box for separation
        duration_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.duration_checkboxes = []
        durations = ["3 Years", "4 Years", "5+ Years"]
        for duration in durations:
            checkbox = QCheckBox(duration)
            checkbox.setFont(QFont("Arial", 14))
            self.duration_checkboxes.append(checkbox)
            duration_layout.addWidget(checkbox)
        content_layout.addWidget(self.duration_group)

        # Spacer below duration section for better separation
        content_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Add qualification options
        self.qualification_group = QGroupBox("Preferred Qualifications")
        self.qualification_group.setFont(QFont("Arial", 16, QFont.Bold))
        self.qualification_group.setStyleSheet("color: #40797d;")
        qualification_layout = QVBoxLayout(self.qualification_group)

        # Spacer inside the group box for separation
        qualification_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.qualification_checkboxes = []
        qualifications = [
            "Bachelor's Degree (e.g., BSc, BA)",
            "Master's Degree (e.g., MSc, MA)",
            "Doctorate (e.g., PhD, DPhil)",
        ]
        for qualification in qualifications:
            checkbox = QCheckBox(qualification)
            checkbox.setFont(QFont("Arial", 14))
            self.qualification_checkboxes.append(checkbox)
            qualification_layout.addWidget(checkbox)
        content_layout.addWidget(self.qualification_group)


        # Add content widget to the scroll area
        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area, alignment=Qt.AlignCenter)

        # Spacer for better positioning of the Next button
        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Next Button
        next_button = QPushButton("Next")
        next_button.setFont(QFont("Arial", 14))
        next_button.setFixedWidth(200)
        next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        next_button.clicked.connect(self.next_page)
        self.main_layout.addWidget(next_button, alignment=Qt.AlignCenter)

        # Spacer at the bottom for centering
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def next_page(self):
        """
        Collects selected preferences and moves to the next page.
        """
        # Collect selected durations
        self.selected_preferences["durations"] = [
            checkbox.text() for checkbox in self.duration_checkboxes if checkbox.isChecked()
        ]

        # Collect selected qualifications
        self.selected_preferences["qualifications"] = [
            checkbox.text() for checkbox in self.qualification_checkboxes if checkbox.isChecked()
        ]

        # Pass the preferences to the parent
        self.parent.data["preferences"] = self.selected_preferences

        # Navigate to the next page
        self.parent.move_to_next_section("preferences", self.selected_preferences)
