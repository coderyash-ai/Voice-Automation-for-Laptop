import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QSize, QRect
import random

class Application(QMainWindow):
    class OrbWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("background-color: black;")  # Set background color to black

            # Initialize variables for disco effect
            self.disco_color = QColor(0, 51, 102)  # Start with a dark blue color
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateDiscoColor)
            self.timer.start(1000)  # Update color every 1000 ms (1 second)

        def updateDiscoColor(self):
            # Update the disco color to a random dark blue variation
            self.disco_color = QColor(
                random.randint(0, 51),  # Darker range for red channel
                random.randint(0, 51),  # Darker range for green channel
                random.randint(51, 102),  # Darker range for blue channel
                255  # Fully opaque
            )
            self.update()  # Request a repaint

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # Smooth drawing

            center = self.rect().center()
            radius = min(self.width(), self.height()) * 0.20  # Size of the main orb

            # Paint the central orb with a simple glow effect
            glow_radius = radius * 1.5  # Radius for the glow effect
            glow_gradient = QRadialGradient(center, glow_radius)
            glow_gradient.setColorAt(0, QColor(0, 0, 255, 200))  # Bright blue at center
            glow_gradient.setColorAt(0.7, QColor(0, 0, 255, 100))  # Semi-transparent blue
            glow_gradient.setColorAt(1, QColor(0, 0, 255, 0))  # Fades out to transparent

            painter.setBrush(glow_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, glow_radius, glow_radius)

            # Draw the main orb
            main_orb_color = QColor(0, 255, 255)  # Cyan color for the orb
            painter.setBrush(main_orb_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, radius, radius)

            # Draw an additional concentric orb with a smaller radius
            additional_radius = radius * 0.8  # Size of the additional concentric orb, smaller than the main orb
            additional_glow_radius = additional_radius * 1.2  # Radius for the glow effect of the additional orb
            additional_glow_gradient = QRadialGradient(center, additional_glow_radius)
            additional_glow_gradient.setColorAt(0, QColor(255, 0, 0, 150))  # Bright red at center
            additional_glow_gradient.setColorAt(0.7, QColor(255, 0, 0, 75))  # Semi-transparent red
            additional_glow_gradient.setColorAt(1, QColor(255, 0, 0, 0))  # Fades out to transparent

            painter.setBrush(additional_glow_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, additional_glow_radius, additional_glow_radius)

            # Draw the outer orb with red color
            additional_orb_color = QColor(255, 0, 0)  # Red color for the outer orb
            painter.setBrush(additional_orb_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, additional_radius, additional_radius)

            # Draw the disco light effect around the circumference of the additional orb
            disco_radius = additional_radius * 1.1  # Slightly larger radius for the disco effect
            disco_gradient = QRadialGradient(center, disco_radius)
            disco_gradient.setColorAt(0, self.disco_color)  # Disco color at the center
            disco_gradient.setColorAt(0.9, self.disco_color.darker(150))  # Slightly darker
            disco_gradient.setColorAt(1, self.disco_color.darker(200))  # More darker

            painter.setBrush(disco_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, disco_radius, disco_radius)

            # Draw the text "SAM AI" in the center of the orbs
            font_size = 30  # Adjust font size to fit inside the orb
            font = QFont('Arial', font_size, QFont.Bold)  # Set the font, size, and weight
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255, 150))  # White text with some transparency

            text = "SAM AI"
            text_rect = painter.fontMetrics().boundingRect(text)
            text_rect.moveCenter(center)

            # Ensure text is within the orb by adjusting the font size if necessary
            if text_rect.width() > radius * 2 or text_rect.height() > radius * 2:
                # Adjust font size to fit text within the orb
                font_size = min(radius * 2 / text_rect.width(), radius * 2 / text_rect.height()) * font_size
                font.setPointSize(int(font_size))
                painter.setFont(font)
                text_rect = painter.fontMetrics().boundingRect(text)
                text_rect.moveCenter(center)

            painter.drawText(text_rect, Qt.AlignCenter, text)

    class RoundedBoxWidget(QWidget):
        def __init__(self, color, size, radius=20):
            super().__init__()
            self.setFixedSize(size)
            self.color = color
            self.radius = radius

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # Smooth drawing

            # Draw the background color with rounded corners (fully transparent)
            transparent_color = QColor(self.color)
            transparent_color.setAlpha(0)  # Set opacity to 0
            painter.setBrush(QBrush(transparent_color))
            painter.setPen(Qt.NoPen)  # No border for the background
            painter.drawRoundedRect(self.rect(), self.radius, self.radius)

            # Draw the white border outline
            border_pen = QPen(QColor(255, 255, 255))  # White color for the border
            border_pen.setWidth(3)  # Width of the border
            painter.setPen(border_pen)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), self.radius, self.radius)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")  # Set background color to black

        # Create the OrbWidget
        self.orb_widget = self.OrbWidget()

        # Create the first box with fixed size and rounded corners
        self.box_widget1 = self.RoundedBoxWidget(QColor("#003366"), QSize(900, 400))  # Dull cyber blue background color

        # Create the second box with fixed size and rounded corners, also dull cyber blue
        self.box_widget2 = self.RoundedBoxWidget(QColor("#003366"), QSize(900, 80))  # Dull cyber blue background color

        # Create a push button with rounded corners
        self.push_button = QPushButton("ENTER")
        self.push_button.setStyleSheet("""
            background-color: black; 
            color: white; 
            border-radius: 15px; 
            padding: 10px 20px; 
            font-size: 16px;
        """)

        # Create a layout for the second box to add the push button on the right side
        h_layout2 = QHBoxLayout()
        h_layout2.addStretch()  # Add stretchable space before the push button
        h_layout2.addWidget(self.push_button)  # Add the push button
        self.box_widget2.setLayout(h_layout2)

        # Create a horizontal layout to center the second box
        center_layout = QHBoxLayout()
        center_layout.addStretch()  # Add stretchable space before the second box
        center_layout.addWidget(self.box_widget2)  # Add the second box
        center_layout.addStretch()  # Add stretchable space after the second box

        # Create horizontal layouts to center the boxes
        h_layout1 = QHBoxLayout()
        h_layout1.addStretch()  # Add stretchable space before the first box
        h_layout1.addWidget(self.box_widget1)
        h_layout1.addStretch()  # Add stretchable space after the first box

        # Create a vertical layout to position the orb and boxes
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.orb_widget)
        v_layout.addLayout(h_layout1)  # Add the horizontal layout containing the first box
        v_layout.addLayout(center_layout)  # Add the centered layout containing the second box

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

        self.showFullScreen()  # Set the window to full screen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    sys.exit(app.exec_())
