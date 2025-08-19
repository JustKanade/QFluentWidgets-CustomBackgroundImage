# coding:utf-8
from qfluentwidgets import (SettingCardGroup, OptionsSettingCard, HyperlinkCard, 
                            PrimaryPushSettingCard, ScrollArea, 
                            ExpandLayout, CustomColorSettingCard, setTheme, 
                            setThemeColor, InfoBar, SwitchSettingCard, RangeSettingCard,
                            PushSettingCard, SettingCard, PushButton)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout

from ..common import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, isWin11, StyleSheet
from ..background import get_background_manager


class BackgroundImageCard(SettingCard):
    """ Custom setting card with select and clear buttons for background image """
    
    def __init__(self, title, content, icon, parent=None):
        super().__init__(icon, title, content, parent)
        
        # Create buttons
        self.selectButton = PushButton(self.tr('Select image'), self)
        self.clearButton = PushButton(self.tr('Clear'), self)
        
        # Create button layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.addWidget(self.selectButton)
        self.buttonLayout.addWidget(self.clearButton)
        
        # Add button layout to the card
        self.hBoxLayout.addLayout(self.buttonLayout)
        self.hBoxLayout.addSpacing(16)
        
        # Initialize display
        self._updateDisplay()
        
    def _updateDisplay(self):
        """ Update the card display based on current background image path """
        bg_path = cfg.get(cfg.backgroundImagePath)
        if bg_path:
            import os
            file_name = os.path.basename(bg_path)
            self.setContent(f"Selected: {file_name}")
            self.clearButton.setEnabled(True)
        else:
            self.setContent(self.tr('Choose a custom background image file'))
            self.clearButton.setEnabled(False)


class SettingInterface(ScrollArea):
    """ Settings interface """
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        
        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)
        
        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.micaEnabled,
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of your application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        
        # background settings
        self.backgroundGroup = SettingCardGroup(
            self.tr('Background'), self.scrollWidget)
        self.backgroundEnabledCard = SwitchSettingCard(
            FIF.PHOTO,
            self.tr('Background image'),
            self.tr('Enable custom background image for the application'),
            cfg.backgroundImageEnabled,
            self.backgroundGroup
        )
        self.backgroundImageCard = BackgroundImageCard(
            self.tr('Background image path'),
            self.tr('Choose a custom background image file'),
            FIF.FOLDER,
            self.backgroundGroup
        )
        self.backgroundOpacityCard = RangeSettingCard(
            cfg.backgroundOpacity,
            FIF.TRANSPARENT,
            self.tr('Background opacity'),
            self.tr('Adjust the opacity of the background image (0-100%)'),
            self.backgroundGroup
        )
        self.backgroundBlurCard = RangeSettingCard(
            cfg.backgroundBlurRadius,
            FIF.BRUSH,
            self.tr('Background blur'),
            self.tr('Adjust the blur radius of the background image (0-50px)'),
            self.backgroundGroup
        )
        
        # about
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('Open help page'),
            FIF.HELP,
            self.tr('Help'),
            self.tr(
                'Discover new features and learn useful tips about PyQt-Fluent-Widgets'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('Provide feedback'),
            FIF.FEEDBACK,
            self.tr('Provide feedback'),
            self.tr('Help us improve PyQt-Fluent-Widgets by providing feedback'),
            self.aboutGroup
        )

        
        # initialize background manager
        self.backgroundManager = get_background_manager(cfg)
        
        self.__initWidget()
    
    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')
        
        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)
        
        self.micaCard.setEnabled(isWin11())
        
        # initialize background cards state
        self.__updateBackgroundCardsState()
        
        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()
    
    def __initLayout(self):
        """ Initialize layout """
        self.settingLabel.move(36, 30)
        
        # add cards to groups
        self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        
        self.backgroundGroup.addSettingCard(self.backgroundEnabledCard)
        self.backgroundGroup.addSettingCard(self.backgroundImageCard)
        self.backgroundGroup.addSettingCard(self.backgroundOpacityCard)
        self.backgroundGroup.addSettingCard(self.backgroundBlurCard)
        
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        
        # add setting card groups to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.backgroundGroup)
        self.expandLayout.addWidget(self.aboutGroup)
    

    

    
    def __connectSignalToSlot(self):
        """ connect signal to slot """

        
        # personalization
        cfg.themeChanged.connect(setTheme)
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
        self.micaCard.checkedChanged.connect(self.__onMicaToggled)
        
        # background settings
        self.backgroundEnabledCard.checkedChanged.connect(self.__onBackgroundEnabledChanged)
        self.backgroundImageCard.selectButton.clicked.connect(self.__onSelectBackgroundImage)
        self.backgroundImageCard.clearButton.clicked.connect(self.__onClearBackgroundImage)
        self.backgroundOpacityCard.valueChanged.connect(self.__onBackgroundOpacityChanged)
        self.backgroundBlurCard.valueChanged.connect(self.__onBackgroundBlurChanged)
        
        # about
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
    
    def __onMicaToggled(self, isChecked):
        """ Handle mica effect toggle """
        # Get parent window and apply mica effect
        parent_window = self.window()
        if hasattr(parent_window, 'setMicaEffectEnabled'):
            parent_window.setMicaEffectEnabled(isChecked)
    
    def __onBackgroundEnabledChanged(self, isChecked: bool):
        """ Handle background image enable/disable """
        cfg.set(cfg.backgroundImageEnabled, isChecked)
        self.backgroundManager.update_background()
        self.__updateBackgroundCardsState()
        self.__updateBackgroundPreview()
    
    def __onSelectBackgroundImage(self):
        """ Handle background image selection """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr('Select background image'),
            '',
            self.tr('Image files (*.jpg *.jpeg *.png *.bmp *.gif *.webp)')
        )
        
        if file_path:
            cfg.set(cfg.backgroundImagePath, file_path)
            self.backgroundManager.update_background()
            self.backgroundImageCard._updateDisplay()
            self.__updateBackgroundPreview()
    
    def __onClearBackgroundImage(self):
        """ Handle background image clearing """
        cfg.set(cfg.backgroundImagePath, "")
        self.backgroundManager.update_background()
        self.backgroundImageCard._updateDisplay()
        self.__updateBackgroundPreview()
    
    def __onBackgroundOpacityChanged(self, value: int):
        """ Handle background opacity change """
        cfg.set(cfg.backgroundOpacity, value)
        self.backgroundManager.update_background()
        self.__updateBackgroundPreview()
    
    def __onBackgroundBlurChanged(self, value: int):
        """ Handle background blur radius change """
        cfg.set(cfg.backgroundBlurRadius, value)
        self.backgroundManager.update_background()
        self.__updateBackgroundPreview()
    
    def __updateBackgroundPreview(self):
        """ Update background preview in main window """
        parent_window = self.window()
        if hasattr(parent_window, 'update'):
            parent_window.update()  # Trigger repaint to show background changes
    
    def __updateBackgroundCardsState(self):
        """ Update the enabled state of background setting cards """
        is_background_enabled = cfg.get(cfg.backgroundImageEnabled)
        
        # Enable/disable background related cards based on background enabled state
        self.backgroundImageCard.setEnabled(is_background_enabled)
        self.backgroundOpacityCard.setEnabled(is_background_enabled)
        self.backgroundBlurCard.setEnabled(is_background_enabled)
        
        # Update display when background is enabled/disabled
        if hasattr(self.backgroundImageCard, '_updateDisplay'):
            self.backgroundImageCard._updateDisplay()
 