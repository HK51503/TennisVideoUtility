from PySide6.QtWidgets import (
    QTabWidget, QWidget, QRadioButton, QLabel, QGroupBox, QVBoxLayout, QGridLayout,
    QButtonGroup, QFrame, QComboBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
import functions_settings_config as settings


class EditSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowModality(Qt.ApplicationModal)
        tab_widget = QTabWidget()
        main_v_layout = QVBoxLayout()
        tab_widget.addTab(VideoSettingsTab(), self.tr("動画設定"))
        tab_widget.addTab(GeneralSettingsTab(), self.tr("一般設定"))
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
        youtube_upload_true_button = QRadioButton(self.tr("する（Coming Soon!）"))
        youtube_upload_false_button = QRadioButton(self.tr("しない"))
        self.youtube_upload_setting_button_group.addButton(youtube_upload_true_button, 1)
        self.youtube_upload_setting_button_group.addButton(youtube_upload_false_button, 2)
        self.youtube_upload_setting_button_group.buttonClicked.connect(self.youtube_upload_setting_button_clicked)
        if settings.read_value("video_settings", "youtube_upload") == "True":
            youtube_upload_true_button.setChecked(True)
        else:
            youtube_upload_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel(self.tr("YouTubeにアップロード")), 0, 0)
        video_setting_layout.addWidget(youtube_upload_true_button, 0, 1)
        video_setting_layout.addWidget(youtube_upload_false_button, 1, 1)

        youtube_upload_true_button.setEnabled(False)

        # stitch videos using ffmpeg setting
        self.stitch_videos_setting_button_group = QButtonGroup()
        stitch_videos_true_button = QRadioButton(self.tr("する"))
        stitch_videos_false_button = QRadioButton(self.tr("しない"))
        self.stitch_videos_setting_button_group.addButton(stitch_videos_true_button, 1)
        self.stitch_videos_setting_button_group.addButton(stitch_videos_false_button, 2)
        self.stitch_videos_setting_button_group.buttonClicked.connect(self.stitch_videos_setting_button_clicked)
        if settings.read_value("video_settings", "stitch_videos") == "True":
            stitch_videos_true_button.setChecked(True)
        else:
            stitch_videos_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel(self.tr("動画を結合")), 3, 0)
        video_setting_layout.addWidget(stitch_videos_true_button, 3, 1)
        video_setting_layout.addWidget(stitch_videos_false_button, 4, 1)

        # keep original file setting
        self.keep_original_setting_button_group = QButtonGroup()
        keep_original_true_button = QRadioButton(self.tr("残す"))
        keep_original_false_button = QRadioButton(self.tr("残さない"))
        self.keep_original_setting_button_group.addButton(keep_original_true_button, 1)
        self.keep_original_setting_button_group.addButton(keep_original_false_button, 2)
        self.keep_original_setting_button_group.buttonClicked.connect(self.keep_original_setting_button_clicked)
        if settings.read_value("video_settings", "keep_original") == "True":
            keep_original_true_button.setChecked(True)
        else:
            keep_original_false_button.setChecked(True)

        video_setting_layout.addWidget(QLabel(self.tr("元ファイルを")), 6, 0)
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
        main_v_layout.addWidget(video_setting_groupbox, alignment=Qt.AlignTop)

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


class GeneralSettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        main_grid_layout = QGridLayout()

        main_grid_layout.addWidget(QLabel(self.tr("言語 : ")), 0, 0)

        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(["Japanese(日本語)", "English"])
        if settings.read_value("general_settings", "language") == "en":
            self.language_combo_box.setCurrentIndex(1)
        self.language_combo_box.currentIndexChanged.connect(self.language_changed)
        main_grid_layout.addWidget(self.language_combo_box, 0, 1)

        self.language_change_restart_label = QLabel(self.tr("言語を変更するにはアプリケーションを再起動してください"))
        self.language_change_restart_label.setStyleSheet("QLabel {color:red;}")
        self.language_change_restart_label.hide()
        main_grid_layout.addWidget(self.language_change_restart_label, 1, 1)

        main_grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0)

        self.setLayout(main_grid_layout)

    def language_changed(self):
        if self.language_combo_box.currentIndex() == 0:
            settings.set_value("general_settings", "language", "ja")

        elif self.language_combo_box.currentIndex() == 1:
            settings.set_value("general_settings", "language", "en")

        self.language_change_restart_label.show()
