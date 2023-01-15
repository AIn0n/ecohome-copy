from fastapi import APIRouter
from models.timestamp import Timestamp
from config.db import collection
from schemas.timestamp import timestamp_entities

timestamp = APIRouter()

@timestamp.post("/{room}/device/{device}/timestamp")
def add_timestamp(room: str, device: str, timestamp: Timestamp):
  collection.update_one(
    {"name": room, "devices.name": device},
    {
      "$push" : { "devices.$.timestamps": dict(timestamp)}
    }
  )
  return {"message" : "sucessfully added timestamp"}

@timestamp.get("/{room}/device/{device}/timestamp")
def get_timestamps(room: str, device: str):
  result = collection.find_one({"name": room, "devices.name": device},
  {"devices.$":1})['devices'][0]['timestamps']
  
  return timestamp_entities(result)