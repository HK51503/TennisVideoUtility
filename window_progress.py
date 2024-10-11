from PySide6.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QMessageBox, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QObject, QThread
import functions_settings_config as conf
import tool_rename, tool_ffmpeg, tool_youtube_upload
import variables as var
import os, logging, shutil


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum())


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
        logging.getLogger().setLevel(logging.INFO)
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
        match_directory_path = tool_rename.create_match_folder(cwd)
        logging.debug("Config:" + is_youtube_upload + is_stitch_videos + is_keep_original)
        for match_id in var.dict_matches:
            if var.dict_matches[match_id].file_list:
                if is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "False":
                    tool_rename.rename_videos(match_id, match_directory_path)
                elif is_youtube_upload == "False" and is_stitch_videos == "False" and is_keep_original == "True":
                    if self.is_enough_disk_space(cwd) is True:
                        tool_rename.copy_video(match_id, match_directory_path)
                        tool_rename.rename_videos(match_id, match_directory_path)
                elif is_youtube_upload == "False" and is_stitch_videos == "True":
                    if self.is_enough_disk_space(cwd) is True:
                        timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
                        tool_ffmpeg.stitch_video(match_id, match_directory_path, timestamp_file_path, is_keep_original)
                        tool_rename.rename_stitched_video(match_id, match_directory_path)
                elif is_youtube_upload == "True" and is_stitch_videos == "True" and is_keep_original == "True":
                    if self.is_enough_disk_space(cwd) is True:
                        timestamp_file_path = os.path.join(match_directory_path, "timestamp.txt")
                        tool_ffmpeg.stitch_video(match_id, match_directory_path, timestamp_file_path, is_keep_original)
                        tool_rename.rename_stitched_video(match_id, match_directory_path)
                        tool_youtube_upload.upload_video(match_id)
            else:
                logging.info("Video not selected in " + match_id.upper() + ". Skipping...")

        logging.info("Everything done")
        self.finished.emit()

    @staticmethod
    def is_enough_disk_space(path):
        total_size = 0
        for match_id in var.dict_matches:
            for file in var.dict_matches[match_id].file_list:
                total_size += os.path.getsize(file)
        total, used, free = shutil.disk_usage(path)
        disk_free_in_gib = round(free / 2 ** 30, 2)
        file_total_in_gib = round(total_size / 2 ** 30, 2)
        if free >= total_size:
            logging.info("Estimated total file size: " + str(file_total_in_gib) + "GiB")
            logging.info("Free disk space: " + str(disk_free_in_gib) + "GiB")
            return True
        else:
            logging.info("Estimated total file size: " + str(file_total_in_gib) + "GiB")
            logging.info("Free disk space: " + str(disk_free_in_gib) + "GiB")
            logging.info("Not enough disk space")
            return False
