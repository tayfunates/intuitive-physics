#!/usr/bin/python3

import json
import logging
import os
import sys
from glob import glob
from pathlib import Path

import vlc
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFrame, QListWidget, QLineEdit, QPushButton


def minimized_dataset(dataset_json) -> dict:
    video_to_qa = {}
    for qa_json in dataset_json:
        video_to_qa[Path(qa_json["questions"]["info"]["video_filename"]).name] = \
            [
                {
                    "question": question_obj["question"],
                    "answer": question_obj["answer"],
                    "template_filename": question_obj["template_filename"]
                }
                for question_obj in qa_json["questions"]["questions"]
            ]
    return video_to_qa


class Dataset:

    def __init__(self, dataset_json):
        self.video_to_qa = minimized_dataset(dataset_json)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('dataset_viewer.ui', self)  # Load the .ui file

        self.path = None

        self.btn_load = self.findChild(QPushButton, "loadDatasetButton")
        self.le_dataset_folder = self.findChild(QLineEdit, "datasetFolderLineEdit")
        self.lw_videos = self.findChild(QListWidget, "videosListWidget")
        self.f_video = self.findChild(QFrame, "videoFrame")
        self.lw_questions = self.findChild(QFrame, "questionsListWidget")

        self.vlc_instance = vlc.Instance()
        self.vlc_media_player = self.vlc_instance.media_player_new()

        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.vlc_media_player.set_xwindow(self.f_video.winId())
        elif sys.platform == "win32":  # for Windows
            self.vlc_media_player.set_hwnd(self.f_video.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.vlc_media_player.set_nsobject(self.f_video.winId())

        self.initialize_listeners()

        self.show()  # Show the GUI

    def initialize_listeners(self):
        self.btn_load.clicked.connect(self.load_dataset)

    def video_item_clicked(self, item):
        logging.debug("Item clicked: " + item.text())
        filename = item.text()

        files = []
        start_dir = Path(f"{self.path}").joinpath("videos")
        pattern = "*.mpg"

        for dir, _, _ in os.walk(start_dir):
            files.extend(glob(os.path.join(dir, pattern)))

        full_path = ""
        for path in files:
            if Path(path).name == filename:
                full_path = path

        logging.debug("Full video path: %s", full_path)

        media = self.vlc_instance.media_new(full_path)
        self.vlc_media_player.set_media(media)
        self.vlc_media_player.play()

        self.lw_questions.clear()
        self.lw_questions.addItems([f"Q: {qa['question']}\nA: {qa['answer']}\nT: {qa['template_filename']}\n"
                                    for qa in g_dataset.video_to_qa[filename]])

    def populate_lists(self):
        self.lw_videos.clear()
        self.lw_videos.addItems(g_dataset.video_to_qa.keys())
        self.lw_videos.itemClicked.connect(self.video_item_clicked)

    def load_dataset(self):
        logging.info("Loading dataset...")
        self.path = self.le_dataset_folder.text()
        with open(Path(f"{self.path}").joinpath("dataset.json"), "r") as json_file:
            global g_dataset
            g_dataset = Dataset(json.load(json_file))
        logging.info(f"Dataset at {self.path} loaded...")
        self.populate_lists()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.NOTSET,
        format='[%(levelname)s]\t%(asctime)s\t%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)])
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()  # Start the application
