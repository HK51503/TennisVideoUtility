from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QMessageBox, QGroupBox,
    QLabel, QLineEdit, QGridLayout
)
from PySide6.QtCore import Qt
import match_config_functions as conf


class EditMatchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.main_v_layout = QVBoxLayout()

        # Edit match settings
        config_groupbox = QGroupBox()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("大学名 : "), 0, 0)
        grid_layout.addWidget(QLabel("シングルスの本数 : "), 1, 0)
        grid_layout.addWidget(QLabel("ダブルスの本数 : "), 2, 0)

        self.university_name_lineedit = QLineEdit(conf.read_university())
        grid_layout.addWidget(self.university_name_lineedit, 0, 1)

        if conf.read_number_of_singles() == "0":
            self.number_of_singles_lineedit = QLineEdit("")
        else:
            self.number_of_singles_lineedit = QLineEdit(conf.read_number_of_singles())
        grid_layout.addWidget(self.number_of_singles_lineedit, 1, 1)

        if conf.read_number_of_doubles() == "0":
            self.number_of_doubles_lineedit = QLineEdit("")
        else:
            self.number_of_doubles_lineedit = QLineEdit(conf.read_number_of_doubles())
        grid_layout.addWidget(self.number_of_doubles_lineedit, 2, 1)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red;")
        grid_layout.addWidget(self.warning_label, 1, 2)
        apply_button = QPushButton()
        apply_button.setText("本数を適用")
        apply_button.clicked.connect(self.apply_button_clicked)
        grid_layout.addWidget(apply_button, 2, 2)

        config_groupbox.setLayout(grid_layout)

        # Add player names
        self.matches_h_layout = QHBoxLayout()

        self.singles_groupbox = QGroupBox()
        self.singles_v_layout = QVBoxLayout()
        self.singles_gridlayout = QGridLayout()
        self.singles_v_layout.addLayout(self.singles_gridlayout)
        self.singles_v_layout.addStretch()
        self.singles_groupbox.setLayout(self.singles_v_layout)
        self.matches_h_layout.addWidget(self.singles_groupbox)
        self.matches_h_layout.setStretch(0, 1)

        self.doubles_groupbox = QGroupBox()
        self.doubles_v_layout = QVBoxLayout()
        self.doubles_gridlayout = QGridLayout()
        self.doubles_v_layout.addLayout(self.doubles_gridlayout)
        self.doubles_v_layout.addStretch()
        self.doubles_groupbox.setLayout(self.doubles_v_layout)
        self.matches_h_layout.addWidget(self.doubles_groupbox)
        self.matches_h_layout.setStretch(1, 1)

        self.main_v_layout.addWidget(config_groupbox)
        self.main_v_layout.addLayout(self.matches_h_layout)
        self.setLayout(self.main_v_layout)

        self.render_players()

    def apply_button_clicked(self):
        validation_1 = str.isdecimal(self.number_of_singles_lineedit.text())
        validation_2 = str.isdecimal(self.number_of_doubles_lineedit.text())
        validation = validation_1 and validation_2

        if validation is True:
            # remove warning label text if it exists
            self.warning_label.setText("")
            # save to match config
            self.save_players()

            # write numbers to match config
            conf.set_number_of_singles(self.number_of_singles_lineedit.text())
            conf.set_number_of_doubles(self.number_of_doubles_lineedit.text())

            # render window
            self.render_players()

        else:
            self.warning_label.setText("有効な数字を入力してください")

        self.update()

    def render_players(self):
        for i in reversed(range(self.singles_gridlayout.count())):
            self.singles_gridlayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.doubles_gridlayout.count())):
            self.doubles_gridlayout.itemAt(i).widget().setParent(None)

        number_of_singles = int(conf.read_number_of_singles())
        number_of_doubles = int(conf.read_number_of_doubles())

        for i in range(number_of_singles):
            label_name = "label_s" + str(i+1)
            label_text = "S" + str(i+1)
            setattr(self, label_name, QLabel(label_text))

            lineedit_name = "lineedit_s" + str(i+1)
            setattr(self, lineedit_name, QLineEdit(""))

            self.singles_gridlayout.addWidget(getattr(self, label_name), i, 0)

            section_name = "S" + str(i + 1)
            lineedit = getattr(self, lineedit_name)
            try: lineedit.setText(conf.read_value(section_name, "p"))
            except: lineedit.setText("")
            self.singles_gridlayout.addWidget(lineedit, i, 1)

        for i in range(number_of_doubles):
            section_name = "D" + str(i+1)
            # player1
            label_name_1 = "label_d" + str(i+1) + "_1"
            label_text_1 = "D" + str(i+1) + "①"
            setattr(self, label_name_1, QLabel(label_text_1))

            lineedit_name_1 = "lineedit_d" + str(i+1) + "_1"
            setattr(self, lineedit_name_1, QLineEdit(""))

            self.doubles_gridlayout.addWidget(getattr(self, label_name_1), i*2, 0)

            lineedit_1 = getattr(self, lineedit_name_1)
            try: lineedit_1.setText(conf.read_value(section_name, "p1"))
            except: lineedit_1.setText("")
            self.doubles_gridlayout.addWidget(getattr(self, lineedit_name_1), i*2, 1)

            # player2
            label_name_2 = "label_d" + str(i+1) + "_2"
            label_text_2 = "D" + str(i + 1) + "②"
            setattr(self, label_name_2, QLabel(label_text_2))

            lineedit_name_2 = "lineedit_d" + str(i + 1) + "_2"
            setattr(self, lineedit_name_2, QLineEdit(""))

            self.doubles_gridlayout.addWidget(getattr(self, label_name_2), i*2+1, 0)

            lineedit_2 = getattr(self, lineedit_name_2)
            try: lineedit_2.setText(conf.read_value(section_name, "p2"))
            except: lineedit_2.setText("")
            self.doubles_gridlayout.addWidget(getattr(self, lineedit_name_2), i*2+1, 1)

    def save_players(self):
        # save university name
        conf.set_university(self.university_name_lineedit.text())

        # save player list
        for i in range(int(conf.read_number_of_singles())):
            lineedit_name = "lineedit_s" + str(i + 1)
            section_name = "S" + str(i+1)
            conf.add_section(section_name)
            conf.set_value(section_name, "p", getattr(self, lineedit_name).text())

        for i in range(int(conf.read_number_of_doubles())):
            lineedit_name_1 = "lineedit_d" + str(i+1) + "_1"
            lineedit_name_2 = "lineedit_d" + str(i+1) + "_2"
            section_name = "D" + str(i+1)
            option_name_1 = "D" + str(i+1) + "p1"
            option_name_2 = "D" + str(i+1) + "p2"
            conf.add_section(section_name)
            conf.set_value(section_name, "p1", getattr(self, lineedit_name_1).text())
            conf.set_value(section_name, "p2", getattr(self, lineedit_name_2).text())

    def closeEvent(self, event):
        super().closeEvent(event)
        self.save_players()
        self.deleteLater()
