from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI()


fake_db = {
    "item1": {
        "title": "Old Python Course",
        "description": "Old description"
    }
}


class Item(BaseModel):
    title: str
    description: str | None = None


@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):

    if item_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item_data = jsonable_encoder(item)

    fake_db[item_id] = item_data

    return {
        "message": "Item updated successfully",
        "item": fake_db[item_id]
    }


@app.get("/items/{item_id}")
def get_item(item_id: str):

    if item_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return fake_db[item_id]



# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel

# app = FastAPI()


# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }


# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]


# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded