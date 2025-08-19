# coding:utf-8
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (FluentWindow, NavigationItemPosition, MessageBox, 
                            SplashScreen, SystemThemeListener, isDarkTheme, setTheme,
                            NavigationAvatarWidget)
from qfluentwidgets import FluentIcon as FIF

from .settings_interface import SettingInterface
from ..common import cfg
from ..background import get_background_manager


class MainWindow(FluentWindow):
    """ Main window """
    
    def __init__(self):
        super().__init__()
        self.initWindow()
        
        # create system theme listener
        self.themeListener = SystemThemeListener(self)
        
        # create sub interface
        self.settingInterface = SettingInterface(self)
        
        # initialize background manager
        self.backgroundManager = get_background_manager(cfg)
        
        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        
        # set sidebar expand width
        self.navigationInterface.setExpandWidth(150)
        
        # force sidebar to always expanded state (disable collapsible)
        self.navigationInterface.setCollapsible(False)
        
        # ensure sidebar is expanded
        self.navigationInterface.expand(useAni=False)
        
        self.connectSignalToSlot()
        
        # add items to navigation interface
        self.initNavigation()
        
        # start theme listener
        self.themeListener.start()
    
    def connectSignalToSlot(self):
        """ Connect signal to slot """
        pass
    
    def initNavigation(self):
        """ Initialize navigation """
        # add navigation items
        self.addSubInterface(
            self.settingInterface, 
            FIF.SETTING, 
            "Settings",
            NavigationItemPosition.TOP
        )
        
        # add separator
        self.navigationInterface.addSeparator()
        
        # add shoko avatar to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', 'app/resource/shoko.png'),
            onClick=lambda: QDesktopServices.openUrl(QUrl("https://github.com/zhiyiYo")),
            position=NavigationItemPosition.BOTTOM
        )
        
        # add info item to bottom
        self.navigationInterface.addItem(
            routeKey='info',
            icon=FIF.INFO,
            text='About',
            onClick=None,
            selectable=False,
            tooltip='About this application',
            position=NavigationItemPosition.BOTTOM
        )
    
    def initWindow(self):
        """ Initialize window """
        self.resize(1200, 800)
        self.setMinimumSize(600, 500)
        self.setWindowIcon(QIcon('app/resource/logo.png'))
        self.setWindowTitle('PyQt Fluent Widgets Custom Background Image Settings Demo')
        
        # set mica effect
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        
        # close splash screen after initialization
        QApplication.processEvents()
    

    

    
    def resizeEvent(self, e):
        """ Resize event """
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
    
    def paintEvent(self, event):
        """ Paint event - draw background image if enabled """
        super().paintEvent(event)
        
        # Draw background image if enabled
        if hasattr(self, 'backgroundManager') and self.backgroundManager.is_background_enabled():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Get background pixmap
            window_size = self.size()
            background_pixmap = self.backgroundManager.get_background_pixmap(window_size)
            
            if background_pixmap and not background_pixmap.isNull():
                # Apply opacity
                opacity = self.backgroundManager.get_background_opacity() / 100.0  # Convert percentage to float
                painter.setOpacity(opacity)
                
                # Calculate position to center the image
                pixmap_size = background_pixmap.size()
                x = max(0, (window_size.width() - pixmap_size.width()) // 2)
                y = max(0, (window_size.height() - pixmap_size.height()) // 2)
                
                # Draw the background image
                painter.drawPixmap(x, y, background_pixmap)
            
            painter.end() 