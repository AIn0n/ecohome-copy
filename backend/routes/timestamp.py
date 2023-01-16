from fastapi import APIRouter
from models.timestamp import Timestamp, Weekdays
from config.db import collection
from schemas.timestamp import timestamp_entities

timestamp = APIRouter()


@timestamp.post("/{room}/device/{device}/timestamp")
def add_timestamp(room: str, device: str, timestamp: Timestamp):
    collection.update_one(
        {"name": room, "devices.name": device},
        {"$push": {"devices.$.timestamps": dict(timestamp)}},
    )
    return {"message": "sucessfully added timestamp"}


@timestamp.post("/{room}/device/{device}/timestamp-update")
def add_timestamp(room: str, device: str, timestamps: list[Timestamp]):
    collection.update_one(
        {"name": room, "devices.name": device},
        {"$set": {"devices.$.timestamps": [dict(t) for t in timestamps]}},
    )
    return {"message": "sucessfully updated timestamps"}


@timestamp.get("/{room}/device/{device}/timestamp")
def get_timestamps(room: str, device: str):
    result = collection.find_one(
        {"name": room, "devices.name": device}, {"devices.$": 1}
    )["devices"][0]["timestamps"]

    return timestamp_entities(result)


@timestamp.get("/day2number")
def get_day_to_number_mapping_dict():
    return {name.lower(): x.value for name, x in Weekdays.__members__.items()}
