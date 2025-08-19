# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common import cfg
from app.view import MainWindow


# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization - set to English explicitly
from PyQt5.QtCore import QLocale
locale = QLocale(QLocale.English)
translator = FluentTranslator(locale)
app.installTranslator(translator)

# set application font
font = QFont()
font.setFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
app.setFont(font)

# create main window
w = MainWindow()
w.show()

# close splash screen after showing main window
if hasattr(w, 'splashScreen'):
    w.splashScreen.finish()

# run application
app.exec_() 