from pydantic import BaseModel
from .timestamp import Timestamp
from enum import IntEnum
from typing import Optional


class EnergyClass(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


class DeviceType(IntEnum):
    DEFAULT = 0
    SOLAR = 1
    ACCUMULATOR = 2


class Device(BaseModel):
    energy_class: EnergyClass
    parameter: float
    name: str
    device_type: DeviceType
    timestamps: Optional[list[Timestamp]] = []
