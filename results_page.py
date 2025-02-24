class ResultsPage(QWidget):
    def __init__(self, parent=None, results=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        # Title
        self.title = QLabel("Recommended University Courses")
        self.layout.addWidget(self.title)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Course Name", "University", "Match Score"])
        self.layout.addWidget(self.results_table)

        # Populate table with initial results
        if results:
            self.populate_table(results)

        self.setLayout(self.layout)

    def populate_table(self, results):
        self.results_table.setRowCount(len(results))
        for row_idx, result in enumerate(results):
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(result["Course Name"]))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(result["University"]))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(str(result["Match Score"])))
