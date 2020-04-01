from enum import Enum


class Color(bytes, Enum):
    def __new__(cls, value, label):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        return obj

    RED = (0, "rgb(255, 0, 0)")
    GREEN = (1, "rgb(0, 255, 0)")
    BLUE = (2, "rgb(0, 0, 255)")
    YELLOW = (3, "rgb(255, 255, 0)")
    WHITE = (4, "rgb(255, 255, 255)")
    BLACK = (5, "rgb(0, 0, 0)")
    PURPLE = (6, "rgb(142, 0, 142)")
    BROWN = (7, "rgb(107, 61, 2)")
    GREY = (8, "rgb(122, 122, 122)")
    AQUA = (9, "rgb(0, 255, 255)")