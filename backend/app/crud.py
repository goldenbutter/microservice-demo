from sqlalchemy.orm import Session
from .models import ItemModel
from .schemas import ItemCreate

# Return all items from the database
def get_all_items(db: Session):
    return db.query(ItemModel).all()

# Create a new item in the database
def create_item(db: Session, item: ItemCreate):
    db_item = ItemModel(
        name=item.name,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Return a single item by ID
def get_item(db: Session, item_id: int):
    return db.query(ItemModel).filter(ItemModel.id == item_id).first()