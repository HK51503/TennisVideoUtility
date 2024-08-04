from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, Signal
import functions_settings_config as conf
import rename_tool
import ffmpeg_tool
import os
import logging


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class ProgressWindow(QWidget):
    signal = Signal()
    parent_dir = os.getcwd()

    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        self.setWindowModality(Qt.ApplicationModal)

        self.logger_text_edit = QTextEditLogger(self)
        self.logger_text_edit.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s'))
        logging.getLogger().addHandler(self.logger_text_edit)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Initialized")

        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(self.logger_text_edit.widget)

        self.setLayout(main_v_layout)
        self.main_process()


    def main_process(self):
        logging.info("Main process started")
        is_youtube_upload = conf.read_value("video_settings", "youtube_upload")
        is_stitch_videos = conf.read_value("video_settings", "stitch_videos")
        is_keep_original = conf.read_value("video_settings", "keep_original")
        if is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "False":
            current_directory = os.getcwd()
            match_directory_path = rename_tool.create_match_folder(current_directory)
            rename_tool.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "True":
            current_directory = os.getcwd()
            match_directory_path = rename_tool.create_match_folder(current_directory)
            rename_tool.copy_videos(match_directory_path)
            rename_tool.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "False":
            current_directory = os.getcwd()
            match_directory_path = rename_tool.create_match_folder(current_directory)
            timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
            ffmpeg_tool.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
            rename_tool.rename_stitched_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "True":
            current_directory = os.getcwd()
            match_directory_path = rename_tool.create_match_folder(current_directory)
            timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
            ffmpeg_tool.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
            rename_tool.rename_stitched_videos(match_directory_path)
        else:
            print("Not Supported")
        logging.info("Done")

    def closeEvent(self, event):
        self.signal.emit()
