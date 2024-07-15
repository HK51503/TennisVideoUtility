from PySide6.QtWidgets import QWidget
import functions_settings_config as conf
import rename_tool
import os
import variables as var


class ProgressWindow(QWidget):
    parent_dir = os.getcwd()

    def __init__(self):
        super().__init__()
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
        else:
            print("Not Supported")
