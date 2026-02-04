from pydantic import BaseModel

# Model for creating a new item (client input)
class ItemCreate(BaseModel):
    name: str
    description: str

# Model for returning an item (server output)
class Item(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True