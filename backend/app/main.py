from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import models, database, and schemas
from . import models, crud, schemas
from .database import SessionLocal, engine

# Import CORS middleware so the browser can access the API
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables on startup
# This handles the schema creation for us automatically
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI(
    title="Microservice Demo API (SQLite)",
    description="FastAPI backend with SQLite persistence for Docker & Kubernetes.",
    version="2.0.0"
)

# Enable CORS (allowing all for simplicity in this demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Persistent Microservice Demo API!"}

# GET /items — returns all items
@app.get("/items", response_model=List[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return crud.get_all_items(db)

# POST /items — create a new item
@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

# GET /items/{item_id} — return a single item
@app.get("/items/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item