from .models import ItemModel
from .database import ITEMS, CURRENT_ID
from .schemas import ItemCreate

# Return all items
def get_all_items():
    return ITEMS

# Create a new item
def create_item(item: ItemCreate):
    global CURRENT_ID

    # Simulate auto-increment ID
    CURRENT_ID += 1

    new_item = ItemModel(
        id=CURRENT_ID,
        name=item.name,
        description=item.description
    )

    ITEMS.append(new_item)
    return new_item

# Return a single item by ID
def get_item(item_id: int):
    for item in ITEMS:
        if item.id == item_id:
            return item
    return None   # FastAPI will convert this to a 404 for us