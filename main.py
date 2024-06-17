from PySide6.QtWidgets import QApplication
from window_main import MainWindow
import sys
import match_config_functions as conf
import variables as var

conf.initialize()

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()
