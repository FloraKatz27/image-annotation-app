import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    """Create and run the Image Annotation application."""

    # Create the application object that manages events and windows.
    app = QApplication(sys.argv)

    # Create the main application window.
    window = MainWindow()

    # Display the main window.
    window.show()

    # Start the Qt event loop.
    sys.exit(app.exec())


if __name__ == "__main__":
    main()