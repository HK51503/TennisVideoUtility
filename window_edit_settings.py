from PySide6.QtWidgets import (
    QTabWidget, QWidget, QRadioButton, QPushButton, QLabel, QGroupBox, QVBoxLayout, QGridLayout,
    QButtonGroup, QFrame
)
import functions_settings_config as settings


class EditSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        tab_widget = QTabWidget()
        main_v_layout = QVBoxLayout()
        tab_widget.addTab(VideoSettingsTab(), "動画設定")
        main_v_layout.addWidget(tab_widget)
        self.setLayout(main_v_layout)


class VideoSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        main_v_layout = QVBoxLayout()
        self.setLayout(main_v_layout)

        video_setting_groupbox = QGroupBox()
        video_setting_layout = QGridLayout()

        # youtube upload settings
        self.youtube_upload_setting_button_group = QButtonGroup()
        youtube_upload_true_button = QRadioButton("する（Coming Soon!）")
        youtube_upload_false_button = QRadioButton("しない")
        self.youtube_upload_setting_button_group.addButton(youtube_upload_true_button, 1)
        self.youtube_upload_setting_button_group.addButton(youtube_upload_false_button, 2)
        self.youtube_upload_setting_button_group.buttonClicked.connect(self.youtube_upload_setting_button_clicked)
        if settings.read_value("video_settings", "youtube_upload") == "True":
            youtube_upload_true_button.setChecked(True)
        else:
            youtube_upload_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel("YouTubeにアップロード"), 0, 0)
        video_setting_layout.addWidget(youtube_upload_true_button, 0, 1)
        video_setting_layout.addWidget(youtube_upload_false_button, 1, 1)

        youtube_upload_true_button.setEnabled(False)

        # stitch videos using ffmpeg setting
        self.stitch_videos_setting_button_group = QButtonGroup()
        stitch_videos_true_button = QRadioButton("する（Coming Soon!）")
        stitch_videos_false_button = QRadioButton("しない")
        self.stitch_videos_setting_button_group.addButton(stitch_videos_true_button, 1)
        self.stitch_videos_setting_button_group.addButton(stitch_videos_false_button, 2)
        self.stitch_videos_setting_button_group.buttonClicked.connect(self.stitch_videos_setting_button_clicked)
        if settings.read_value("video_settings", "stitch_videos") == "True":
            stitch_videos_true_button.setChecked(True)
        else:
            stitch_videos_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel("動画を結合"), 3, 0)
        video_setting_layout.addWidget(stitch_videos_true_button, 3, 1)
        video_setting_layout.addWidget(stitch_videos_false_button, 4, 1)

        stitch_videos_true_button.setEnabled(False)

        # keep original file setting
        self.keep_original_setting_button_group = QButtonGroup()
        keep_original_true_button = QRadioButton("残す")
        keep_original_false_button = QRadioButton("残さない")
        self.keep_original_setting_button_group.addButton(keep_original_true_button, 1)
        self.keep_original_setting_button_group.addButton(keep_original_false_button, 2)
        self.keep_original_setting_button_group.buttonClicked.connect(self.keep_original_setting_button_clicked)
        if settings.read_value("video_settings", "keep_original") == "True":
            keep_original_true_button.setChecked(True)
        else:
            keep_original_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel("元ファイルを"), 6, 0)
        video_setting_layout.addWidget(keep_original_true_button, 6, 1)
        video_setting_layout.addWidget(keep_original_false_button, 7, 1)

        # add separator line
        line = QFrame()
        line.setFrameStyle(QFrame.HLine)
        line.setLineWidth(0)
        line.setMidLineWidth(0)
        video_setting_layout.addWidget(line, 2, 0, 1, 2)
        video_setting_layout.addWidget(line, 5, 0, 1, 2)

        video_setting_groupbox.setLayout(video_setting_layout)
        main_v_layout.addWidget(video_setting_groupbox)

    def youtube_upload_setting_button_clicked(self):
        if self.youtube_upload_setting_button_group.checkedId() == 1:
            settings.set_value("video_settings", "youtube_upload", "True")
        else:
            settings.set_value("video_settings", "youtube_upload", "False")

    def stitch_videos_setting_button_clicked(self):
        if self.stitch_videos_setting_button_group.checkedId() == 1:
            settings.set_value("video_settings", "stitch_videos", "True")
        else:
            settings.set_value("video_settings", "stitch_videos", "False")

    def keep_original_setting_button_clicked(self):
        if self.keep_original_setting_button_group.checkedId() == 1:
            settings.set_value("video_settings", "keep_original", "True")
        else:
            settings.set_value("video_settings", "keep_original", "False")
