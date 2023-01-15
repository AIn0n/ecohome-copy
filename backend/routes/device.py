from fastapi import APIRouter
from models.device import Device, EnergyClass, DeviceType
from schemas.device import device_entity
from config.db import collection

device = APIRouter()


def retrieve_devices_from_room(room: str) -> list:
    return [device_entity(n) for n in collection.find_one({"name": room})["devices"]]


@device.get("/{room}/device")
def get_devices_from_room(room: str):
    return retrieve_devices_from_room(room)


@device.post("/{room}/device")
def add_new_device(room: str, device: Device):
    # check if devices exist
    if device.name in map(lambda x: x["name"], retrieve_devices_from_room(room)):
        return {"message": "device already created"}
    if len(device.name) < 1:
        return {"message": "cannot add device - empty name"}
    collection.update_one({"name": room}, {"$push": {"devices": dict(device)}})
    return {"message": "successfully added new device <3"}


@device.delete("/{room}/device/{device}")
def remove_device(room: str, device: str):
    result = collection.update_many(
        {"name": room}, {"$pull": {"devices": {"name": device}}}
    )
    return {
        "message": "deleted device" if result.modified_count else "device not found"
    }


@device.get("/energy-class")
def get_all_possible_energy_classes():
    return {member.name: member.value for member in EnergyClass}


@device.get("/device-type")
def get_all_device_classes():
    return {it.name: it.value for it in DeviceType}
