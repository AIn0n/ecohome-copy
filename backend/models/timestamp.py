from pydantic import BaseModel
from enum import IntFlag, auto


class Weekdays(IntFlag):
    MONDAY = auto()
    TUESDAY = auto()
    WENDESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class Timestamp(BaseModel):
    start: int
    end: int
    weekdays: Weekdays
