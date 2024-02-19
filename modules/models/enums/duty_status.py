from enum import Enum


class DutyStatus(Enum):
    NONE = 0
    DRIVING = 1
    ON_DUTY = 2
    OFF_DUTY = 3
    SLEEPING = 4
    YM = 5  # weather factor
    PC = 6  # personal use
