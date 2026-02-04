from fastapi import FastAPI
from typing import List
from .schemas import Item, ItemCreate
from . import crud

app = FastAPI(
    title="Microservice Demo API",
    description="A simple FastAPI backend for practicing Docker & Kubernetes.",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Microservice Demo API!"}

# Get all items
@app.get("/items", response_model=List[Item])
def get_items():
    return crud.get_all_items()

# Create a new item
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    return crud.create_item(item)

# Get item by ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    return crud.get_item(item_id)