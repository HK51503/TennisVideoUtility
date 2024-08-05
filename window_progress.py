from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, Signal
import functions_settings_config as conf
import tool_rename, tool_ffmpeg
import os, logging


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class ProgressWindow(QWidget):
    close_signal = Signal()
    open_signal = Signal()
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


    def main_process(self):
        logging.info("Main process started")
        is_youtube_upload = conf.read_value("video_settings", "youtube_upload")
        is_stitch_videos = conf.read_value("video_settings", "stitch_videos")
        is_keep_original = conf.read_value("video_settings", "keep_original")
        if is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "False":
            logging.debug("Config is False False False")
            current_directory = os.getcwd()
            match_directory_path = tool_rename.create_match_folder(current_directory)
            tool_rename.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "True":
            logging.debug("Config is False False True")
            current_directory = os.getcwd()
            match_directory_path = tool_rename.create_match_folder(current_directory)
            tool_rename.copy_videos(match_directory_path)
            tool_rename.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "False":
            logging.debug("Config is False True False")
            current_directory = os.getcwd()
            match_directory_path = tool_rename.create_match_folder(current_directory)
            timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
            tool_ffmpeg.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
            tool_rename.rename_stitched_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "True":
            logging.debug("Config is False True True")
            current_directory = os.getcwd()
            match_directory_path = tool_rename.create_match_folder(current_directory)
            timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
            tool_ffmpeg.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
            tool_rename.rename_stitched_videos(match_directory_path)
        else:
            logging.info("Configuration not supported")
        logging.info("Done")

    def closeEvent(self, event):
        self.close_signal.emit()