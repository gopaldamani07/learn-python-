# db.py
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import duckdb

router = APIRouter()
app = FastAPI()

con = duckdb.connect("items.duckdb")

con.execute("CREATE SEQUENCE IF NOT EXISTS items_id_seq START 1")
con.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        description VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):     
    name: str
    description: Optional[str] = None

class ItemPatch(BaseModel):         
    name: Optional[str] = None
    description: Optional[str] = None


def row_to_dict(r):
    """Tuples from fetchall() are positional — convert to named fields for JSON."""
    return {"id": r[0], "name": r[1], "description": r[2], "created_at": r[3]}

@router.get("/items/search")
def search_items(created_after: Optional[str] = None,
                 created_before: Optional[str] = None):
    sql = "SELECT id, name, description, created_at FROM items WHERE 1=1"
    params = []
    if created_after:
        sql += " AND created_at >= ?"
        params.append(created_after)
    if created_before:
        sql += " AND created_at <= ?"
        params.append(created_before)
    rows = con.execute(sql, params).fetchall()
    return [row_to_dict(r) for r in rows]


@router.get("/items")
def list_items():
    rows = con.execute(
        "SELECT id, name, description, created_at FROM items"
    ).fetchall()
    return [row_to_dict(r) for r in rows]


@router.get("/items/{item_id}")
def get_item(item_id: int):
    row = con.execute(
        "SELECT id, name, description, created_at FROM items WHERE id = ?",
        [item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row_to_dict(row)


@router.post("/items", status_code=201)
def create_item(item: ItemCreate):
    row = con.execute(
        """INSERT INTO items (id, name, description)
           VALUES (nextval('items_id_seq'), ?, ?)
           RETURNING id, name, description, created_at""",
        [item.name, item.description]
    ).fetchone()
    return row_to_dict(row)


@router.put("/items/{item_id}")
def replace_item(item_id: int, item: ItemUpdate):
    
    row = con.execute(
        """UPDATE items SET name = ?, description = ? WHERE id = ?
           RETURNING id, name, description, created_at""",
        [item.name, item.description, item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row_to_dict(row)


@router.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemPatch):
    
    fields = item.dict(exclude_unset=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields provided")

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    params = list(fields.values()) + [item_id]
    row = con.execute(
        f"""UPDATE items SET {set_clause} WHERE id = ?
            RETURNING id, name, description, created_at""",
        params
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row_to_dict(row)


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    row = con.execute(
        "DELETE FROM items WHERE id = ? RETURNING id", [item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")


app.include_router(router)  