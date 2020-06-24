import json
import sys
from PyQt5 import QtWidgets, uic


# Maybe create a dataset viewer GUI to inspect data comfortably?


class Dataset:

    def __init__(self, dataset_json):
        self.dataset = dataset_json


g_dataset = None


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('dataset_viewer.ui', self)  # Load the .ui file

        self.initialize_components()
        self.initialize_listeners()

        self.show()  # Show the GUI

    def initialize_listeners(self):
        self.btn_load.clicked.connect(self.load_dataset)

    def initialize_components(self):
        # To do...
        self.btn_load = self.findChild(QtWidgets.QPushButton, "loadDatasetButton")
        self.le_dataset_folder = self.findChild(QtWidgets.QLineEdit, "datasetFolderLineEdit")

    def load_dataset(self):
        print("Loading dataset...")
        path = self.le_dataset_folder.text()
        with open(f"{path}/dataset.json", "r") as json_file:
            global g_dataset
            g_dataset = Dataset(json.load(json_file))
        print(f"Dataset at {path} loaded...")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()  # Start the application
