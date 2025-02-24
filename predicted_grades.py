from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider, QPushButton, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


class PredictedGradesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grades = []  # List to store all subjects, grades, and confidence

        # Main layout to hold everything
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background image label
        self.background_label = QLabel(self)
        self.original_pixmap = QPixmap("2.png")  # Replace with your image file

        # Light white box container
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 20px;")

        # Overlay layout for all content
        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setAlignment(Qt.AlignTop)
        overlay_layout.setSpacing(30)
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable Content Container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(30)  # Adjust spacing between main components

        # Placeholder for grade inputs
        self.grade_inputs = QVBoxLayout()
        self.grade_inputs.setSpacing(30)  # Adjust spacing between grade input sections
        content_layout.addLayout(self.grade_inputs)

        # Add initial grade input
        self.add_grade_input()

        # Add button
        self.add_button = QPushButton("Add Another Subject")
        self.add_button.setFixedWidth(200)
        self.add_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 8px; border-radius: 5px;"
        )
        self.add_button.clicked.connect(self.add_grade_input)
        content_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.setFixedWidth(200)
        self.next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 8px; border-radius: 5px;"
        )
        self.next_button.clicked.connect(self.next_page)
        content_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        # Add the scrollable content to the scroll area
        scroll_area.setWidget(content_widget)
        overlay_layout.addWidget(scroll_area)

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
            new_width = int(self.width() * 0.6)  # 60% of the window width
            new_height = int(self.height() * 0.4)  # 40% of the window height
            self.overlay_container.resize(new_width, new_height)
            self.overlay_container.move(
                (self.width() - new_width) // 2,
                (self.height() - new_height) // 2
            )

    def add_grade_input(self):
        """
        Adds a new set of input widgets for selecting a subject, grade, and confidence level.
        """
        # Container for new grade input
        grade_input_layout = QVBoxLayout()
        grade_input_layout.setSpacing(20)

        # Subject selector
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        subject_label.setStyleSheet("color: #40797d; font-weight: bold;")
        subject_combo = QComboBox()
        subject_combo.addItems([
            "Accounting", "Ancient History", "Anthropology", "Archaeology", "Art and Design", 
            "Biology", "Business Studies", "Chemistry", "Classical Civilisation", 
            "Computer Science", "Dance", "Design and Technology", "Drama and Theatre", 
            "Economics", "English Language", "English Language and Literature", 
            "English Literature", "Environmental Science", "Film Studies", "French", 
            "Further Mathematics", "Geography", "Geology", "German", "Government and Politics", 
            "Graphic Design", "Greek", "Health and Social Care", "History", 
            "Information Technology", "Italian", "Law", "Mathematics", "Media Studies", 
            "Music", "Music Technology", "Philosophy", "Physical Education", "Physics", 
            "Politics", "Psychology", "Religious Studies", "Sociology", "Spanish", 
            "Statistics", "Textiles", "Travel and Tourism"
        ])
        subject_combo.setFixedWidth(300)
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(subject_combo)
        grade_input_layout.addLayout(subject_layout)

        # Predicted Grade Section
        predicted_grade_layout = QVBoxLayout()
        predicted_grade_layout.setSpacing(15)

        predicted_grade_label = QLabel("Predicted Grade:")
        predicted_grade_label.setStyleSheet("color: #40797d; font-weight: bold;")
        predicted_grade_layout.addWidget(predicted_grade_label, alignment=Qt.AlignLeft)

        grade_slider = QSlider(Qt.Horizontal)
        grade_slider.setRange(1, 6)
        grade_slider.setTickInterval(1)
        grade_slider.setTickPosition(QSlider.TicksBelow)
        grade_slider.setToolTip("Slide to select your predicted grade")
        grade_slider.setStyleSheet("color: #40797d;")
        grade_slider.setFixedWidth(700)  # Reduced width for the grade slider
        predicted_grade_layout.addWidget(grade_slider, alignment=Qt.AlignCenter)  # Center the slider

        # Grade Labels (E to A*)
        grade_labels_layout = QHBoxLayout()
        grade_labels_layout.setSpacing(10)
        grade_labels = ["E", "D", "C", "B", "A", "A*"]
        for label in grade_labels:
            grade_label = QLabel(label)
            grade_label.setAlignment(Qt.AlignCenter)
            grade_label.setStyleSheet("color: #40797d; font-weight: bold;")
            grade_labels_layout.addWidget(grade_label)
        predicted_grade_layout.addLayout(grade_labels_layout)

        grade_input_layout.addLayout(predicted_grade_layout)

        # Confidence Level Section
        confidence_level_layout = QVBoxLayout()
        confidence_level_layout.setSpacing(15)

        confidence_label = QLabel("Confidence Level:")
        confidence_label.setStyleSheet("color: #40797d; font-weight: bold;")
        confidence_level_layout.addWidget(confidence_label, alignment=Qt.AlignLeft)

        confidence_slider = QSlider(Qt.Horizontal)
        confidence_slider.setRange(1, 5)
        confidence_slider.setTickInterval(1)
        confidence_slider.setTickPosition(QSlider.TicksBelow)
        confidence_slider.setToolTip("Slide to set your confidence level")
        confidence_slider.setStyleSheet("color: #40797d;")
        confidence_slider.setFixedWidth(700)  # Reduced width for the confidence slider
        confidence_level_layout.addWidget(confidence_slider, alignment=Qt.AlignCenter)  # Center the slider

        # Confidence Labels (Not very to Very confident)
        confidence_labels_layout = QHBoxLayout()
        confidence_labels_layout.setSpacing(10)
        confidence_labels = ["Not very", "Slightly", "Moderately", "Confident", "Very confident"]
        for label in confidence_labels:
            confidence_label = QLabel(label)
            confidence_label.setAlignment(Qt.AlignCenter)
            confidence_label.setStyleSheet("color: #40797d; font-weight: bold;")
            confidence_labels_layout.addWidget(confidence_label)
        confidence_level_layout.addLayout(confidence_labels_layout)

        grade_input_layout.addLayout(confidence_level_layout)

        # Add grade input layout to the main grade inputs container
        self.grade_inputs.addLayout(grade_input_layout)

        # Store the widgets for later use
        self.grades.append({
            "subject_combo": subject_combo,
            "grade_slider": grade_slider,
            "confidence_slider": confidence_slider
        })


    def next_page(self):
        """
        Collects all input data and sends it to the parent widget before moving to the next page.
        """
        # Confidence adjustment factors
        confidence_adjustment = {
            1: 0.75,  # Not very confident: 75%
            2: 0.9,   # Slightly confident: 90%
            3: 1.0,   # Moderately confident: 100%
            4: 1.0,   # Confident: 100%
            5: 1.5    # Very confident: 150%
        }

        grades_data = []
        for grade_input in self.grades:
            subject = grade_input["subject_combo"].currentText()
            grade = grade_input["grade_slider"].value()
            confidence = grade_input["confidence_slider"].value()

            # Adjust confidence factor
            adjusted_confidence = confidence_adjustment.get(confidence, 1.0)

            grades_data.append({
                "subject": subject,
                "grade": grade,
                "confidence": adjusted_confidence  # Adjusted confidence factor
            })

        # Pass the grades data to the parent widget
        self.parent().move_to_next_section("grades", grades_data)


