from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QMessageBox, QGroupBox,
    QLabel, QLineEdit, QGridLayout, QCalendarWidget
)
from PySide6.QtCore import Qt, QDate
import functions_match_config as conf
import variables as var
from class_match import SinglesMatch, DoublesMatch


class EditMatchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.main_v_layout = QVBoxLayout()

        self.setWindowTitle(self.tr("試合設定"))

        # Edit match settings
        config_groupbox = QGroupBox()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel(self.tr("大学名 : ")), 0, 0)
        grid_layout.addWidget(QLabel(self.tr("日付 : ")), 1, 0)
        grid_layout.addWidget(QLabel(self.tr("シングルスの本数 : ")), 2, 0)
        grid_layout.addWidget(QLabel(self.tr("ダブルスの本数 : ")), 3, 0)

        self.university_name_lineedit = QLineEdit(conf.read_university())
        grid_layout.addWidget(self.university_name_lineedit, 0, 1, 1, 2)

        self.match_date_lineedit = QLineEdit(conf.read_value("settings", "match_date"))
        self.match_date_lineedit.setReadOnly(True)
        self.match_date_button = QPushButton("📅")
        self.match_date_button.setFixedWidth(25)
        self.match_date_button.clicked.connect(self.match_date_button_clicked)
        grid_layout.addWidget(self.match_date_lineedit, 1, 1)
        grid_layout.addWidget(self.match_date_button, 1, 2)

        if conf.read_number_of_singles() == "0":
            self.number_of_singles_lineedit = QLineEdit("")
        else:
            self.number_of_singles_lineedit = QLineEdit(conf.read_number_of_singles())
        grid_layout.addWidget(self.number_of_singles_lineedit, 2, 1, 1, 2)

        if conf.read_number_of_doubles() == "0":
            self.number_of_doubles_lineedit = QLineEdit("")
        else:
            self.number_of_doubles_lineedit = QLineEdit(conf.read_number_of_doubles())
        grid_layout.addWidget(self.number_of_doubles_lineedit, 3, 1, 1, 2)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red;")
        grid_layout.addWidget(self.warning_label, 2, 3)
        apply_button = QPushButton()
        apply_button.setText(self.tr("本数を適用"))
        apply_button.clicked.connect(self.apply_button_clicked)
        grid_layout.addWidget(apply_button, 3, 3)

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

            # create match object
            singles_differential = int(self.number_of_singles_lineedit.text())-int(conf.read_number_of_singles())
            doubles_differential = int(self.number_of_doubles_lineedit.text())-int(conf.read_number_of_doubles())
            if singles_differential > 0:
                for i in range(int(conf.read_number_of_singles()), int(self.number_of_singles_lineedit.text())):
                    match_id = "s" + str(i+1)
                    var.dict_matches[match_id] = SinglesMatch(match_id)
            elif singles_differential < 0:
                for i in range(int(self.number_of_singles_lineedit.text()), int(conf.read_number_of_singles())):
                    match_id = "s" + str(i+1)
                    section_name = match_id.upper()
                    del var.dict_matches[match_id]
                    conf.set_value(section_name, "p", "")

            if doubles_differential > 0:
                for i in range(int(conf.read_number_of_doubles()), int(self.number_of_doubles_lineedit.text())):
                    match_id = "d" + str(i+1)
                    var.dict_matches[match_id] = DoublesMatch(match_id)
            elif doubles_differential < 0:
                for i in range(int(self.number_of_doubles_lineedit.text()), int(conf.read_number_of_doubles())):
                    match_id = "d" + str(i+1)
                    section_name = match_id.upper()
                    del var.dict_matches[match_id]
                    conf.set_value(section_name, "p1", "")
                    conf.set_value(section_name, "p2", "")

            # save to match config
            self.save_match_config()

            # write numbers to match config
            conf.set_number_of_singles(self.number_of_singles_lineedit.text())
            conf.set_number_of_doubles(self.number_of_doubles_lineedit.text())

            # render window
            self.render_players()

        else:
            self.warning_label.setText(self.tr("有効な数字を入力してください"))
            self.save_match_config()

        self.update()

    def render_players(self):
        for i in reversed(range(self.singles_gridlayout.count())):
            self.singles_gridlayout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.doubles_gridlayout.count())):
            self.doubles_gridlayout.itemAt(i).widget().setParent(None)

        number_of_singles = int(conf.read_number_of_singles())
        number_of_doubles = int(conf.read_number_of_doubles())

        for i in range(number_of_singles):
            match_id = "s" + str(i+1)
            label_name = "label_" + match_id
            label_text = match_id.upper()
            setattr(self, label_name, QLabel(label_text))

            lineedit_name = "lineedit_" + match_id
            setattr(self, lineedit_name, QLineEdit(""))

            self.singles_gridlayout.addWidget(getattr(self, label_name), i, 0)

            lineedit = getattr(self, lineedit_name)
            lineedit.setText(var.dict_matches[match_id].player_name)
            self.singles_gridlayout.addWidget(lineedit, i, 1)

        for i in range(number_of_doubles):
            match_id = "d" + str(i+1)
            match_id_hi = "D" + str(i+1)
            # player1
            label_name_1 = "label_" + match_id + "_1"
            label_text_1 = match_id_hi + "①"
            setattr(self, label_name_1, QLabel(label_text_1))

            lineedit_name_1 = "lineedit_" + match_id + "_1"
            setattr(self, lineedit_name_1, QLineEdit(""))

            self.doubles_gridlayout.addWidget(getattr(self, label_name_1), i*2, 0)

            lineedit_1 = getattr(self, lineedit_name_1)
            lineedit_1.setText(var.dict_matches[match_id].player_name_1)
            self.doubles_gridlayout.addWidget(getattr(self, lineedit_name_1), i*2, 1)

            # player2
            label_name_2 = "label_" + match_id + "_2"
            label_text_2 = match_id_hi + "②"
            setattr(self, label_name_2, QLabel(label_text_2))

            lineedit_name_2 = "lineedit_" + match_id + "_2"
            setattr(self, lineedit_name_2, QLineEdit(""))

            self.doubles_gridlayout.addWidget(getattr(self, label_name_2), i*2+1, 0)

            lineedit_2 = getattr(self, lineedit_name_2)
            lineedit_2.setText(var.dict_matches[match_id].player_name_2)
            self.doubles_gridlayout.addWidget(getattr(self, lineedit_name_2), i*2+1, 1)

    def save_match_config(self):
        # save university name
        conf.set_university(self.university_name_lineedit.text())
        var.university_name = self.university_name_lineedit.text()
        conf.set_value("settings", "match_date", var.match_date)

        # save player list
        for i in range(int(conf.read_number_of_singles())):
            lineedit_name = "lineedit_s" + str(i+1)
            match_id = "s" + str(i+1)
            var.dict_matches[match_id].set_player(getattr(self, lineedit_name).text())

            section_name = "S" + str(i + 1)
            conf.add_section(section_name)
            conf.set_value(section_name, "p", getattr(self, lineedit_name).text())

        for i in range(int(conf.read_number_of_doubles())):
            lineedit_name_1 = "lineedit_d" + str(i+1) + "_1"
            lineedit_name_2 = "lineedit_d" + str(i+1) + "_2"
            match_id = "d" + str(i+1)
            var.dict_matches[match_id].set_player(getattr(self, lineedit_name_1).text(), getattr(self, lineedit_name_2).text())

            section_name = "D" + str(i + 1)
            conf.add_section(section_name)
            conf.set_value(section_name, "p1", getattr(self, lineedit_name_1).text())
            conf.set_value(section_name, "p2", getattr(self, lineedit_name_2).text())

    def match_date_button_clicked(self):
        self.calendar_window = EditMatchDateWindow()
        self.calendar_window.setWindowTitle(self.tr("日付を選択"))
        self.calendar_window.show()
        self.calendar_window.calendar_widget.selectionChanged.connect(self.update_date)

    def update_date(self):
        self.match_date_lineedit.setText(QDate.toString(self.calendar_window.calendar_widget.selectedDate(), format=Qt.ISODate))
        self.update()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.save_match_config()
        self.deleteLater()


class EditMatchDateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)

        self.main_h_layout = QHBoxLayout()
        self.setLayout(self.main_h_layout)

        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setSelectedDate(QDate.fromString(var.match_date, format=Qt.ISODate))
        self.main_h_layout.addWidget(self.calendar_widget)

    def closeEvent(self, event):
        super().closeEvent(event)
        var.match_date = QDate.toString(self.calendar_widget.selectedDate(), format=Qt.ISODate)
        self.deleteLater()
