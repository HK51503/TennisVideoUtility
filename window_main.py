from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QMessageBox, QFrame,
    QLabel, QFileDialog
)
from PySide6.QtCore import Qt
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

        for i in range(int(conf.read_number_of_singles())):
            match_id_low = "s" + str(i+1)
            match_id_hi = "S" + str(i+1)
            match_frame_name = "match_frame_" + match_id_low
            match_h_layout_name = "match_h_layout_" + match_id_low
            player_name = conf.read_value("singles", match_id_hi)
            label_name = "label_" + match_id_low
            add_button_name = "add_button_" + match_id_low

            # create match frame and h layout
            setattr(self, match_frame_name, QFrame())
            getattr(self, match_frame_name).setFrameStyle(QFrame.Panel | QFrame.Plain)
            getattr(self, match_frame_name).setLineWidth(1)
            getattr(self, match_frame_name).setFixedHeight(50)

            setattr(self, match_h_layout_name, QHBoxLayout())

            # add content to h layout
            setattr(self, label_name, QLabel("S"+str(i+1)+" "+player_name))
            getattr(self, match_h_layout_name).addWidget(getattr(self, label_name))

            getattr(self, match_h_layout_name).addStretch()

            setattr(self, add_button_name, QPushButton("動画を追加"))
            getattr(self, match_h_layout_name).addWidget(getattr(self, add_button_name))

            # add h layout to frame
            getattr(self, match_frame_name).setLayout(getattr(self, match_h_layout_name))

            self.match_list_v_layout.addWidget(getattr(self, match_frame_name))

            # push button signal
            self.match_list_dict.update({match_id_low: getattr(self, add_button_name)})

        for i in range(int(conf.read_number_of_doubles())):
            match_id_low = "d" + str(i+1)
            match_id_hi = "D" + str(i+1)
            match_frame_name = "match_frame_" + match_id_low
            match_h_layout_name = "match_h_layout_" + match_id_low
            player_name_1 = conf.read_value("doubles", match_id_hi + "p1")
            player_name_2 = conf.read_value("doubles", match_id_hi + "p2")
            label_name = "label_" + match_id_low
            add_button_name = "add_button_" + match_id_low

            # create match frame and h layout
            setattr(self, match_frame_name, QFrame())
            getattr(self, match_frame_name).setFrameStyle(QFrame.Panel | QFrame.Plain)
            getattr(self, match_frame_name).setLineWidth(1)
            getattr(self, match_frame_name).setFixedHeight(50)

            setattr(self, match_h_layout_name, QHBoxLayout())

            # add content to h layout
            setattr(self, label_name, QLabel("D" + str(i + 1) + " " + player_name_1 + " " + player_name_2))
            getattr(self, match_h_layout_name).addWidget(getattr(self, label_name))

            getattr(self, match_h_layout_name).addStretch()

            setattr(self, add_button_name, QPushButton("動画を追加"))
            getattr(self, match_h_layout_name).addWidget(getattr(self, add_button_name))

            # add h layout to frame
            getattr(self, match_frame_name).setLayout(getattr(self, match_h_layout_name))

            self.match_list_v_layout.addWidget(getattr(self, match_frame_name))

            # push button signal
            self.match_list_dict.update({match_id_low: getattr(self, add_button_name)})

        for button in self.match_list_dict:
            self.match_list_dict[button].clicked.connect(lambda _, b=button: self.add_button_clicked(b))

        self.match_list_v_layout.addStretch()
        self.setLayout(self.match_list_v_layout)

    def add_button_clicked(self, match_id):
        file_dialog = QFileDialog()
        file_dialog.exec()
