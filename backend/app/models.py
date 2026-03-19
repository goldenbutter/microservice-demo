from sqlalchemy import Column, Integer, String
from .database import Base

# This is our SQLAlchemy model for our database table
class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)