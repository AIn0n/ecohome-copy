from pydantic import BaseModel
from enum import IntFlag


class Weekdays(IntFlag):
    MONDAY = 1
    TUESDAY = 2
    WENDESDAY = 4
    THURSDAY = 8
    FRIDAY = 16
    SATURDAY = 32
    SUNDAY = 64


class Timestamp(BaseModel):
    start: int
    end: int
    weekdays: Weekdays
