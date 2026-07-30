from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen
from PyQt6.QtCore import Qt, QPoint
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
        
        self.current_tool = "freehand"  # Default tool is freehand drawing
        
        self.last_point = None  # Store the last point for freehand drawing 
        
        self.canvas = QPixmap(1000, 700)  # Create a pixmap to draw on
        self.canvas.fill(Qt.GlobalColor.white)  # Fill the pixmap with white color
        
        #Add a visible border around the canvas
        self.setStyleSheet("""AnnotationCanvas {border: 2px solid #666666;}""")

        
        
    def paintEvent(self, event):
        """Handle the painting of the canvas."""
        
        """Paint the canvas whenever Qt requests an update. Parameter: event(QPaintEvent): Contains information about the area of the widget that needs to be repainted."""
        
        
        #Create a painter that draws onto this widget
        painter = QPainter(self)
        
        painter.drawPixmap(0, 0, self.canvas)  # Draw the pixmap onto the widget    
        
    
    def mousePressEvent(self, event):
        """Handle mouse press events for starting annotations."""
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.pos()  # Store the position where the mouse was pressed
            
            
    def mouseMoveEvent(self, event):
        
        if (event.buttons() & Qt.MouseButton.LeftButton and self.last_point is not None):
            
            painter = QPainter(self.canvas)  # Create a painter to draw on the pixmap   
            
            pen = QPen(Qt.GlobalColor.black, 5, Qt.PenStyle.SolidLine)
            
            painter.setPen(pen)  # Set the pen for drawing  
            
            painter.drawLine(self.last_point, event.pos())  # Draw a line from the last point to the current mouse position
            
            self.last_point = event.pos()  # Update the last point to the current position  
            
            self.update()  # Request a repaint of the widget
            
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events to finish annotations."""
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = None  # Reset the last point when the mouse button is released
            