from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("仮タイトル")
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

        main_window_match_list = QScrollArea()
        h_layout = QHBoxLayout()
        h_layout.addWidget(main_window_match_list)
        h_layout.addLayout(main_window_button_layout)
        main_window_central_widget.setLayout(h_layout)
        self.setCentralWidget(main_window_central_widget)

    def start_button_clicked(self):
        print("1")

    def edit_match_button_clicked(self):
        print("2")

    def edit_settings_button_clicked(self):
        print("3")

    def quit_button_clicked(self):
        print("4")

