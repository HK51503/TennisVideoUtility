from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout
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
    parent_dir = os.getcwd()

    def __init__(self):
        super().__init__()
        logger_text_edit = QTextEditLogger(self)
        logger_text_edit.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logger_text_edit)

        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(logger_text_edit.widget)

        self.setLayout(main_v_layout)
        self.main_process()

    def main_process(self):
        is_youtube_upload = conf.read_value("video_settings", "youtube_upload")
        is_stitch_videos = conf.read_value("video_settings", "stitch_videos")
        is_keep_original = conf.read_value("video_settings", "keep_original")
        if is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "False":
            current_directory = os.getcwd()
            match_directory_path = rename_tool.create_match_folder(current_directory)
            rename_tool.rename_videos(match_directory_path)
            print("finished")
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "False":
            current_directory = os.getcwd()
            tmp_folder_path = os.path.join(current_directory, "tmp")
            if not (os.path.exists(tmp_folder_path)):
                os.mkdir(tmp_folder_path)

            ffmpeg_tool.stitch_videos(tmp_folder_path)
            match_directory_path = rename_tool.create_match_folder(current_directory)
            rename_tool.rename_stitched_videos(match_directory_path)
            print("finished")
        else:
            print("Not Supported")

    def closeEvent(self, event):
        self.deleteLater()
