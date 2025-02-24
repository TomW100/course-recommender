from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QScrollArea,
    QHeaderView, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QProgressBar, QDialog, QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from sklearn.feature_extraction.text import TfidfVectorizer  # For NLP-based keyword extraction
from sklearn.metrics.pairwise import cosine_similarity  # (If used elsewhere)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import nltk
import random  # For randomly choosing templates
from recommendation_model import RecommendationExplanationSystem

# Ensure NLTK is initialized
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")


class ResultsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data = {}
        self.results = pd.DataFrame()
        self.results_displayed = 0
        self.batch_size = 15  # Number of results to display per batch
        self.explanation_system = RecommendationExplanationSystem()  # Instantiate explanation system
        self.load_dataset()
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

    def load_dataset(self):
        self.file_path = "combined_university_courses.csv"
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Dataset file '{self.file_path}' not found.")
            return

        if 'Course Title' in self.df.columns:
            self.df['cleaned_description'] = (
                self.df['Course Title'].fillna('') + " " +
                self.df['Qualification'].fillna('') + " " +
                self.df['University Name'].fillna('')
            )
        else:
            QMessageBox.critical(self, "Error", "Dataset must contain a 'Course Title' column.")
            return

        # Preprocess UCAS Tariff Points to handle ranges
        if 'UCAS Tariff Points' in self.df.columns:
            def extract_lower_bound(value):
                try:
                    if '-' in value:  # Handle ranges like "104-112"
                        return float(value.split('-')[0])
                    return float(value)  # Handle single numeric values
                except (ValueError, TypeError):
                    return None  # Return None for invalid entries

            self.df['UCAS Tariff Points'] = self.df['UCAS Tariff Points'].apply(
                lambda x: extract_lower_bound(str(x).strip())
            )

        # Preprocess descriptions
        self.df['cleaned_description'] = self.df['cleaned_description'].apply(self.preprocess_text)

        # Load university rankings (focus on the first two columns only)
        try:
            self.rankings_df = pd.read_csv("UK_University_Rankings_-_Full_Inclusive_List.csv", usecols=[0, 1], header=0)
            self.rankings_df.columns = ["Rank", "University"]  # Rename columns for clarity
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Rankings file not found.")
            self.rankings_df = pd.DataFrame(columns=["Rank", "University"])

        # Ensure column names match
        if "University" not in self.rankings_df.columns:
            QMessageBox.critical(self, "Error", "Rankings file must contain a 'University' column.")
            return

        # Merge rankings with main dataset
        self.df = self.df.merge(
            self.rankings_df, left_on="University Name", right_on="University", how="left"
        ).fillna({"Rank": float("inf")})  # Assign infinity for missing ranks

        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['cleaned_description'])


    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Sorting Dropdown
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

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(10)  # Includes "University Rank" and "Explanation"
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

        # Connect cell click signal to popup handler
        self.results_table.cellClicked.connect(self.show_explanation_popup_from_table)

        # Scrollable Area
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

        # Load More Button
        self.load_more_button = QPushButton("Load More Results")
        self.load_more_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.load_more_button.clicked.connect(self.load_more_results)
        self.layout.addWidget(self.load_more_button, alignment=Qt.AlignCenter)

        # "Get Another Recommendation" Button
        self.new_recommendation_button = QPushButton("Get Another Recommendation")
        self.new_recommendation_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.new_recommendation_button.clicked.connect(self.get_another_recommendation)
        self.new_recommendation_button.setMaximumWidth(300)
        self.layout.addWidget(self.new_recommendation_button, alignment=Qt.AlignCenter)

        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)



    def show_explanation_popup_from_table(self, row, column):
        """Handle clicking on the explanation cell to show a popup."""
        explanation_column_index = 8  # Column index for Explanation
        if column == explanation_column_index:  # Check if the clicked cell is in the Explanation column
            explanation_item = self.results_table.item(row, column)
            if explanation_item:  # Ensure the cell is not empty
                explanation_text = explanation_item.text()
                self.show_explanation_popup(explanation_text)  # Reuse the existing popup method

    def show_explanation_popup(self, explanation):
        """Show the explanation in a popup dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Course Explanation")
        dialog_layout = QVBoxLayout(dialog)

        explanation_header = QLabel("<b>Recommended Course Explanation:</b>")
        explanation_header.setStyleSheet("padding: 5px; font-size: 16px;")
        dialog_layout.addWidget(explanation_header)

        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignLeft)
        explanation_label.setStyleSheet("padding: 10px; font-size: 14px;")
        dialog_layout.addWidget(explanation_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        dialog_layout.addWidget(buttons)

        dialog.exec_()

    def show_explanation_popup_from_table(self, row, column):
        """Handle clicking on the explanation cell to show a popup."""
        explanation_column_index = 8  # Column index for Explanation
        if column == explanation_column_index:  # Check if the clicked cell is in the Explanation column
            explanation_item = self.results_table.item(row, column)
            if explanation_item:  # Ensure the cell is not empty
                explanation_text = explanation_item.text()
                self.show_explanation_popup(explanation_text)  # Reuse the existing popup method

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

    def sort_results(self):
        """Sort only the first 15 results based on dropdown selection."""
        
        # Ensure rankings are preloaded for all results
        if "Rank" not in self.results.columns:
            self.results = self.results.merge(
                self.rankings_df, left_on="University Name", right_on="University", how="left"
            )

        # **Fix: Convert Rank to numeric safely**
        self.results["Rank"] = self.results["Rank"].replace(">131", 999)  # Replace '>131' with a high numeric value
        self.results["Rank"] = pd.to_numeric(self.results["Rank"], errors="coerce").fillna(999).astype(int)  # Convert safely

        if self.sorting_dropdown.currentIndex() == 0:  # Sort by Compatibility
            # Sort by similarity score in descending order
            self.results.sort_values(by="similarity_score", ascending=False, inplace=True)
            self.results_displayed = 0
            self.results_table.setRowCount(0)
            self.load_more_results()

        elif self.sorting_dropdown.currentIndex() == 1:  # Sort by Best Universities
            # Extract the top 15 most compatible universities
            top_compatibility_results = self.results.head(15).copy()

            # **Ensure rankings are formatted correctly before sorting**
            top_compatibility_results["Rank"] = top_compatibility_results["Rank"].apply(
                lambda x: ">131" if x == 999 else str(int(x))
            )

            # Sort by University Rank (low numbers first, "999" as highest rank)
            sorted_results = top_compatibility_results.sort_values(by="Rank", ascending=True, key=lambda x: x.replace(">131", "999").astype(int))

            # Reset the table and load sorted results
            self.results_table.setRowCount(0)
            self.results_displayed = 0

            # Load only the sorted top 15 results
            for _, row in sorted_results.iterrows():
                row_index = self.results_table.rowCount()
                self.results_table.insertRow(row_index)

                for col_index in range(self.results_table.columnCount()):
                    if col_index == 7:  # Course URL
                        link_label = QLabel(f'<a href="{row["Course URL"]}" style="color: blue; text-decoration: underline;">Link</a>')
                        link_label.setOpenExternalLinks(True)
                        link_label.setAlignment(Qt.AlignCenter)
                        self.results_table.setCellWidget(row_index, col_index, link_label)

                    elif col_index == 8:  # Explanation column
                        explanation_button = QPushButton("Click Here")
                        explanation_button.setStyleSheet(
                            "background-color: #40797d; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
                        )
                        explanation_button.clicked.connect(lambda _, e=row["Explanation"]: self.show_explanation_popup(e))
                        self.results_table.setCellWidget(row_index, col_index, explanation_button)

                    elif col_index == 9:  # University Rank
                        rank_text = row["Rank"]
                        rank_label = QLabel(rank_text)
                        rank_label.setAlignment(Qt.AlignCenter)
                        self.results_table.setCellWidget(row_index, col_index, rank_label)

                    elif col_index == 0:  # Similarity Score
                        progress_bar = QProgressBar()
                        progress_bar.setRange(0, 100)
                        progress_bar.setValue(int(row["similarity_score"] * 100))

                        percentage = int(row["similarity_score"] * 100)
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

                    else:
                        value = row[self.results.columns[col_index]]
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignCenter)
                        table_item.setToolTip(str(value))  # Add tooltip for long text
                        self.results_table.setItem(row_index, col_index, table_item)

        else:
            QMessageBox.critical(self, "Error", "Rankings data is missing or incorrectly formatted.")



    def generate_dynamic_explanation(self, row):
        """Generate explanation dynamically based on the row data."""
        course_title = row.get("Course Title", "Unknown Course")
        university = row.get("University Name", "Unknown University")
        similarity_score = row.get("similarity_score", 0.0)

        combined_user_input = " ".join([
            " ".join(self.data.get('interests', [])),
            self.data.get('hobbies', ''),
            " ".join(self.data.get('strengths', [])),
            self.data.get('career_goals', '')
        ])

        # Extract keywords from course title and user input
        from sklearn.feature_extraction.text import TfidfVectorizer
        documents = [combined_user_input, course_title]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()
        user_keywords = {feature_names[i]: tfidf_matrix[0, i] for i in range(len(feature_names)) if tfidf_matrix[0, i] > 0.1}
        course_keywords = {feature_names[i]: tfidf_matrix[1, i] for i in range(len(feature_names)) if tfidf_matrix[1, i] > 0.1}

        common_keywords = set(user_keywords.keys()).intersection(set(course_keywords.keys()))
        if common_keywords:
            context_match = f"This program directly matches your interest in {' and '.join(common_keywords)}."
        else:
            context_match = "This course offers a unique opportunity to explore new areas aligned with your aspirations."

        user_input = f"your interests in {', '.join(self.data.get('interests', ['various topics']))}, " \
                    f"your hobbies such as {self.data.get('hobbies', 'exploring new activities')}, " \
                    f"your strengths like {', '.join(self.data.get('strengths', ['being adaptable']))}, " \
                    f"and your career goals of {self.data.get('career_goals', 'finding a fulfilling career')}."

        explanation = self.explanation_system.generate_explanation(
            course_title=course_title,
            university=university,
            similarity_score=similarity_score,
            user_input=user_input,
            context_match=context_match
        )
        return explanation


    def sort_table(self, sort_by):
        """Sort table based on user selection."""
        if sort_by == "Compatibility":
            # Sort by similarity_score descending
            self.results = self.results.sort_values(by="similarity_score", ascending=False)
        elif sort_by == "Best Universities":
            # Sort by University Rank ascending
            self.results = self.results.sort_values(by="University Rank", ascending=True)

        # Refresh the table display
        self.results_table.setRowCount(0)
        self.results_displayed = 0
        self.load_more_results()

    
    def display_results(self):
        """Display results in the table."""
        self.results_table.setRowCount(0)
        for _, row in self.results.iterrows():
            row_idx = self.results_table.rowCount()
            self.results_table.insertRow(row_idx)

            for col_idx, value in enumerate(row):
                if col_idx == 7:  # Course URL as a clickable link
                    link = QLabel(f'<a href="{value}">Link</a>')
                    link.setOpenExternalLinks(True)
                    self.results_table.setCellWidget(row_idx, col_idx, link)
                elif col_idx == 9:  # Explanation column
                    explanation_button = QPushButton("View Explanation")
                    explanation_button.clicked.connect(lambda: self.show_explanation_popup(row["Explanation"]))
                    self.results_table.setCellWidget(row_idx, col_idx, explanation_button)
                else:
                    self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                    

    def display_recommendations(self, inputs):
        """Generate and display results, ensuring rankings are included beforehand."""
        
        # Debugging: Print inputs received
        print("Debug: Inputs received in ResultsPage:", inputs)

        # Combine user inputs into a single text input for the recommendation engine
        combined_input = " ".join(
            [
                str(inputs.get('interests', '')).strip(),
                str(inputs.get('hobbies', '')).strip(),
                str(inputs.get('strengths', '')).strip(),
                str(inputs.get('career_goals', '')).strip()
            ]
        ).strip()

        # Fallback if combined input is empty
        if not combined_input:
            combined_input = "general interests and goals"

        # Debugging: Print the combined input
        print("Debug: Combined input for recommendations:", combined_input)

        # Calculate UCAS points based on grades
        ucas_points = self.calculate_ucas_points(inputs.get('grades', []))
        print(f"Debug: Calculated UCAS points: {ucas_points}")  # Debugging

        # Get course recommendations
        self.results = self.recommend_courses(combined_input, ucas_points)

        # **Ensure university rankings are preloaded and merged BEFORE displaying the table**
        if "Rank" not in self.results.columns:
            self.results = self.results.merge(
                self.rankings_df, left_on="University Name", right_on="University", how="left"
            )

        # **Fill missing rankings with a default high value and convert to appropriate format**
        self.results["Rank"] = self.results["Rank"].fillna(999).astype(float)

        # **Ensure rank formatting is done before rendering**
        self.results["Rank"] = self.results["Rank"].apply(
            lambda x: ">131" if x == 999 else int(x)
        )

        # Reset display
        self.results_displayed = 0
        self.results_table.setRowCount(0)

        # Check if recommendations are available
        if self.results.empty:
            QMessageBox.information(self, "No Results", "No courses found matching your criteria.")
            self.results_table.setVisible(False)
            self.load_more_button.setVisible(False)
        else:
            # Debugging: Print the first few rows of results
            print("Debug: Top results after merging rankings:")
            print(self.results.head())

            # Display the results
            self.results_table.setVisible(True)
            self.load_more_button.setVisible(True)
            self.load_more_results()


    def calculate_ucas_points(self, grades):
        ucas_table = {1: 16, 2: 24, 3: 32, 4: 40, 5: 48, 6: 56}
        total_points = 0

        for grade_entry in grades:
            grade = grade_entry["grade"]
            confidence_factor = grade_entry["confidence"]
            grade_points = ucas_table.get(grade, 0)
            adjusted_points = grade_points * confidence_factor
            total_points += adjusted_points

        return total_points

    def recommend_courses(self, combined_input, ucas_points=None):
        """Recommend courses based on inputs."""
        if ucas_points is not None:
            self.df = self.df[
                self.df['UCAS Tariff Points']
                .fillna(0)
                .astype(float)
                .le(ucas_points)
            ]

        selected_durations = self.data.get('preferences', {}).get('durations', [])
        if selected_durations:
            self.df = self.df[self.df['Duration'].isin(selected_durations)]

        selected_qualifications = self.data.get('preferences', {}).get('qualifications', [])
        if selected_qualifications:
            self.df = self.df[self.df['Qualification'].isin(selected_qualifications)]

        if self.df.empty:
            return pd.DataFrame()

        # Calculate similarity scores
        filtered_tfidf_matrix = self.vectorizer.transform(self.df['cleaned_description'])
        user_input_vector = self.vectorizer.transform([combined_input.lower()])
        similarities = cosine_similarity(user_input_vector, filtered_tfidf_matrix)[0]
        self.df['similarity_score'] = similarities

        # Load university rankings
        university_rankings = pd.read_csv("UK_University_Rankings_-_Full_Inclusive_List.csv")
        university_rankings.columns = university_rankings.columns.str.strip()
        university_rankings = university_rankings.set_index("University")["Average Rank"].to_dict()

        # Map rankings to the main dataframe
        self.df["University Rank"] = self.df["University Name"].map(university_rankings).fillna(float("inf"))

        # Sort data initially by similarity score and rank
        recommendations = self.df.drop_duplicates(subset=["Course Title", "University Name"])
        recommendations = recommendations.sort_values(
            by=["similarity_score", "University Rank"], ascending=[False, True]
        )

        # Set correct column order
        recommendations = recommendations[
            ["similarity_score", "Course Title", "University Name", "Duration",
            "Qualification", "Study Mode", "UCAS Tariff Points", "Course URL", "University Rank"]
        ]
        recommendations["Explanation"] = ""  # Add Explanation at the end

        return recommendations



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

    def load_more_results(self):
        """Load more results incrementally, adding explanations dynamically."""
        end_index = self.results_displayed + self.batch_size

        print(f"Displaying results from index {self.results_displayed} to {end_index}")
        print(self.results.iloc[self.results_displayed:end_index])

        for _, row in self.results.iloc[self.results_displayed:end_index].iterrows():
            row_index = self.results_table.rowCount()
            self.results_table.insertRow(row_index)

            for col_index in range(self.results_table.columnCount()):
                if col_index == 7:  # Course URL column
                    link_label = QLabel(f'<a href="{row["Course URL"]}" style="color: blue; text-decoration: underline;">Link</a>')
                    link_label.setOpenExternalLinks(True)
                    link_label.setAlignment(Qt.AlignCenter)
                    self.results_table.setCellWidget(row_index, col_index, link_label)

                elif col_index == 9:  # University Rank column
                    rank_value = row.get("Rank", "N/A")

                    # **Fix: Handle ">131" properly**
                    if isinstance(rank_value, str) and rank_value == ">131":
                        rank_text = ">131"
                    elif pd.isna(rank_value) or rank_value == "N/A":
                        rank_text = "N/A"
                    else:
                        try:
                            rank_text = str(int(float(rank_value)))
                        except ValueError:
                            rank_text = "N/A"  # Fallback in case of unexpected values

                    rank_item = QTableWidgetItem(rank_text)
                    rank_item.setTextAlignment(Qt.AlignCenter)
                    rank_item.setToolTip(rank_text)
                    self.results_table.setItem(row_index, col_index, rank_item)

                elif col_index == 8:  # Explanation column
                    explanation_button = QPushButton("Click Here")
                    explanation_button.setStyleSheet(
                        "background-color: #40797d; color: white; font-weight: bold; padding: 5px; border-radius: 5px;"
                    )
                    explanation_button.clicked.connect(lambda _, e=row["Explanation"]: self.show_explanation_popup(e))
                    self.results_table.setCellWidget(row_index, col_index, explanation_button)

                elif col_index == 0:  # Similarity Score column
                    progress_bar = QProgressBar()
                    progress_bar.setRange(0, 100)
                    progress_bar.setValue(int(row["similarity_score"] * 100))

                    percentage = int(row["similarity_score"] * 100)
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

                else:
                    value = row[self.results.columns[col_index]]
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignCenter)
                    table_item.setToolTip(str(value))  # Add tooltip for long text
                    self.results_table.setItem(row_index, col_index, table_item)

        self.results_displayed = end_index

        if self.results_displayed >= len(self.results):
            self.load_more_button.setVisible(False)




    def get_another_recommendation(self):
        """Return to the start page."""
        self.parent.reset_all_data()
        self.parent.setCurrentWidget(self.parent.start_page)
