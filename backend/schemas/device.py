from models.device import DeviceType, EnergyClass
from schemas.timestamp import timestamp_entities


def device_entity(item) -> dict:
    return {
        "parameter": item["parameter"],
        "energy_class": EnergyClass(item["energy_class"]),
        "name": item["name"],
        "device_type": DeviceType(item["device_type"]),
        "timestamps": timestamp_entities(item["timestamps"]),
    }
