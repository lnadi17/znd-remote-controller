from enum import Enum


class DisplayMode(Enum):
    ON = "on"
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


class ButtonNumber(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class TraceFormat(Enum):
    LINEAR = "mlinear"
    DB = "magnitude"
    PHASE = "phase"
    UPHASE = "uphase"
    COMPLEX = "complex"
    SMITH = "smith"
    ISMITH = "ismith"
    REAL = "real"
    IMAGINARY = "imaginary"
    GDELAY = "gdelay"
    SWR = "swr"
    LOG = "logarithmic"


class SweepMode(Enum):
    CONTINUOUS = "on"
    SINGLE = "off"
