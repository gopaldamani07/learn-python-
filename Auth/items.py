from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_admin
from database import con, row_to_dict
from models import ItemCreate, ItemUpdate, ItemPatch, User

router = APIRouter()

@router.get("/items/search")
def search_items(created_after: Optional[str] = None,
                 created_before: Optional[str] = None,
                 current_user: User = Depends(get_current_user)):
    sql = "SELECT id, name, description, created_at FROM items WHERE 1=1"
    params = []
    if created_after:
        sql += " AND created_at >= ?"
        params.append(created_after)
    if created_before:
        sql += " AND created_at <= ?"
        params.append(created_before)
    return [row_to_dict(r) for r in con.execute(sql, params).fetchall()]


@router.get("/items")
def list_items(current_user: User = Depends(get_current_user)):
    rows = con.execute(
        "SELECT id, name, description, created_at FROM items ORDER BY id"
    ).fetchall()
    return [row_to_dict(r) for r in rows]


@router.get("/items/{item_id}")
def get_item(item_id: int, current_user: User = Depends(get_current_user)):
    row = con.execute(
        "SELECT id, name, description, created_at FROM items WHERE id = ?",
        [item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row_to_dict(row)


@router.post("/items", status_code=201)
def create_item(item: ItemCreate, current_user: User = Depends(get_current_user)):
    row = con.execute(
        """INSERT INTO items (id, name, description)
           VALUES (nextval('items_id_seq'), ?, ?)
           RETURNING id, name, description, created_at""",
        [item.name, item.description]
    ).fetchone()
    return row_to_dict(row)


@router.put("/items/{item_id}")
def replace_item(item_id: int, item: ItemUpdate,
                 current_user: User = Depends(get_current_user)):
    row = con.execute(
        """UPDATE items SET name = ?, description = ? WHERE id = ?
           RETURNING id, name, description, created_at""",
        [item.name, item.description, item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return row_to_dict(row)


@router.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemPatch,
               current_user: User = Depends(get_current_user)):
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
def delete_item(item_id: int, current_user: User = Depends(require_admin)):
    row = con.execute(
        "DELETE FROM items WHERE id = ? RETURNING id", [item_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")