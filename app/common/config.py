# coding:utf-8
import sys
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, 
                            OptionsValidator, Theme, ColorConfigItem, EnumSerializer, 
                            BoolValidator, RangeConfigItem, RangeValidator)








def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Configuration of application """
    
    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", 
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    
    # personalization
    themeMode = OptionsConfigItem(
        "QFluentWidgets", "ThemeMode", Theme.AUTO, OptionsValidator(Theme), EnumSerializer(Theme), restart=True)
    themeColor = ColorConfigItem("QFluentWidgets", "ThemeColor", '#009faa')
    
    # background settings
    backgroundImageEnabled = ConfigItem("Background", "ImageEnabled", False, BoolValidator())
    backgroundImagePath = ConfigItem("Background", "ImagePath", "")
    backgroundOpacity = RangeConfigItem("Background", "Opacity", 30, RangeValidator(0, 100))
    backgroundBlurRadius = RangeConfigItem("Background", "BlurRadius", 0, RangeValidator(0, 50))
    backgroundDisplayMode = OptionsConfigItem(
        "Background", "DisplayMode", "Keep Aspect Ratio", 
        OptionsValidator(["Stretch", "Keep Aspect Ratio", "Tile", "Original Size", "Fit Window"])
    )


# Create global config instance
cfg = Config()

# URLs
HELP_URL = "https://qfluentwidgets.com"
FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
EXAMPLE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples"

# Application info
AUTHOR = "PyQt-Fluent-Widgets"
VERSION = "1.0.0"
YEAR = 2024

# Load configuration
qconfig.load('config/config.json', cfg) 