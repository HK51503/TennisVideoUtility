from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QMessageBox, QFrame,
    QLabel, QFileDialog, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from window_edit_match import EditMatchWindow
import match_config_functions as conf


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("Tennis Video Utility V1")
        self.resize(500, 400)
        main_window_central_widget = QWidget()
        main_window_button_layout = QVBoxLayout()

        start_button = QPushButton("開始")
        start_button.clicked.connect(self.start_button_clicked)
        edit_match_button = QPushButton("試合を編集")
        edit_match_button.clicked.connect(self.edit_match_button_clicked)
        edit_settings_button = QPushButton("設定")
        edit_settings_button.clicked.connect(self.edit_settings_button_clicked)
        quit_button = QPushButton("終了")
        quit_button.clicked.connect(self.quit_button_clicked)

        main_window_button_layout.addWidget(start_button)
        main_window_button_layout.addWidget(edit_match_button)
        main_window_button_layout.addWidget(edit_settings_button)
        main_window_button_layout.addWidget(quit_button)
        main_window_button_layout.addStretch()

        self.main_window_match_list = QScrollArea()
        self.main_window_match_list.setMinimumSize(300, 0)
        self.main_window_match_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.main_window_match_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.render_match_list()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.main_window_match_list)
        h_layout.addLayout(main_window_button_layout)
        main_window_central_widget.setLayout(h_layout)
        self.setCentralWidget(main_window_central_widget)

    def start_button_clicked(self):
        print("1")

    def edit_match_button_clicked(self):
        self.edit_match_window = EditMatchWindow()
        self.edit_match_window.show()
        self.edit_match_window.destroyed.connect(self.render_match_list)

    def edit_settings_button_clicked(self):
        print("3")

    def quit_button_clicked(self):
        quit_dialog = QMessageBox()
        quit_dialog.setWindowTitle(" ")
        quit_dialog.setIcon(QMessageBox.Information)
        quit_dialog.setText("アプリケーションを終了しますか？")
        quit_dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        quit_dialog.setDefaultButton(QMessageBox.No)
        quit_dialog.setButtonText(QMessageBox.Yes, "はい")
        quit_dialog.setButtonText(QMessageBox.No, "いいえ")

        ret = quit_dialog.exec()

        if ret == QMessageBox.Yes:
            self.app.quit()

    def render_match_list(self):
        self.main_window_match_list.setWidget(MatchListWidget())
        self.main_window_match_list.setWidgetResizable(True)


class MatchListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.match_list_v_layout = QVBoxLayout()
        self.match_list_dict = {}

        self.add_message_label = QLabel("試合を追加してください")
        self.add_message_label.setStyleSheet("color:grey")
        self.match_list_v_layout.addWidget(self.add_message_label)
        if conf.if_match_exists() is False: self.add_message_label.show()
        else: self.add_message_label.hide()

        match_id_low_list = []
        match_id_hi_list = []
        for i in range(int(conf.read_number_of_singles())):
            match_id_low = "s" + str(i + 1)
            match_id_hi = "S" + str(i + 1)

            match_id_low_list.append(match_id_low)
            match_id_hi_list.append(match_id_hi)

        for i in range(int(conf.read_number_of_doubles())):
            match_id_low = "d" + str(i + 1)
            match_id_hi = "D" + str(i + 1)

            match_id_low_list.append(match_id_low)
            match_id_hi_list.append(match_id_hi)

        for i in range(len(match_id_low_list)):
            match_id_low = match_id_low_list[i]
            match_id_hi = match_id_hi_list[i]
            singles_or_doubles = match_id_low[0]
            match_frame_name = "match_frame_" + match_id_low
            match_h_layout_name = "match_h_layout_" + match_id_low
            player_name = ""
            player_name_1 = ""
            player_name_2 = ""
            if singles_or_doubles == "s": player_name = conf.read_value("singles", match_id_hi)
            else:
                player_name_1 = conf.read_value("doubles", match_id_hi + "p1")
                player_name_2 = conf.read_value("doubles", match_id_hi + "p2")
            label_name = "label_" + match_id_low
            add_button_name = "add_button_" + match_id_low

            menu_button_name = "menu_button_" + match_id_low
            menu_name = "menu_" + match_id_low
            video_count_label_name = "video_count_label_button_" + match_id_low

            # create match frame and h layout
            setattr(self, match_frame_name, QFrame())
            getattr(self, match_frame_name).setFrameStyle(QFrame.Panel | QFrame.Plain)
            getattr(self, match_frame_name).setLineWidth(1)
            getattr(self, match_frame_name).setFixedHeight(50)

            setattr(self, match_h_layout_name, QHBoxLayout())

            # add content to h layout
            if singles_or_doubles == "s": setattr(self, label_name, QLabel(match_id_hi + " " + player_name))
            else: setattr(self, label_name, QLabel(match_id_hi + " " + player_name_1 + " " + player_name_2))
            getattr(self, match_h_layout_name).addWidget(getattr(self, label_name))

            getattr(self, match_h_layout_name).addStretch()

            setattr(self, video_count_label_name, QLabel(""))
            getattr(self, video_count_label_name).setStyleSheet("color:grey")
            getattr(self, match_h_layout_name).addWidget(getattr(self, video_count_label_name))
            getattr(self, match_h_layout_name).addWidget(getattr(self, video_count_label_name))
            getattr(self, video_count_label_name).hide()

            setattr(self, add_button_name, QPushButton("動画を選択"))
            getattr(self, match_h_layout_name).addWidget(getattr(self, add_button_name))

            setattr(self, menu_name, QMenu())
            getattr(self, menu_name).addAction("追加で選択", lambda m=match_id_low: self.add_button_clicked(m))
            getattr(self, menu_name).addAction("選択をリセット", lambda m=match_id_low: self.remove_action_triggered(m))
            setattr(self, menu_button_name, QPushButton("・"))
            """ fix button
            getattr(self, menu_button_name).setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            getattr(self, menu_button_name).setFixedSize(32, 32)
            getattr(self, menu_button_name).setIcon(QIcon("images/three-dots-menu.svg"))
            getattr(self, menu_button_name).setFlat(True)
            """
            getattr(self, menu_button_name).setMenu(getattr(self, menu_name))
            getattr(self, match_h_layout_name).addWidget(getattr(self, menu_button_name))
            getattr(self, menu_button_name).hide()

            # add h layout to frame
            getattr(self, match_frame_name).setLayout(getattr(self, match_h_layout_name))

            self.match_list_v_layout.addWidget(getattr(self, match_frame_name))

            # push button signal
            self.match_list_dict.update({match_id_low: getattr(self, add_button_name)})

            # create list for files
            file_list_name = "file_list_" + match_id_low
            setattr(self, file_list_name, [])

        for button in self.match_list_dict:
            self.match_list_dict[button].clicked.connect(lambda _, b=button: self.add_button_clicked(b))

        self.match_list_v_layout.addStretch()
        self.setLayout(self.match_list_v_layout)

    def add_button_clicked(self, match_id):
        # file dialog settings
        file_list_name = "file_list_" + match_id
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.exec()

        # save selected files to list
        for file in file_dialog.selectedFiles():
            getattr(self, file_list_name).append(file)

        # change ui
        video_count_text = ""
        label_name = "video_count_label_button_" + match_id
        menu_button_name = "menu_button_" + match_id
        add_button_name = "add_button_" + match_id
        if len(getattr(self, file_list_name)) != 0:
            video_count_text = str(len(getattr(self, file_list_name))) + "本の動画を選択済み"
            getattr(self, label_name).setStyleSheet("color:grey")
            getattr(self, label_name).setText(video_count_text)
            getattr(self, label_name).show()
            getattr(self, menu_button_name).show()
            getattr(self, add_button_name).hide()
        else:
            video_count_text = "動画を選択してください"
            getattr(self, label_name).setStyleSheet("color:red")
            getattr(self, label_name).setText(video_count_text)
            getattr(self, label_name).show()
            getattr(self, menu_button_name).hide()
            getattr(self, add_button_name).show()

    def remove_action_triggered(self, match_id):
        # clear list
        file_list_name = "file_list_" + match_id
        getattr(self, file_list_name).clear()

        # update ui
        label_name = "video_count_label_button_" + match_id
        menu_button_name = "menu_button_" + match_id
        add_button_name = "add_button_" + match_id
        getattr(self, label_name).hide()
        getattr(self, menu_button_name).hide()
        getattr(self, add_button_name).show()
