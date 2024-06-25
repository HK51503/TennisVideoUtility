from PySide6.QtWidgets import QApplication
from window_main import MainWindow
import sys
import match_config_functions as conf
import variables as var
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help = "Add match config file.", required = False, default = "")
args = parser.parse_args()
if args.config:
    var.match_config_file_name = args.config

conf.initialize()

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()
