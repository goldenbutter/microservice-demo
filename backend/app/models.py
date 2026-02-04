# This file contains the data model for our in‑memory storage.
# We keep it very simple to make the project easy to learn.

class ItemModel:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description