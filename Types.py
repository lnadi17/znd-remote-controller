from enum import Enum


class DisplayMode(Enum):
    CONTINUOUS = "on"
    ONCE = "once"
    OFF = "off"


class TSLockMode(Enum):
    OFF = "off"
    DIAGRAMS = "diagrams"
    SCREEN = "screen"


class SaveFormat(Enum):
    COMPLEX = "complex"
    LINPHASE = "linphase"
    LOGPHASE = "logphase"


class DecimalSeparator(Enum):
    POINT = 'point'
    COMMA = 'comma'


class FieldSeparator(Enum):
    SEMICOLON = 'semicolon'
    COMMA = 'comma'
    TAB = 'tabulator'
    SPACE = 'space'
