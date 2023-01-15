from pydantic import BaseModel
from .device import Device
from typing import Optional


class Room(BaseModel):
    name: str
    devices: Optional[list[Device]] = []
