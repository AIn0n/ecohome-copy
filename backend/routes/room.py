from fastapi import APIRouter
from models.room import Room
from config.db import collection
from schemas.room import roomEntity
from pymongo.errors import DuplicateKeyError

room = APIRouter()


@room.get("/room/")
async def find_all_rooms():
    return list(map(roomEntity, collection.find()))


@room.post("/room/")
async def create_room(room: Room):
    if len(room.name) < 1:
        return {"message": "room name is empty"}
    try:
        collection.insert_one(dict(room))
    except DuplicateKeyError:
        return {"message": "room already exists"}
    return {"message": "OK"}


@room.delete("/room/{room_name}")
async def delete_room(room_name: str):
    return {
        "message": "Room deleted successfully"
        if collection.delete_one({"name": room_name}).deleted_count
        else "Room not found"
    }
