# ---------------------------------------------------------
# main.py — FastAPI entry point for the Microservice Demo
# ---------------------------------------------------------
# This file:
# - Creates the FastAPI application
# - Enables CORS (so frontend can talk to backend)
# - Defines all API routes (endpoints)
# - Connects routes to CRUD logic and Pydantic schemas
# ---------------------------------------------------------

from fastapi import FastAPI
from typing import List

# Import Pydantic models for validating input/output
from .schemas import Item, ItemCreate

# Import CRUD operations (business logic)
from . import crud

# Import CORS middleware so the browser can access the API
from fastapi.middleware.cors import CORSMiddleware


# ---------------------------------------------------------
# Create the FastAPI app instance
# ---------------------------------------------------------
app = FastAPI(
    title="Microservice Demo API",
    description="A simple FastAPI backend for learning Docker & Kubernetes.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Enable CORS so frontend (port 5500) can call backend (port 8000)
# ---------------------------------------------------------
# Without this, the browser blocks your fetch() calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (OK for learning)
    allow_credentials=True,
    allow_methods=["*"],      # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],      # Allow all request headers
)


# ---------------------------------------------------------
# Root endpoint — simple welcome message
# ---------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the Microservice Demo API!"}


# ---------------------------------------------------------
# GET /items — returns all items
# ---------------------------------------------------------
@app.get("/items", response_model=List[Item])
def get_items():
    return crud.get_all_items()   # Calls logic from crud.py


# ---------------------------------------------------------
# POST /items — create a new item
# ---------------------------------------------------------
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    return crud.create_item(item)


# ---------------------------------------------------------
# GET /items/{item_id} — return a single item
# ---------------------------------------------------------
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    return crud.get_item(item_id)