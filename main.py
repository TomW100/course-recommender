import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from interests import InterestsPage
from predicted_grades import PredictedGradesPage
from location import LocationPage
from hobbies import HobbiesPage
from strengths import StrengthsPage
from career_goals import CareerGoalsPage
from results import ResultsPage
from start_page import StartPage
from course_preferences_page import CoursePreferencesPage
from paragraph_input_page import ParagraphPage as ParagraphInputPage
from paragraph_results_page import ParagraphResultsPage  # Import the paragraph results page


class CourseRecommendationApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.data = {}  # Dictionary to store user input data

        # Background image label
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)

        # Dictionary to map pages to their background images
        self.page_backgrounds = {
            StartPage: "start.png",
            InterestsPage: "1.png",
            PredictedGradesPage: "2.png",
            CoursePreferencesPage: "9.png",
            LocationPage: "4.png",
            HobbiesPage: "5.png",
            StrengthsPage: "10.png",
            CareerGoalsPage: "7.png",
            ResultsPage: "8.png",
            ParagraphInputPage: "13.png",
            ParagraphResultsPage: "13.png",
        }

        # Create all pages
        self.start_page = StartPage(self)
        self.interests_page = InterestsPage(self)
        self.grades_page = PredictedGradesPage(self)
        self.preferences_page = CoursePreferencesPage(self)
        self.location_page = LocationPage(self)
        self.hobbies_page = HobbiesPage(self)
        self.strengths_page = StrengthsPage(self)
        self.career_goals_page = CareerGoalsPage(self)
        self.results_page = ResultsPage(self)
        self.paragraph_input_page = ParagraphInputPage(self)  # Paragraph input page
        self.paragraph_results_page = ParagraphResultsPage(self)  # Paragraph results page

        # Add pages to the QStackedWidget
        self.addWidget(self.start_page)
        self.addWidget(self.interests_page)
        self.addWidget(self.grades_page)
        self.addWidget(self.preferences_page)
        self.addWidget(self.location_page)
        self.addWidget(self.hobbies_page)
        self.addWidget(self.strengths_page)
        self.addWidget(self.career_goals_page)
        self.addWidget(self.results_page)
        self.addWidget(self.paragraph_input_page)
        self.addWidget(self.paragraph_results_page)

        # Set the initial page and background
        self.setCurrentWidget(self.start_page)
        self.update_background()

    def resizeEvent(self, event):
        """Handle resizing of the window and adjust the background image."""
        self.resize_background()
        super().resizeEvent(event)

    def resize_background(self):
        """Resize the current background image to fill the window."""
        current_page = type(self.currentWidget())
        background_path = self.page_backgrounds.get(current_page)
        if background_path:
            pixmap = QPixmap(background_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                self.background_label.setPixmap(scaled_pixmap)
                self.background_label.setGeometry(0, 0, self.width(), self.height())

    def update_background(self):
        """Update the background image when the page changes."""
        self.resize_background()

    def reset_all_data(self):
        """Clear all stored user inputs to start a new recommendation process."""
        self.data = {}

    def move_to_next_section(self, section_name, section_data=None):
        """Store the current section's data and navigate to the next page."""
        if section_name != "start":
            self.data[section_name] = section_data

        # Determine which page to show next
        if self.currentWidget() == self.start_page:
            self.setCurrentWidget(self.interests_page)
        elif self.currentWidget() == self.interests_page:
            self.setCurrentWidget(self.grades_page)
        elif self.currentWidget() == self.grades_page:
            self.setCurrentWidget(self.preferences_page)
        elif self.currentWidget() == self.preferences_page:
            self.setCurrentWidget(self.location_page)
        elif self.currentWidget() == self.location_page:
            self.setCurrentWidget(self.hobbies_page)
        elif self.currentWidget() == self.hobbies_page:
            self.setCurrentWidget(self.strengths_page)
        elif self.currentWidget() == self.strengths_page:
            self.setCurrentWidget(self.career_goals_page)
        elif self.currentWidget() == self.career_goals_page:
            # Display the standard recommendation results
            self.display_results()
        elif self.currentWidget() == self.paragraph_input_page:
            # Display the paragraph-based results
            self.display_paragraph_results()

        # Update the background image for the new page
        self.update_background()

    def display_results(self):
        """Pass the collected user inputs to the ResultsPage for recommendations."""
        self.results_page.display_recommendations(self.data)
        self.setCurrentWidget(self.results_page)
        self.update_background()

    def display_paragraph_results(self):
        """Navigate to the results page for paragraph input."""
        paragraph_text = self.data.get("paragraph", "")
        self.paragraph_results_page.display_results(paragraph_text)
        self.setCurrentWidget(self.paragraph_results_page)
        self.update_background()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseRecommendationApp()
    window.setWindowTitle("University Course Recommendation")
    window.setGeometry(100, 100, 800, 600)  # Set a default window size
    window.show()
    sys.exit(app.exec_())
