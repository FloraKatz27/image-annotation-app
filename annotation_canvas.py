from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

class AnnotationCanvas(QWidget):
    """
    A canvas for displaying and annotating images.

    This class will handle the rendering of the image and any annotations
    made by the user. It will also manage user interactions such as mouse
    clicks and drags for creating annotations.
    """

    def __init__(self):
        """Initialise the annotation canvas."""
        super().__init__()
        
        #Keep the drawing area large enough to remain usable even when the window is resized.
        self.setMinimumSize(600, 400)
        
        #store the default canvas background color
        self.background_color = QColor("white")
        
        #Add a visible border around the canvas
        self.setStyleSheet("""AnnotationCanvas {border: 2px solid #666666;}""")

        
        
    def paintEvent(self, event):
        """Handle the painting of the canvas."""
        
        """Paint the canvas whenever Qt requests an update. Parameter: event(QPaintEvent): Contains information about the area of the widget that needs to be repainted."""
        
        
        #Create a painter that draws onto this widget
        painter = QPainter(self)
        
        #Fill the canvas with the background color
        painter.fillRect(self.rect(), self.background_color)
        