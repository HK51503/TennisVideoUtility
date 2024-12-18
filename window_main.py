from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QMessageBox, QFrame,
    QLabel, QFileDialog, QMenu
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from window_edit_match import EditMatchWindow
from window_edit_settings import EditSettingsWindow
from window_progress import ProgressWindow
import functions_match_config as conf
import variables as var
import os, time


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.edit_settings_window = EditSettingsWindow()

        self.progress_window = ProgressWindow()

        self.setWindowTitle("Tennis Video Utility V1")
        self.resize(500, 400)
        main_window_central_widget = QWidget()
        main_window_button_layout = QVBoxLayout()

        start_button = QPushButton(self.tr("開始"))
        start_button.clicked.connect(self.start_button_clicked)
        import_match_button = QPushButton(self.tr("試合を読込"))
        import_match_button.clicked.connect(self.import_match_button_clicked)
        edit_match_button = QPushButton(self.tr("試合を編集"))
        edit_match_button.clicked.connect(self.edit_match_button_clicked)
        edit_settings_button = QPushButton(self.tr("設定"))
        edit_settings_button.clicked.connect(self.edit_settings_button_clicked)
        quit_button = QPushButton(self.tr("終了"))
        quit_button.clicked.connect(self.quit_button_clicked)

        main_window_button_layout.addWidget(start_button)
        main_window_button_layout.addWidget(import_match_button)
        main_window_button_layout.addWidget(edit_match_button)
        main_window_button_layout.addWidget(edit_settings_button)
        main_window_button_layout.addWidget(quit_button)
        main_window_button_layout.addStretch()

        self.main_window_match_list = QScrollArea()
        self.main_window_match_list.setMinimumSize(300, 0)
        self.main_window_match_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_window_match_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.render_match_list()

        save_selection_button = QPushButton(self.tr("動画の選択を保存"))
        save_selection_button.clicked.connect(self.save_selection_button_clicked)
        clear_selection_button = QPushButton(self.tr("動画の選択をリセット"))
        clear_selection_button.clicked.connect(self.clear_selection_button_clicked)

        match_layout_clear_selection_button_layout = QHBoxLayout()
        match_layout_clear_selection_button_layout.addStretch()
        match_layout_clear_selection_button_layout.addWidget(save_selection_button)
        match_layout_clear_selection_button_layout.addWidget(clear_selection_button)

        main_window_match_layout = QVBoxLayout()
        main_window_match_layout.addWidget(self.main_window_match_list)
        main_window_match_layout.addLayout(match_layout_clear_selection_button_layout)

        h_layout = QHBoxLayout()
        h_layout.addLayout(main_window_match_layout)
        h_layout.addLayout(main_window_button_layout)
        main_window_central_widget.setLayout(h_layout)
        self.setCentralWidget(main_window_central_widget)

    def start_button_clicked(self):
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle(" ")
        confirmation_dialog.setIcon(QMessageBox.Information)
        confirmation_dialog.setText(self.tr("開始しますか？"))
        confirmation_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_dialog.setDefaultButton(QMessageBox.Yes)
        confirmation_dialog.setButtonText(QMessageBox.Yes, self.tr("開始"))
        confirmation_dialog.setButtonText(QMessageBox.No, self.tr("戻る"))

        ret = confirmation_dialog.exec()

        if ret == QMessageBox.Yes:
            self.progress_window.show()
            self.progress_window.run_main_process()
            self.progress_window.close_signal.connect(self.process_finished)

    def import_match_button_clicked(self):
        file_name, n = QFileDialog.getOpenFileName(self, self.tr("試合を読み込み"), filter=self.tr("設定ファイル (*.ini)"))
        if file_name != "":
            if var.match_config_file_name == var.default_match_config_file_name:
                os.remove(var.default_match_config_file_name)
            var.match_config_file_name = file_name

        var.dict_matches.clear()
        conf.initialize()
        self.render_match_list()

    def edit_match_button_clicked(self):
        self.edit_match_window = EditMatchWindow()
        self.edit_match_window.show()
        self.edit_match_window.destroyed.connect(self.render_match_list)

    def edit_settings_button_clicked(self):
        self.edit_settings_window.show()

    def quit_button_clicked(self):
        quit_dialog = QMessageBox()
        quit_dialog.setWindowTitle(" ")
        quit_dialog.setIcon(QMessageBox.Information)
        quit_dialog.setText(self.tr("アプリケーションを終了しますか？"))
        quit_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        quit_dialog.setDefaultButton(QMessageBox.No)
        quit_dialog.setButtonText(QMessageBox.Yes, self.tr("はい"))
        quit_dialog.setButtonText(QMessageBox.No, self.tr("いいえ"))

        ret = quit_dialog.exec()
        if ret == QMessageBox.Yes:
            self.app.quit()
        return ret

    def render_match_list(self):
        self.main_window_match_list.setWidget(MatchListWidget())
        self.main_window_match_list.setWidgetResizable(True)

    def process_finished(self):
        self.progress_window.close()

    def clear_selection_button_clicked(self):
        clear_dialog = QMessageBox()
        clear_dialog.setWindowTitle(" ")
        clear_dialog.setIcon(QMessageBox.Information)
        clear_dialog.setText(self.tr("本当にリセットしますか？"))
        clear_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        clear_dialog.setDefaultButton(QMessageBox.No)
        clear_dialog.setButtonText(QMessageBox.Yes, self.tr("はい"))
        clear_dialog.setButtonText(QMessageBox.No, self.tr("いいえ"))

        ret = clear_dialog.exec()
        if ret == QMessageBox.Yes:
            for match_id in var.dict_matches:
                var.dict_matches[match_id].clear_file_selection()

            self.render_match_list()

    @staticmethod
    def save_selection_button_clicked():
        for match_id in var.dict_matches:
            match_id_hi = match_id.upper()
            conf.set_value(match_id_hi, "files", str(var.dict_matches[match_id].file_list))

    def closeEvent(self, event):
        ret = self.quit_button_clicked()
        if ret == QMessageBox.No:
            event.ignore()


class MatchListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.match_list_v_layout = QVBoxLayout()
        self.match_list_add_button_dict = {}

        self.add_message_label = QLabel(self.tr("試合を追加してください"))
        self.add_message_label.setStyleSheet("color:grey")
        self.match_list_v_layout.addWidget(self.add_message_label)
        if conf.if_match_exists() is False: self.add_message_label.show()
        else: self.add_message_label.hide()

        # create id list
        match_id_low_list = []
        match_id_hi_list = []
        for match_id in var.dict_matches:
            match_id_low_list.append(match_id)
            match_id_hi_list.append(var.dict_matches[match_id].match_id_high)
        match_id_low_list.sort()
        match_id_hi_list.sort()

        # initialize match list
        for i in range(len(match_id_low_list)):
            # define variables
            match_id_low = match_id_low_list[i]
            match_frame_name = "match_frame_" + match_id_low
            match_h_layout_name = "match_h_layout_" + match_id_low
            label_name = "label_" + match_id_low
            add_button_name = "add_button_" + match_id_low

            menu_button_name = "menu_button_" + match_id_low
            menu_name = "menu_" + match_id_low
            video_count_label_name = "video_count_label_button_" + match_id_low

            match_id_full = var.dict_matches[match_id_low].get_match_id_full()

            # create match frame and h layout
            setattr(self, match_frame_name, QFrame())
            getattr(self, match_frame_name).setFrameStyle(QFrame.Panel | QFrame.Plain)
            getattr(self, match_frame_name).setLineWidth(1)
            getattr(self, match_frame_name).setFixedHeight(50)

            setattr(self, match_h_layout_name, QHBoxLayout())

            # add content to h layout
            setattr(self, label_name, QLabel(match_id_full))
            # getattr(self, label_name).setStyleSheet('.QLabel { font-size: 14pt;}')

            getattr(self, match_h_layout_name).addWidget(getattr(self, label_name))

            getattr(self, match_h_layout_name).addStretch()

            setattr(self, video_count_label_name, QLabel(""))
            getattr(self, video_count_label_name).setStyleSheet("color:grey")
            getattr(self, match_h_layout_name).addWidget(getattr(self, video_count_label_name))

            setattr(self, add_button_name, QPushButton(self.tr("動画を選択")))
            getattr(self, match_h_layout_name).addWidget(getattr(self, add_button_name))

            setattr(self, menu_name, QMenu())
            getattr(self, menu_name).addAction(self.tr("追加で選択"), lambda m=match_id_low: self.add_button_clicked(m))
            getattr(self, menu_name).addAction(self.tr("選択をリセット"), lambda m=match_id_low: self.remove_action_triggered(m))
            setattr(self, menu_button_name, QPushButton())
            getattr(self, menu_button_name).setFixedSize(22, 22)
            getattr(self, menu_button_name).setIconSize(QSize(14, 14))
            if var.theme == "Dark":
                getattr(self, menu_button_name).setStyleSheet("""QPushButton {
                                                              border-radius : 11px;
                                                              }
                                                              QPushButton:hover:!pressed {
                                                              background-color : #424242;}
                                                              QPushButton:pressed {
                                                              background-color : #3c3c3c;}
                                                              QPushButton::menu-indicator{ width:0px; };
                                                              """)
                getattr(self, menu_button_name).setIcon(QIcon("resources/images/three-dots-menu-white.svg"))
            elif var.theme == "Light":
                getattr(self, menu_button_name).setStyleSheet("""QPushButton {
                                                              border-radius : 11px;
                                                              }
                                                              QPushButton:hover:!pressed {
                                                              background-color : #e6e6e6;}
                                                              QPushButton:pressed {
                                                              background-color : #c0c0c0;}
                                                              QPushButton::menu-indicator{ width:0px; };
                                                              """)
                getattr(self, menu_button_name).setIcon(QIcon("resources/images/three-dots-menu-black.svg"))

            getattr(self, menu_button_name).setMenu(getattr(self, menu_name))
            getattr(self, match_h_layout_name).addWidget(getattr(self, menu_button_name))

            if len(var.dict_matches[match_id_low].file_list) != 0:
                getattr(self, video_count_label_name).setText(str(
                    len(var.dict_matches[match_id_low].file_list)) + self.tr("本の動画を選択済み"))
                getattr(self, video_count_label_name).setStyleSheet("color:grey")
                getattr(self, video_count_label_name).show()
                getattr(self, add_button_name).hide()
                getattr(self, menu_button_name).show()
            else:
                getattr(self, video_count_label_name).hide()
                getattr(self, add_button_name).show()
                getattr(self, menu_button_name).hide()

            # add h layout to frame
            getattr(self, match_frame_name).setLayout(getattr(self, match_h_layout_name))

            self.match_list_v_layout.addWidget(getattr(self, match_frame_name))

            # push button signal
            self.match_list_add_button_dict.update({match_id_low: getattr(self, add_button_name)})

        for button in self.match_list_add_button_dict:
            self.match_list_add_button_dict[button].clicked.connect(lambda _, b=button: self.add_button_clicked(b))

        self.match_list_v_layout.addStretch()
        self.setLayout(self.match_list_v_layout)

    def add_button_clicked(self, match_id):
        # file dialog settings
        caption = ""
        if var.loaded_language == "en":
            caption = "Select videos for " + match_id.upper()
        elif var.loaded_language == "ja":
            caption = match_id.upper() + "の試合を選択"
        file_dialog = QFileDialog(caption=caption)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.exec()

        # save selected files to list
        for file in file_dialog.selectedFiles():
            if file not in var.dict_matches[match_id].file_list:
                var.dict_matches[match_id].file_list.append(file)

        # sort files by creation date
        var.dict_matches[match_id].file_list.sort(key=lambda x: os.path.getmtime(x))

        # change ui
        video_count_label_name = "video_count_label_button_" + match_id
        menu_button_name = "menu_button_" + match_id
        add_button_name = "add_button_" + match_id
        if len(var.dict_matches[match_id].file_list) != 0:
            video_count_text = str(len(var.dict_matches[match_id].file_list)) + self.tr("本の動画を選択済み")
            getattr(self, video_count_label_name).setStyleSheet("color:grey")
            getattr(self, video_count_label_name).setText(video_count_text)
            getattr(self, video_count_label_name).show()
            getattr(self, menu_button_name).show()
            getattr(self, add_button_name).hide()
        else:
            video_count_text = self.tr("動画を選択してください")
            getattr(self, video_count_label_name).setStyleSheet("color:red")
            getattr(self, video_count_label_name).setText(video_count_text)
            getattr(self, video_count_label_name).show()
            getattr(self, menu_button_name).hide()
            getattr(self, add_button_name).show()

    def remove_action_triggered(self, match_id):
        # clear list
        var.dict_matches[match_id].file_list.clear()

        # update ui
        label_name = "video_count_label_button_" + match_id
        menu_button_name = "menu_button_" + match_id
        add_button_name = "add_button_" + match_id
        getattr(self, label_name).hide()
        getattr(self, menu_button_name).hide()
        getattr(self, add_button_name).show()
