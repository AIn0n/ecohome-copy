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
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    weekdays: Weekdays
