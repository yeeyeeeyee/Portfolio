import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class InvisibleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invisible Window")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Click me to hide!", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.clicked.connect(self.hide_window)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_window)

    def hide_window(self):
        self.hide()
        self.timer.start(5000)  # Hide for 5 seconds (5000 milliseconds)

    def show_window(self):
        self.show()
        self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvisibleWindow()
    window.show()
    sys.exit(app.exec())
