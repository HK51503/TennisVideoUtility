from PySide6 import QtWidgets, QtCore
from window_main import MainWindow
import functions_match_config as conf
import functions_settings_config as settings
import variables as var
import argparse, sys, darkdetect, os
"""
# use this to trace variables
from watchpoints import watch

watch(var.dict_matches)
"""
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Add match config file.", required=False, default="")
args = parser.parse_args()
if os.path.exists(args.config):
    var.match_config_file_name = args.config
elif args.config:
    exit("Config file not found")

conf.initialize()

var.theme = darkdetect.theme()

app = QtWidgets.QApplication(sys.argv)

qm_file = "./resources/translation-bin/en_US.qm"
if settings.read_value("general_settings", "language") == "en":
    translator = QtCore.QTranslator(app)
    if translator.load(QtCore.QLocale.English, qm_file):
        QtCore.QCoreApplication.installTranslator(translator)
        var.loaded_language = "en"
    else:
        var.loaded_language = "ja"
else:
    var.loaded_language = "ja"

window = MainWindow(app)
window.show()

app.exec()
