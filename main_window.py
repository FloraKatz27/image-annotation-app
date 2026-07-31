from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QComboBox, QButtonGroup, QColorDialog, QFileDialog)
from annotation_canvas import AnnotationCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence


class MainWindow(QMainWindow):
    """
    Main window for the Image Annotation application.

    This class will manage the overall interface, including
    the canvas, menus, tool controls and status information.
    """

    def __init__(self):
        """Initialise and configure the main application window."""

        super().__init__()
        
        #Store the path currently used by Save
        #None means the user has not yet saved the canvas to a file
        self.current_save_path = None

        # Set the text displayed in the title bar.
        self.setWindowTitle("Image Annotation Application")

        # Set the initial window size.
        self.resize(1000, 700)

        # Prevent the interface from becoming too small.
        self.setMinimumSize(800, 600)
        
        #Create a general container widget for the central container
        central_widget = QWidget()
        
        #Create side by side layout for the central widget
        main_layout = QHBoxLayout(central_widget)
        
        #Add spacing around the interface
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        #Add spacing between the control panel and the canvas
        main_layout.setSpacing(15)
        
        #Create the left control panel
        control_panel = QWidget()
        
        #Keep the panel at a consistent width
        control_panel.setFixedWidth(200)
        
        #Arrange the controls vertically inside the panel
        control_layout = QVBoxLayout(control_panel)
        
        #Create the heading for document-related actions
        file_label = QLabel("File Actions")
        control_layout.addWidget(file_label)
        
        #Create a New Canvas button and connect it 
        self.new_canvas_button = QPushButton("New Canvas")
        
        #Explain the button and show its keyboard shortcut
        self.new_canvas_button.setToolTip("Create a new blank canvas (Shortcut: Ctrl+N)")
                
        #Connect it to the new canvas method
        self.new_canvas_button.clicked.connect(self.new_canvas)
                
        control_layout.addWidget(self.new_canvas_button)
        
        #Create a button for opening an image file and connecting it to the canvas's load method
        self.open_image_button = QPushButton("Open Image")
        
        #Explain the button and show its keyboard shortcut
        self.open_image_button.setToolTip("Open an image file (Shortcut: Ctrl+O)")
                
        #Connect the button to the canvas's load method
        self.open_image_button.clicked.connect(self.open_image)
                
        control_layout.addWidget(self.open_image_button)
        
        #Create a button that saves to the current file path
        self.save_button = QPushButton("Save")
        
        #Explain the button and show its keyboard shortcut
        self.save_button.setToolTip("Save the current canvas (Shortcut: Ctrl+S)")
        
        #Connect the button to the save method
        self.save_button.clicked.connect(self.save_canvas)
        
        control_layout.addWidget(self.save_button)
        
        #Create a button that lets the user choose where to save the canvas
        self.save_as_button = QPushButton("Save As")
        
        #Explain the button and show its keyboard shortcut
        self.save_as_button.setToolTip("Save the current canvas as a new file (Shortcut: Meta+Shift+S)")
                
        #Connect the button to the save method
        self.save_as_button.clicked.connect(self.save_canvas_as)
                
        control_layout.addWidget(self.save_as_button)
        
        #Add visual separation before the annotation tools
        control_layout.addSpacing(15)
        
        #Create the tools heading
        tool_label = QLabel("Annotation Tools")
        control_layout.addWidget(tool_label)
        
        #Create the annotation tool buttons
        self.freehand_button = QPushButton("Freehand")
        self.line_button = QPushButton("Line")
        self.rectangle_button = QPushButton("Rectangle")
        
        #Allow each tool button to remain selected after it is clicked
        self.freehand_button.setCheckable(True)
        self.line_button.setCheckable(True)
        self.rectangle_button.setCheckable(True)
        
        #Group the tool buttons so that only one can be selected at a time
        self.tool_button_group = QButtonGroup(self)
        self.tool_button_group.addButton(self.freehand_button)
        self.tool_button_group.addButton(self.line_button)
        self.tool_button_group.addButton(self.rectangle_button)
        
        self.tool_button_group.setExclusive(True)  # Ensure only one button can be selected at a time
        
        #Freehand is the default tool, so select it when the application starts
        self.freehand_button.setChecked(True)
        
        #Connect each tool button to a method that updates the current tool in the canvas
        self.freehand_button.clicked.connect(self.select_freehand_tool)
        self.line_button.clicked.connect(self.select_line_tool)
        self.rectangle_button.clicked.connect(self.select_rectangle_tool)

        #Add the tool buttons to the control panel
        control_layout.addWidget(self.freehand_button)
        control_layout.addWidget(self.line_button)
        control_layout.addWidget(self.rectangle_button)
        
        #Add visual separation before the canvas control buttons
        control_layout.addSpacing(15)
        
        #Create the editing controls heading
        editing_label = QLabel("Editing Controls")
        control_layout.addWidget(editing_label)
        
        #Create the Undo button and connect it to the canvas's undo method
        self.undo_button = QPushButton("Undo")
        
        #Explain the button and show its keyboard shortcut
        self.undo_button.setToolTip("Undo the most recent annotation action (Shortcut: Ctrl+Z)")    
        #Connect it to the undo method
        self.undo_button.clicked.connect(self.undo)
                
        control_layout.addWidget(self.undo_button)
        
        #Create a button to clear the canvas and connect it to the canvas's clear method
        self.clear_button = QPushButton("Clear Canvas")
        
        #Connect the button to the canvas-clearing method
        self.clear_button.clicked.connect(self.clear_canvas)
        
        control_layout.addWidget(self.clear_button)     
        
        #Add spacing before the brush settings section
        control_layout.addSpacing(20)
        
        #Create the heading for the brush controls
        brush_label = QLabel("Brush Settings")
        control_layout.addWidget(brush_label)
        
        #Create a clearly labelled brush color control
        color_label = QLabel("Brush Color:")
        control_layout.addWidget(color_label)
        
        self.color_button = QPushButton("Black")
        
        self.color_button.clicked.connect(self.choose_brush_color) 
        
        control_layout.addWidget(self.color_button)
        
        #Create a label for the brush size control
        size_label = QLabel("Brush Size:")
        control_layout.addWidget(size_label)
        
        #Allow the user to select a brush size in pixels from 1 to 20, with a default of 5
        self.brush_size_spinbox = QSpinBox()
        self.brush_size_spinbox.setRange(1, 50)
        self.brush_size_spinbox.setValue(5)
        self.brush_size_spinbox.setSuffix(" px")
        
        self.brush_size_spinbox.valueChanged.connect(self.update_brush_size)
        
        control_layout.addWidget(self.brush_size_spinbox)
        
        #Create a label for the brush style control
        style_label = QLabel("Brush Style:")
        control_layout.addWidget(style_label)
        
        #Provide the required solid and dashed brush styles
        self.brush_style_combo = QComboBox()
        self.brush_style_combo.addItems(["Solid", "Dashed"])
        
        self.brush_style_combo.currentTextChanged.connect(self.update_brush_style) 
        
        control_layout.addWidget(self.brush_style_combo)
        
        
        #Push the controls to the top of the panel
        control_layout.addStretch()
        
        #Create the annotation canvas before adding it to the main layout to ensure it is displayed correctly
        self.canvas = AnnotationCanvas()
        
        #Add the control panel to the left side of the main layout
        main_layout.addWidget(control_panel)
        
        #Add the canvas to the top right side of the main layout
        #The stretch value of 1 lets the canvas expand to fill the remaining space in the window
        main_layout.addWidget(self.canvas, stretch=1)
        
        #Place the complete interface inside the main window
        self.setCentralWidget(central_widget)
        
        #Create the status bar at the bottom of the window
        self.statusBar()
        
        #Display the initial application state
        self.update_status_bar()
        
        #Create a new blank canvas when the application starts
        self.new_shortcut = QShortcut(QKeySequence.StandardKey.New, self)
        self.new_shortcut.activated.connect(self.new_canvas)
        
        #Open an existing image
        self.open_shortcut = QShortcut(QKeySequence.StandardKey.Open, self)
        self.open_shortcut.activated.connect(self.open_image)
        
        #Save using the current save path
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self.save_canvas)
        
        #Open Save As dialog to choose a save location
        self.save_as_shortcut = QShortcut(QKeySequence("Meta+Shift+S"), self)
        self.save_as_shortcut.activated.connect(self.save_canvas_as)
        
        #Undo the most recent annotation action
        self.undo_shortcut = QShortcut(QKeySequence.StandardKey.Undo, self)
        self.undo_shortcut.activated.connect(self.undo)
        
    def select_freehand_tool(self):
        """Set the current tool in the canvas to freehand drawing."""
        self.canvas.current_tool = "freehand"
        self.update_status_bar()  # Update the status bar to reflect the current tool
        
    def select_line_tool(self):
        """Set the current tool in the canvas to line drawing."""
        self.canvas.current_tool = "line"
        self.update_status_bar()  # Update the status bar to reflect the current tool
        
    def select_rectangle_tool(self):
        """Set the current tool in the canvas to rectangle drawing."""
        self.canvas.current_tool = "rectangle"
        self.update_status_bar()  # Update the status bar to reflect the current tool

    def update_brush_size(self, size):
        """Update the brush size in the canvas based on the spinbox value."""
        self.canvas.brush_size = size
        self.update_status_bar()  # Update the status bar to reflect the current brush size   
        
    def update_brush_style(self, style_name):
        """Update the brush style in the canvas based on the combobox selection."""
        if style_name == "Solid":
            self.canvas.brush_style = Qt.PenStyle.SolidLine
        elif style_name == "Dashed":
            self.canvas.brush_style = Qt.PenStyle.DashLine 
            
        self.update_status_bar()  # Update the status bar to reflect the current brush style     
                
    
    def choose_brush_color(self):
        """Open a color dialog to allow the user to select a brush color."""
        color = QColorDialog.getColor(self.canvas.brush_color, self, "Choose Brush Color")
        if color.isValid():
            self.canvas.brush_color = color
            self.update_status_bar()  # Update the status bar to reflect the current brush color
            self.color_button.setText(color.name())  # Update the button text to show the selected color
            self.color_button.setStyleSheet(f"background-color: {color.name()}; color: white;")  # Change button background to selected color
            
            
    def clear_canvas(self):
        """Clear all annotations from the canvas."""
        self.canvas.clear_canvas()
        
    def undo(self):
        """Undo the last annotation action on the canvas."""
        self.canvas.undo()
        
    def new_canvas(self):
        """Create a new blank canvas for annotations."""
        self.canvas.new_canvas()
        #A new document does not yet have a save location, so reset the current save path
        self.current_save_path = None
        
        self.statusBar().showMessage("New canvas created.", 5000)  # Show message for 5 seconds     
        
        self.update_status_bar()  # Update the status bar to reflect the current state of the canvas 
        
    def open_image(self):
        """Open a file dialog to allow the user to select an image file to load onto the canvas."""
        file_path, selected_filter = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        
        if file_path:
            self.canvas.load_image(file_path)  # Load the selected image onto the canvas
            
            #Require Save As before exporting over a chosen path
            self.current_save_path = None
            
            self.statusBar().showMessage(f"Image opened from: {file_path}", 5000)  # Update the status bar to reflect the current state of the canvas
            
            self.update_status_bar()  # Update the status bar to reflect the current state of the canvas    
        
    def save_canvas_as(self):
        """Open a file dialog to allow the user to save the canvas as an image file."""
        file_path, selected_filter = QFileDialog.getSaveFileName(self, "Save Annotated Image", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
        
        if file_path:
            #Remember this path for future Save operations
            self.current_save_path = file_path
            
            #Determine the file format based on the selected filter
            success = self.canvas.canvas.save(file_path)
            
            if success:
                self.statusBar().showMessage(f"Image saved to {file_path}", 5000)  # Show message for 5 seconds        

    def save_canvas(self):
        """Save the image using the current save path if it exists"""
        #If no location has been chosen, use Save As first
        if self.current_save_path is None:
            self.save_canvas_as()
            return  # Exit the method after saving with Save As
        
        success = self.canvas.canvas.save(self.current_save_path)
        
        if success:
            self.statusBar().showMessage(f"Image saved to {self.current_save_path}", 5000)  # Show message for 5 seconds
        else:
            self.statusBar().showMessage("Failed to save image.", 5000)  # Show message for 5 seconds
    
            
    def update_status_bar(self):
        """Update the status bar with the current tool and brush settings."""
 
        image_width = self.canvas.canvas.width()
        image_height = self.canvas.canvas.height()
       
        message = (f"Tool: {self.canvas.current_tool.capitalize()} | " f"Color: {self.canvas.brush_color.name()} | " f"Size: {self.canvas.brush_size} px | " f"Image: {image_width} x {image_height}")
        
        self.statusBar().showMessage(message)
        
        
    
        