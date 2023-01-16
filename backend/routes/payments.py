from fastapi import APIRouter
from config.db import conn
from pydantic import BaseModel

payments = APIRouter()

class Payment(BaseModel):
  before_limit: float
  after_limit: float

@payments.post('/payments/')
def set_prices(payment: Payment):
  conn["database"]["payments"].update_one({}, {"$set" :{
    "before_limit": payment.before_limit,
    "after_limit": payment.after_limit
  }})

@payments.get('/payments/')
def get_prices():
  item = conn["database"]["payments"].find_one()
  return {
    "before_limit": item["before_limit"],
    "after_limit": item["after_limit"]
  }