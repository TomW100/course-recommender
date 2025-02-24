from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class LocationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_regions = []  # List of selected regions

        # Define universities mapped to their respective regions
        self.university_data = {
            "Scotland": [
                "Abertay University",
                "University of Aberdeen",
                "University of Dundee",
                "University of Edinburgh",
                "University of Glasgow",
                "University of St Andrews",
                "University of Stirling",
                "University of Strathclyde",
                "Heriot-Watt University",
                "Edinburgh Napier University",
                "Glasgow Caledonian University",
                "Queen Margaret University",
                "Robert Gordon University",
                "University of the Highlands and Islands",
                "University of the West of Scotland",
                "Scotland's Rural College",
                "The Open University in Scotland",
                "Glasgow School of Art",
                "Royal Conservatoire of Scotland"
            ],
            "Wales": [
                "Aberystwyth University",
                "Bangor University",
                "Cardiff University",
                "Swansea University",
                "University of South Wales",
                "Cardiff Metropolitan University",
                "University of Wales Trinity Saint David",
                "Wrexham Glyndŵr University"
            ],
            "North West": [
                "University of Manchester",
                "University of Liverpool",
                "Lancaster University",
                "University of Chester",
                "Edge Hill University",
                "Liverpool John Moores University",
                "Manchester Metropolitan University",
                "University of Salford",
                "University of Central Lancashire",
                "University of Bolton",
                "Liverpool Hope University",
                "University of Cumbria"
            ],
            "North East": [
                "Newcastle University",
                "Durham University",
                "University of Sunderland",
                "Northumbria University",
                "Teesside University"
            ],
            "Yorkshire and the Humber": [
                "University of Leeds",
                "University of Sheffield",
                "University of York",
                "Leeds Beckett University",
                "Sheffield Hallam University",
                "University of Hull",
                "University of Bradford",
                "University of Huddersfield",
                "Leeds Trinity University",
                "Leeds Arts University",
                "York St John University"
            ],
            "East Midlands": [
                "University of Nottingham",
                "Loughborough University",
                "University of Leicester",
                "De Montfort University",
                "Nottingham Trent University",
                "University of Lincoln",
                "University of Derby",
                "University of Northampton",
                "Bishop Grosseteste University"
            ],
            "Anglia": [
                "University of Cambridge",
                "University of East Anglia",
                "Anglia Ruskin University",
                "University of Essex",
                "University of Suffolk",
                "Norwich University of the Arts",
                "University of Hertfordshire",
                "University of Bedfordshire",
                "Cranfield University",
                "Writtle University College"
            ],
            "South West": [
                "University of Exeter",
                "University of Bristol",
                "University of Bath",
                "University of Plymouth",
                "Falmouth University",
                "University of the West of England (UWE Bristol)",
                "Bath Spa University",
                "Arts University Bournemouth",
                "Plymouth Marjon University",
                "University of Gloucestershire",
                "Royal Agricultural University",
                "Bournemouth University",
                "Arts University Plymouth"
            ],
            "South East": [
                "University of Oxford",
                "University of Sussex",
                "University of Reading",
                "University of Kent",
                "University of Southampton",
                "University of Surrey",
                "University of Brighton",
                "University of Portsmouth",
                "Oxford Brookes University",
                "Royal Holloway, University of London",
                "University of Winchester",
                "University of Chichester",
                "Canterbury Christ Church University",
                "University for the Creative Arts",
                "Buckinghamshire New University",
                "Solent University",
                "University of Buckingham"
            ],
            "London": [
                "Imperial College London",
                "University College London",
                "King's College London",
                "London School of Economics",
                "Queen Mary University of London",
                "Birkbeck, University of London",
                "Brunel University London",
                "City, University of London",
                "Goldsmiths, University of London",
                "London Business School",
                "London Metropolitan University",
                "London School of Hygiene & Tropical Medicine",
                "London South Bank University",
                "Middlesex University",
                "Royal Academy of Music",
                "Royal College of Art",
                "Royal College of Music",
                "Royal Holloway, University of London",
                "Royal Veterinary College",
                "School of Oriental and African Studies (SOAS), University of London",
                "St George's, University of London",
                "University of East London",
                "University of Greenwich",
                "University of London",
                "University of Roehampton",
                "University of the Arts London",
                "University of West London",
                "University of Westminster"
            ],
            "Northern Ireland": [
                "Queen's University Belfast",
                "Ulster University",
                "St Mary's University College",
                "Stranmillis University College",
                "The Open University in Northern Ireland"
            ],
            "West Midlands": [
                "University of Birmingham",
                "Aston University",
                "University of Warwick",
                "Coventry University",
                "University of Wolverhampton",
                "Birmingham City University",
                "University College Birmingham",
                "Newman University",
                "Harper Adams University"
            ]

        }

        # Define clickable regions (polygon coordinates)
        self.regions = {
            "Scotland": [
                (430, 223), (392, 262), (321, 279), (223, 122), (254, 19), (398, 0), (449, 76), (436, 197),
                (430, 210), (430, 217), (431, 216), (430, 213), (429, 219)
            ],
            "Wales": [
                (330, 357), (362, 351), (380, 359), (388, 369), (400, 377), (405, 385), (405, 391), (392, 395),
                (397, 407), (395, 415), (397, 422), (389, 426), (397, 433), (392, 449), (395, 461), (403, 463),
                (410, 467), (410, 475), (410, 483), (399, 487), (389, 496), (375, 496), (363, 489), (333, 488),
                (302, 473), (298, 457)
            ],
            "North West": [
                (384, 268), (378, 276), (374, 287), (377, 296), (382, 311), (389, 322), (390, 335), (393, 342),
                (391, 354), (390, 364), (402, 378), (409, 384), (417, 392), (425, 387), (432, 380), (441, 376),
                (439, 365), (443, 354), (433, 336), (430, 324), (436, 329), (418, 313), (418, 307), (424, 302),
                (428, 293), (432, 289), (427, 281), (426, 273), (423, 265), (415, 263), (416, 254), (417, 247),
                (411, 242)
            ],
            "North East": [
                (437, 202), (446, 209), (456, 215), (457, 224), (460, 235), (467, 248), (469, 257), (472, 265),
                (484, 274), (486, 284), (479, 287), (469, 288), (458, 288), (452, 284), (442, 288), (433, 289),
                (427, 276), (424, 265), (417, 262), (417, 252), (415, 243), (420, 236), (431, 218), (430, 209)
            ],
            "Yorks/Humber": [
                (427, 299), (430, 293), (437, 290), (445, 290), (452, 285), (459, 290), (468, 289), (478, 287),
                (487, 285), (501, 285), (503, 293), (509, 298), (517, 304), (517, 313), (516, 322), (520, 330),
                (526, 339), (525, 346), (526, 354), (518, 354), (512, 349), (502, 349), (501, 356), (496, 351),
                (488, 354), (481, 357), (476, 362), (473, 367), (465, 368), (456, 366), (449, 358), (442, 349),
                (435, 337), (430, 321), (423, 315), (420, 309)
            ],
            "East Midlands": [
                (445, 355), (442, 360), (441, 367), (443, 375), (447, 381), (450, 387), (448, 396), (452, 400),
                (458, 403), (455, 410), (459, 414), (464, 419), (470, 424), (473, 429), (473, 436), (470, 444),
                (470, 450), (472, 456), (478, 453), (486, 453), (486, 447), (493, 445), (497, 437), (503, 431),
                (503, 421), (502, 414), (511, 412), (520, 412), (526, 408), (531, 403), (533, 392), (535, 378),
                (532, 367), (528, 359), (521, 354), (516, 360), (512, 352), (502, 350), (501, 357), (494, 354),
                (484, 356), (478, 361), (475, 368), (468, 368), (456, 365), (451, 357)
            ],
            "Anglia": [
                (534, 401), (539, 389), (552, 386), (564, 386), (576, 388), (585, 397), (591, 401), (595, 406),
                (596, 417), (596, 425), (594, 438), (592, 447), (583, 458), (580, 464), (574, 471), (569, 477),
                (564, 485), (551, 489), (537, 490), (539, 482), (532, 481), (523, 477), (515, 477), (508, 480),
                (502, 479), (496, 471), (503, 466), (496, 460), (497, 453), (497, 444), (503, 435), (509, 424),
                (504, 416), (515, 413), (523, 411)
            ],
            "South West": [
                (410, 486), (412, 473), (416, 465), (421, 460), (430, 458), (437, 458), (444, 456), (450, 453),
                (452, 468), (453, 481), (456, 491), (461, 497), (458, 504), (455, 510), (455, 517), (454, 526),
                (442, 523), (442, 529), (446, 537), (452, 543), (449, 548), (429, 555), (410, 554), (397, 551),
                (384, 556), (380, 567), (372, 576), (352, 581), (333, 575), (309, 592), (295, 596), (281, 593),
                (273, 583), (288, 562), (316, 539), (324, 522), (347, 504), (367, 503), (378, 503), (390, 500),
                (398, 493)
            ],
            "South East": [
                (464, 451), (459, 456), (456, 461), (451, 473), (455, 483), (457, 491), (462, 499), (460, 508),
                (454, 514), (455, 520), (456, 528), (446, 526), (449, 533), (451, 539), (456, 545), (465, 551),
                (471, 553), (481, 552), (490, 545), (500, 543), (512, 543), (524, 542), (533, 544), (544, 540),
                (552, 536), (560, 530), (570, 530), (571, 520), (579, 518), (585, 511), (588, 499), (580, 492),
                (569, 486), (561, 494), (550, 491), (540, 493), (535, 497), (535, 504), (525, 504), (519, 504),
                (506, 499), (501, 490), (497, 481), (490, 472), (497, 467), (494, 461), (495, 451), (489, 450),
                (481, 455), (472, 459)
            ],
            "London": [
                (502, 484), (510, 481), (517, 479), (526, 477), (536, 481), (538, 489), (537, 499), (533, 503),
                (522, 502), (512, 500), (506, 494)
            ],
            "Northern Ireland": [
                (209, 257), (218, 243), (238, 231), (264, 220), (280, 224), (282, 234), (284, 243), (292, 255),
                (304, 263), (304, 278), (304, 298), (285, 325), (248, 317), (220, 312), (200, 302), (188, 284),
                (198, 266)
            ],
            "West Midlands": [
                (396, 397), (407, 393), (416, 391), (424, 390), (429, 384), (436, 381), (442, 379), (446, 384),
                (446, 395), (452, 400), (457, 405), (458, 412), (464, 419), (471, 425), (471, 437), (470, 444),
                (463, 450), (456, 458), (449, 449), (445, 455), (434, 455), (428, 456), (420, 456), (419, 462),
                (411, 466), (404, 462), (396, 458), (394, 450), (397, 440), (402, 431), (394, 427), (400, 420),
                (396, 415), (401, 407)
            ]
        }

        # Main layout to hold everything
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background image label
        self.background_label = QLabel(self)
        self.original_pixmap = QPixmap("4.png")  # Replace with your background image file
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # Cover the full window

        # Overlay container for content
        self.overlay_container = QWidget(self)
        self.overlay_container.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 20px;")

        # Overlay layout for all content
        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setAlignment(Qt.AlignTop)
        overlay_layout.setSpacing(20)
        overlay_layout.setContentsMargins(20, 20, 20, 20)

        # Instructions
        self.instructions = QLabel("Click on the map to select your preferred locations.")
        self.instructions.setStyleSheet("font-size: 14px; color: #40797d; font-weight: bold;")
        self.instructions.setAlignment(Qt.AlignCenter)
        overlay_layout.addWidget(self.instructions)

        # Scroll Area for Content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable Content Container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(20)

        # Map Image
        self.map_label = QLabel()
        self.map_pixmap = QPixmap("map5.png")  # Replace with your map image file
        self.map_label.setPixmap(self.map_pixmap)
        self.map_label.setFixedSize(self.map_pixmap.size())  # Ensure the size matches the image
        self.map_label.mousePressEvent = self.detect_regions
        content_layout.addWidget(self.map_label, alignment=Qt.AlignCenter)

        # Selected Regions Label
        self.selected_regions_label = QLabel("Selected Regions: None")
        self.selected_regions_label.setStyleSheet("font-size: 14px; color: #40797d; margin-top: 10px; font-weight: bold;")
        content_layout.addWidget(self.selected_regions_label)

        # Buttons for actions (in a single row)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)  # Add spacing between the buttons

        # Select Entire UK Button
        self.select_all_button = QPushButton("Select Entire UK")
        self.select_all_button.setStyleSheet(
            "background-color: #00509E; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.select_all_button.clicked.connect(self.select_entire_uk)
        actions_layout.addWidget(self.select_all_button)

        # Clear Selection Button
        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.setStyleSheet(
            "background-color: #00509E; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.clear_button.clicked.connect(self.clear_selection)
        actions_layout.addWidget(self.clear_button)

        # Next Button
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet(
            "background-color: #40797d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
        )
        self.next_button.clicked.connect(self.next_page)
        actions_layout.addWidget(self.next_button)

        # Add the actions layout to the content layout
        content_layout.addLayout(actions_layout)

        # Add the scrollable content to the scroll area
        scroll_area.setWidget(content_widget)
        overlay_layout.addWidget(scroll_area)

        # Ensure the overlay container is above the background
        self.overlay_container.raise_()


    def resizeEvent(self, event):
        """Handle window resizing and dynamically adjust the background and overlay."""
        self.resize_background_image()
        self.update_overlay_position_and_size()
        super().resizeEvent(event)

    def resize_background_image(self):
        """Resize the background image to fit the window while maintaining aspect ratio."""
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setGeometry(0, 0, self.width(), self.height())

    def update_overlay_position_and_size(self):
        """Update the position and size of the overlay box dynamically."""
        if self.overlay_container:
            new_width = int(self.width() * 0.6)  # 60% of the window width
            new_height = int(self.height() * 0.9)  # 80% of the window height
            self.overlay_container.resize(new_width, new_height)
            self.overlay_container.move(
                (self.width() - new_width) // 2,
                (self.height() - new_height) // 2
            )

    def detect_regions(self, event):
        """Detect which region was clicked based on the polygon regions."""
        x, y = event.pos().x(), event.pos().y()
        for region, polygon in self.regions.items():
            if self.point_in_polygon((x, y), polygon):
                if region not in self.selected_regions:
                    self.selected_regions.append(region)
                    self.update_selected_regions_label()
                else:
                    self.selected_regions.remove(region)
                    self.update_selected_regions_label()
                return
        QMessageBox.warning(self, "Invalid Selection", "Please click within a valid region.")

    def point_in_polygon(self, point, polygon):
        """Check if a point is inside a polygon using the ray-casting algorithm."""
        x, y = point
        inside = False
        n = len(polygon)
        px, py = polygon[0]
        for i in range(1, n + 1):
            sx, sy = polygon[i % n]
            if y > min(py, sy):
                if y <= max(py, sy):
                    if x <= max(px, sx):
                        if py != sy:
                            xinters = (y - py) * (sx - px) / (sy - py) + px
                            if px == sx or x <= xinters:
                                inside = not inside
            px, py = sx, sy
        return inside

    def update_selected_regions_label(self):
        """Update the label showing selected regions."""
        if self.selected_regions:
            self.selected_regions_label.setText(f"Selected Regions: {', '.join(self.selected_regions)}")
        else:
            self.selected_regions_label.setText("Selected Regions: None")

    def select_entire_uk(self):
        """Select all regions in the UK."""
        self.selected_regions = list(self.university_data.keys())
        self.update_selected_regions_label()

    def clear_selection(self):
        """Clear all selected regions."""
        self.selected_regions = []
        self.update_selected_regions_label()

    def populate_selections(self, location_data):
        """
        Populate the selected regions and universities from existing data.
        """
        self.selected_regions = location_data.get("regions", [])
        self.update_selected_regions_label()


    def next_page(self):
        """Pass the selected regions and universities to the next section."""
        if not self.selected_regions:
            QMessageBox.warning(self, "Region Missing", "Please select at least one region on the map.")
            return

        # Gather the universities for the selected regions
        selected_universities = [
            uni for region in self.selected_regions for uni in self.university_data.get(region, [])
        ]
        location_data = {"regions": self.selected_regions, "universities": selected_universities}

        # Pass the location data to the parent widget
        self.parent().move_to_next_section("location", location_data)
