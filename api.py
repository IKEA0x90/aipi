from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class SingleMessage:
    

# Sample in-memory database
items_db = []

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    items_db.append(item)
    return item