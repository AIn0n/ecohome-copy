from fastapi import APIRouter
from config.db import conn

payments = APIRouter()

@payments.post('/payments/')
def set_prices(before_limit: float, after_limit: float):
  conn["database"]["payments"].update_one({}, {"$set" :{
    "before_limit": before_limit,
    "after_limit": after_limit
  }})

@payments.get('/payments/')
def get_prices():
  item = conn["database"]["payments"].find_one()
  return {
    "before_limit": item["before_limit"],
    "after_limit": item["after_limit"]
  }