from enum import Enum, auto, unique
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea, QFormLayout, QGroupBox, QPushButton
from Graph import UpdateGraph
from Exceptions import ErrorWindow
from Look_Config import Config

@unique
class Color(Enum):
    NOT_CLICKED = auto()
    CLICKED = auto()


class CountryBox(QScrollArea):
    # implementacja panelu z krajami (stworzenie boxa + przyciskow dla panstw)
    def __init__(self, countries, parent):
        super().__init__()
        self.verticalScrollBar().setDisabled(False)
        self.parent = parent
        self.all_buttons = []
        self.__init_view(countries)
        self.all_countries = []

    def __init_view(self, countries):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        self.all_countries = countries
        for i in range(len(self.all_countries)):
            name = self.all_countries[i]
            btn = PushCountryButtons(name, self.parent
                                     )  # tu trzeba zmienic na PushButton jak bedzie wiadomo jak kolorki
            self.all_buttons.append(btn)
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)


class PushCountryButtons(QPushButton):
    def __init__(self, name, parent):
        super().__init__(name)
        self.__name = name
        self.parent = parent
        self.mode = Color.NOT_CLICKED
        self.get_color()
        self.clicked.connect(self.func_click_me())
        self.setFont(QFont("Helvetica", 10))
        # self.shadow = QGraphicsDropShadowEffect()
        # self.shadow.setBlurRadius(5)
        # self.shadow.setXOffset(3)
        # self.shadow.setYOffset(3)
        # self.setGraphicsEffect(self.shadow)

    def func_click_me(self):
        return lambda _: self.names()

    def names(self):

        if self.mode == Color.CLICKED:
            name = self.__name
            self.parent.Data.remove_country(name)
            self.get_color()
            UpdateGraph(self.parent)
        else:
            if len(self.parent.Data.get_countries()) < 6:
                name = self.__name
                self.parent.Data.add_country(name)
                self.get_color()
                UpdateGraph(self.parent)
            else:
                ErrorWindow("Mozna dodac maksymalnie 6 krajow!")

    def get_color(self):
        if self.__name in self.parent.Data.get_countries():
            self.mode = Color.CLICKED
            self.setStyleSheet(Config.COUNTRY_BTN_CLICKED)
        else:
            self.mode = Color.NOT_CLICKED
            self.setStyleSheet(Config.COUNTRY_BTN_UNCLICKED)
