from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QScrollArea,
    QHeaderView, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QProgressBar, 
    QDialog, QDialogButtonBox, QComboBox  # <-- Add QComboBox here
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import nltk

# Ensure NLTK is initialized
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


class ParagraphResultsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data = {}
        self.results = pd.DataFrame()  # Store all results
        self.results_displayed = 0
        self.batch_size = 15  # Number of results to display per batch

        # **Load university rankings once at the start**
        self.rankings_df = self.load_university_rankings()

        # Initialize UI components
        self.init_ui()


    def preprocess_text(self, text):
        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()

        tokens = word_tokenize(text.lower())
        cleaned_tokens = [
            lemmatizer.lemmatize(token)
            for token in tokens if token.isalnum() and token not in stop_words
        ]
        return " ".join(cleaned_tokens)

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # **Sorting Dropdown**
        self.sorting_dropdown = QComboBox()
        self.sorting_dropdown.addItem("Sort by Compatibility")
        self.sorting_dropdown.addItem("Sort by Best Universities")
        self.sorting_dropdown.setStyleSheet(
            """
            background-color: #f9f9f9;
            color: #333;
            font-size: 14px;
            padding: 5px;
            border: 1px solid #40797d;
            border-radius: 5px;
            """
        )
        self.sorting_dropdown.currentIndexChanged.connect(self.sort_results)
        self.layout.addWidget(self.sorting_dropdown, alignment=Qt.AlignCenter)

        # **Results Table with University Rank Column**
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(10)  # Now includes "University Rank"
        self.results_table.setHorizontalHeaderLabels(
            [
                "Compatibility", "Course Title", "University Name", "Duration",
                "Qualification", "Study Mode", "UCAS Points", "Course URL", "Explanation", "University Rank"
            ]
        )
        self.results_table.horizontalHeader().setStretchLastSection(False)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.verticalHeader().setDefaultSectionSize(50)  # Increase row height
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #40797d;
                background-color: #f9f9f9;
                gridline-color: #40797d;
                font-size: 14px;
                border-radius: 10px;
                outline: 0;
            }
            QHeaderView::section {
                background-color: #40797d;
                color: white;
                font-weight: bold;
                border: 1px solid #40797d;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #b4d9dc;
                color: black;
            }
            QTableWidget::item:focus {
                outline: none;
            }
            QTableWidget::alternate {
                background-color: #eef6f7;
            }
        """)

        # **Scrollable Area**
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(400)
        self.scroll_area.setFixedWidth(1200)

        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.addWidget(self.results_table)
        table_layout.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(table_container)
        self.layout.addWidget(self.scroll_area, alignment=Qt.AlignCenter)

        # **Load More Button**
        self.load_more_button = QPushButton("Load More Results")
        self.load_more_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.load_more_button.clicked.connect(self.load_more_results)
        self.layout.addWidget(self.load_more_button, alignment=Qt.AlignCenter)

        # **"Get Another Recommendation" Button**
        self.new_recommendation_button = QPushButton("Get Another Recommendation")
        self.new_recommendation_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.new_recommendation_button.clicked.connect(self.get_another_recommendation)
        self.new_recommendation_button.setMaximumWidth(300)
        self.layout.addWidget(self.new_recommendation_button, alignment=Qt.AlignCenter)

        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)


    def load_university_rankings(self):
        """Load university rankings from a CSV file."""
        try:
            rankings_df = pd.read_csv("UK_University_Rankings_-_Full_Inclusive_List.csv", usecols=[0, 1], header=0)
            rankings_df.columns = ["Rank", "University"]  # Rename columns for clarity
            return rankings_df
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Rankings file not found.")
            return pd.DataFrame(columns=["Rank", "University"])


    def display_results(self, paragraph_text):
        """Generate and display results based on paragraph input."""

        self.results = self.generate_recommendations(paragraph_text)

        # **Ensure rankings are merged before displaying results**
        if "Rank" not in self.results.columns:
            self.results = self.results.merge(
                self.rankings_df, left_on="University Name", right_on="University", how="left"
            )
            self.results["Rank"] = self.results["Rank"].fillna(999).astype(int)

        # **Take only the top 15 compatibility results**
        self.results = self.results.sort_values(by="similarity_score", ascending=False).head(15)

        self.results_displayed = 0
        self.results_table.setRowCount(0)

        if self.results.empty:
            QMessageBox.information(self, "No Results", "No courses found matching your paragraph.")
            self.results_table.setVisible(False)
            self.load_more_button.setVisible(False)
        else:
            self.results_table.setVisible(True)
            self.load_more_button.setVisible(True)

            # **Always start with sorting by compatibility (default)**
            self.sort_results()




    def generate_recommendations(self, paragraph_text):
        """Generate recommendations based on paragraph input."""
        file_path = "combined_university_courses.csv"
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Dataset file '{file_path}' not found.")
            return pd.DataFrame()

        # **Ensure required columns exist**
        required_columns = ['Course Title', 'Qualification', 'University Name', 'Duration', 
                            'Study Mode', 'UCAS Tariff Points', 'Course URL']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            QMessageBox.critical(self, "Error", f"Dataset is missing required columns: {', '.join(missing_columns)}.")
            return pd.DataFrame()

        # **Preprocess course descriptions**
        df['cleaned_description'] = (
            df['Course Title'].fillna('') + " " +
            df['Qualification'].fillna('') + " " +
            df['University Name'].fillna('')
        )
        df['cleaned_description'] = df['cleaned_description'].apply(self.preprocess_text)

        # **Preprocess user paragraph input**
        cleaned_paragraph = self.preprocess_text(paragraph_text)

        # **Calculate similarity using TF-IDF**
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(df['cleaned_description'])
        paragraph_vector = vectorizer.transform([cleaned_paragraph])
        similarities = cosine_similarity(paragraph_vector, tfidf_matrix)[0]

        # **Add similarity scores**
        df['similarity_score'] = similarities
        df = df.drop_duplicates(subset=['Course Title', 'University Name'])

        # **Merge university rankings**
        df = df.merge(self.rankings_df, left_on="University Name", right_on="University", how="left")
        df["Rank"] = df["Rank"].fillna(999).astype(int)  # Default rank is 999 (lowest)

        # **Sort initially by Compatibility and take only the top 15 results**
        recommendations = df[df['similarity_score'] > 0].sort_values(by='similarity_score', ascending=False).head(15)

        # **Generate dynamic explanations**
        recommendations["Explanation"] = recommendations.apply(
            lambda row: f"The course {row['Course Title']} at {row['University Name']} aligns with your interests with a similarity score of {row['similarity_score']:.2f}.",
            axis=1
        )

        return recommendations[
            ['similarity_score', 'Course Title', 'University Name', 'Duration',
            'Qualification', 'Study Mode', 'UCAS Tariff Points', 'Course URL', 'Explanation', 'Rank']
        ]





    def load_more_results(self):
        """Load more results incrementally."""
        end_index = self.results_displayed + self.batch_size

        for _, row in self.results.iloc[self.results_displayed:end_index].iterrows():
            row_index = self.results_table.rowCount()
            self.results_table.insertRow(row_index)

            for col_index, column_name in enumerate(self.results.columns):
                value = row[column_name]

                if column_name == "Course URL":  # Course URL as a clickable link
                    link_label = QLabel(f'<a href="{value}" style="color: blue; text-decoration: underline;">Link</a>')
                    link_label.setOpenExternalLinks(True)
                    link_label.setAlignment(Qt.AlignCenter)
                    self.results_table.setCellWidget(row_index, col_index, link_label)

                elif column_name == "similarity_score":  # Compatibility Score
                    progress_bar = QProgressBar()
                    progress_bar.setRange(0, 100)
                    progress_bar.setValue(int(value * 100))

                    percentage = int(value * 100)
                    color = "green" if percentage >= 50 else "orange" if percentage >= 20 else "red"

                    progress_bar.setStyleSheet(f"""
                        QProgressBar {{
                            border-radius: 5px;
                            text-align: center;
                        }}
                        QProgressBar::chunk {{
                            background-color: {color};
                        }}
                    """)
                    progress_bar.setFormat(f"{percentage}%")
                    progress_bar.setAlignment(Qt.AlignCenter)
                    self.results_table.setCellWidget(row_index, col_index, progress_bar)

                elif column_name == "Explanation":  # Explanation Column
                    btn = QPushButton("Click Here")
                    btn.clicked.connect(lambda _, e=value: self.show_explanation_popup(e))
                    self.results_table.setCellWidget(row_index, col_index, btn)

                elif column_name == "Rank":  # University Rank
                    rank_text = str(value) if value != 999 else ">131"
                    rank_label = QLabel(rank_text)
                    rank_label.setAlignment(Qt.AlignCenter)
                    self.results_table.setCellWidget(row_index, col_index, rank_label)

                else:  # Other columns
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignCenter)
                    table_item.setToolTip(str(value))
                    self.results_table.setItem(row_index, col_index, table_item)

        self.results_displayed = end_index
        if self.results_displayed >= len(self.results):
            self.load_more_button.setVisible(False)



    def sort_results(self):
        """Sort the existing top recommendations based on the dropdown selection."""

        if self.results.empty:
            return  # Don't attempt to sort an empty dataset

        # **Ensure Rank is numeric for sorting**
        if "Rank" in self.results.columns:
            self.results["Rank"] = pd.to_numeric(self.results["Rank"], errors='coerce').fillna(999).astype(int)

        if self.sorting_dropdown.currentIndex() == 0:  # Sort by Compatibility
            # **Sort by similarity_score in descending order (Highest first)**
            self.results = self.results.sort_values(by="similarity_score", ascending=False).head(15)
        elif self.sorting_dropdown.currentIndex() == 1:  # Sort by Best Universities
            # **Sort only the top 15 compatibility results by University Rank (Lowest Rank First)**
            self.results = self.results.sort_values(by="Rank", ascending=True).head(15)

        # **Clear and reload only the sorted results**
        self.results_displayed = 0
        self.results_table.setRowCount(0)
        self.load_more_results()




    def show_explanation_popup(self, explanation):
        """Show the explanation in a popup dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Course Explanation")
        dialog_layout = QVBoxLayout(dialog)

        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignLeft)
        explanation_label.setStyleSheet("padding: 10px; font-size: 14px;")
        dialog_layout.addWidget(explanation_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        dialog_layout.addWidget(buttons)

        dialog.exec_()

    def get_another_recommendation(self):
        """Return to the start page."""
        self.parent.reset_all_data()
        self.parent.setCurrentWidget(self.parent.start_page)

    def get_another_recommendation(self):
        """Return to the start page."""
        self.parent.reset_all_data()
        self.parent.setCurrentWidget(self.parent.start_page)
