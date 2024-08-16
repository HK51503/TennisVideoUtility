from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QMessageBox, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal, QObject, QThread
import functions_settings_config as conf
import tool_rename, tool_ffmpeg
import variables as var
import os, logging, shutil, math


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
    parent_dir = os.getcwd()

    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        self.setWindowModality(Qt.ApplicationModal)
        self.is_finished = False

        self.logger_text_edit = QTextEditLogger(self)
        self.logger_text_edit.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s'))
        logging.getLogger().addHandler(self.logger_text_edit)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Logger Initialized")

        self.close_button = QPushButton(self.tr("閉じる"))
        self.close_button.clicked.connect(self.closeEvent)

        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(self.logger_text_edit.widget)
        main_v_layout.addWidget(self.close_button, alignment=Qt.AlignRight)

        self.close_button.hide()

        self.setLayout(main_v_layout)

    def run_main_process(self):
        self.is_finished = False
        self.close_button.hide()
        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.main_process)
        self.worker.finished.connect(self.worker_finished)

        self.thread.start()

    def worker_finished(self):
        self.thread.quit()
        self.worker.deleteLater()
        self.thread.deleteLater()
        self.is_finished = True
        self.close_button.show()

    def closeEvent(self, event):
        if self.is_finished is True:
            self.logger_text_edit.widget.clear()
            self.close_signal.emit()
        else:
            quit_dialog = QMessageBox()
            quit_dialog.setWindowTitle(" ")
            quit_dialog.setIcon(QMessageBox.Information)
            quit_dialog.setText(self.tr("実行中ですが強制的に閉じますか？"))
            quit_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            quit_dialog.setDefaultButton(QMessageBox.No)
            quit_dialog.setButtonText(QMessageBox.Yes, "はい")
            quit_dialog.setButtonText(QMessageBox.No, "いいえ")

            ret = quit_dialog.exec()
            if ret == QMessageBox.Yes:
                self.logger_text_edit.widget.clear()
                self.thread.quit()
                self.worker.deleteLater()
                self.thread.deleteLater()
                self.close_signal.emit()
            else:
                event.ignore()


class Worker(QObject):
    finished = Signal()

    def main_process(self):
        logging.info("Main process started")
        is_youtube_upload = conf.read_value("video_settings", "youtube_upload")
        is_stitch_videos = conf.read_value("video_settings", "stitch_videos")
        is_keep_original = conf.read_value("video_settings", "keep_original")
        cwd = os.getcwd()
        if is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "False":
            logging.debug("Config is False False False")
            current_directory = cwd
            match_directory_path = tool_rename.create_match_folder(current_directory)
            tool_rename.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "True":
            logging.debug("Config is False False True")
            current_directory = cwd
            match_directory_path = tool_rename.create_match_folder(current_directory)
            tool_rename.copy_videos(match_directory_path)
            tool_rename.rename_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "False":
            logging.debug("Config is False True False")
            if self.is_enough_disk_space(cwd) is True:
                current_directory = cwd
                match_directory_path = tool_rename.create_match_folder(current_directory)
                timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
                tool_ffmpeg.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
                tool_rename.rename_stitched_videos(match_directory_path)
        elif is_youtube_upload == "False" and is_stitch_videos == "True" and is_keep_original == "True":
            logging.debug("Config is False True True")
            if self.is_enough_disk_space(cwd) is True:
                current_directory = cwd
                match_directory_path = tool_rename.create_match_folder(current_directory)
                timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
                tool_ffmpeg.stitch_videos(match_directory_path, timestamp_file_path, is_keep_original)
                tool_rename.rename_stitched_videos(match_directory_path)
        else:
            logging.info("Configuration not supported")
        logging.info("Done")
        self.finished.emit()

    def is_enough_disk_space(self, path):
        total_size = 0
        for match_id in var.dict_file_list:
            for file in var.dict_file_list[match_id]:
                total_size += os.path.getsize(file)
        total, used, free = shutil.disk_usage(path)
        disk_total_in_gib = round(total / 2 ** 30, 2)
        file_total_in_gib = round(total_size / 2 ** 30, 2)
        if free >= total_size:
            logging.info("Estimated total file size: " + str(file_total_in_gib) + "GiB")
            logging.info("Free disk space: " + str(disk_total_in_gib) + "GiB")
            return True
        else:
            logging.info("Estimated total file size: " + str(file_total_in_gib) + "GiB")
            logging.info("Free disk space: " + str(disk_total_in_gib) + "GiB")
            logging.info("Not enough disk space")
            return False
