from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from pydantic import BaseModel
from typing import List

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemSchema(BaseModel):
    id: int = None
    name: str
    description: str
    price: float
    in_stock: bool

    class Config:
        orm_mode = True

@app.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemSchema])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.get("/items/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only the fields that should be updated (exclude id)
    update_data = item.dict(exclude={'id'})
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}