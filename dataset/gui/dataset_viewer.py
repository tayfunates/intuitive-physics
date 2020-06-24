import sys
from PyQt5 import QtWidgets, uic

# Maybe create a dataset viewer GUI to inspect data comfortably?


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('dataset_viewer.ui', self)  # Load the .ui file
        self.initialize_components()
        self.show()  # Show the GUI

    def initialize_components(self):
        # To do...
        self.load_button = self.findChild(QtWidgets.QPushButton, "loadDatasetButton")
        self.load_button.clicked.connect(self.load_dataset_button_clicked)

    def load_dataset_button_clicked(self):
        print("Loading dataset...")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()  # Start the application
