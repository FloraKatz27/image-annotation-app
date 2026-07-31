from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen
from PyQt6.QtCore import Qt, QRect
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
        
        self.brush_size = 5  # Default brush size for freehand drawing
        
        self.brush_style = Qt.PenStyle.SolidLine  # Default brush style for freehand drawing
        
        self.brush_color = Qt.GlobalColor.black   # Default brush color for freehand drawing     
        
        
        self.last_point = None  # Store the last point for freehand drawing
        
        self.start_point = None  # Store the starting point for line and rectangle tools
        self.end_point = None  # Store the ending point for line and rectangle tools 
        
        self.canvas = QPixmap(1000, 700)  # Create a pixmap to draw on
        self.canvas.fill(Qt.GlobalColor.white)  # Fill the pixmap with white color
        
        #Add a visible border around the canvas
        self.setStyleSheet("""AnnotationCanvas {border: 2px solid #666666;}""")

        
        
    def paintEvent(self, event):
        """Paint the permanent canvas and any temporary shape preview."""
        
        
        #Create a painter that draws onto this widget
        painter = QPainter(self)
        
        painter.drawPixmap(0, 0, self.canvas)  # Draw the pixmap onto the widget    
        
        
        #Draw a temporary preview while the user is dragging the mouse to create a line or rectangle
        if (self.current_tool in ["line", "rectangle"] and self.start_point is not None and self.end_point is not None):
            preview_pen = QPen(Qt.GlobalColor.black, self.brush_size, Qt.PenStyle.DashLine)  # Create a pen with the current brush size and style   
            painter.setPen(preview_pen)  # Set the pen for drawing
            
            
            #Draw a straight-line preview
            if self.current_tool == "line":
                painter.drawLine(self.start_point, self.end_point)
                
            #Draw a rectangle preview
            elif self.current_tool == "rectangle":
                preview_rectangle = QRect(self.start_point, self.end_point).normalized()  # Create a rectangle from the start and end points
                
                painter.drawRect(preview_rectangle)  # Draw the rectangle onto the widget
    
    def mousePressEvent(self, event):
        """Handle mouse press events for starting annotations."""
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.pos()  # Store the position where the mouse was pressed
            
            self.start_point = event.pos()  # Store the starting point for line and rectangle tools 
            self.end_point = event.pos()  # Initialize the ending point to the starting point   
            
            
    def mouseMoveEvent(self, event):
        
        if (self.current_tool in ["line", "rectangle"] and event.buttons() & Qt.MouseButton.LeftButton and self.start_point is not None):
            self.end_point = event.pos()  # Update the ending point as the mouse moves
            
            self.update()  # Request a repaint of the widget
        
        if (event.buttons() & Qt.MouseButton.LeftButton and self.last_point is not None and self.current_tool == "freehand"):
            
            painter = QPainter(self.canvas)  # Create a painter to draw on the pixmap   
            
            pen = QPen(self.brush_color, self.brush_size, self.brush_style)  # Create a pen with the current brush size and style   
            
            painter.setPen(pen)  # Set the pen for drawing  
            
            painter.drawLine(self.last_point, event.pos())  # Draw a line from the last point to the current mouse position
            
            painter.end()  # End the painting operation 
            
            self.last_point = event.pos()  # Update the last point to the current position  
            
            self.update()  # Request a repaint of the widget
            
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events to finish annotations."""
        
        if event.button() == Qt.MouseButton.LeftButton:
            
            #Use the exact position where the mouse was released
            self.end_point = event.pos()
            
            #Permanently draw the line onto the canvas if the corresponding tool is selected
            if (self.current_tool == "line" and self.start_point is not None and self.end_point is not None):
                painter = QPainter(self.canvas)  # Create a painter to draw on the pixmap
                
                pen = QPen(self.brush_color, self.brush_size, self.brush_style)  # Create a pen with the current brush size and style   
                
                painter.setPen(pen)  # Set the pen for drawing
                
                painter.drawLine(self.start_point, self.end_point)  # Draw the line onto the pixmap
                
                painter.end()  # End the painting operation
                
            #Permanently draw the rectangle onto the canvas if the rectangle tool is selected
            elif (self.current_tool == "rectangle" and self.start_point is not None and self.end_point is not None):
                painter = QPainter(self.canvas)  # Create a painter to draw on the pixmap
                
                pen = QPen(self.brush_color, self.brush_size, self.brush_style)  # Create a pen with the current brush size and style 
                
                painter.setPen(pen)  # Set the pen for drawing
                
                final_rectangle = QRect(self.start_point, self.end_point).normalized()  # Create a rectangle from the start and end points
                
                painter.drawRect(final_rectangle)  # Draw the rectangle onto the pixmap
                
                painter.end()  # End the painting operation

            #Reset the points after the drawing action finishes
            self.last_point = None
            self.start_point = None
            self.end_point = None
                
            #Refresh the canvas
            self.update()
            