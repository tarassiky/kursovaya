from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Water Delivery System")

orders_db: Dict[int, dict] = {}
counter = 1

class OrderCreate(BaseModel):
    customer_name: str
    address: str
    bottles: int

class Order(OrderCreate):
    id: int
    status: str = "pending"

@app.get("/")
def root():
    return {"message": "Water Delivery API is running"}   # исправлено

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    global counter
    new_id = counter
    counter += 1
    orders_db[new_id] = order.model_dump()   # исправлено: .model_dump()
    orders_db[new_id]["status"] = "pending"
    return Order(id=new_id, **orders_db[new_id])

@app.get("/orders", response_model=List[Order])
def list_orders():
    return [Order(id=id, **data) for id, data in orders_db.items()]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(id=order_id, **orders_db[order_id])