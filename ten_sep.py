from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
import json

from typing import Optional

app = FastAPI()

DB_FILE = "tasks.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [
            {"id": 1, "title": "Buy groceries", "status": "pending", "due_date": "2026-09-15", "created_at": "2026-09-01T10:00:00"},
            {"id": 2, "title": "Finish report", "status": "done", "due_date": "2026-09-10", "created_at": "2026-09-02T09:30:00"},
            {"id": 3, "title": "Call dentist", "status": "pending", "due_date": "2026-09-20", "created_at": "2026-09-05T14:15:00"},
        ]


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=3)


fake_db = load_db()
class TaskCreate(BaseModel):
    title: str
    status: str
    due_date: str

class TaskUpdate(BaseModel):
    title: str
    status: str
    due_date: str
class TaskPatch(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None




@app.get("/tasks/{item_id}")
async def readone(item_id: int):
     for i in fake_db:
          if i["id"] == item_id:
               return i 
     raise HTTPException(status_code=404, detail="id not found")


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    new_task = {
        "id": len(fake_db) + 1,
        "title": task.title,
        "status": task.status,
        "due_date": task.due_date,
        "created_at": datetime.now().isoformat(),
    }
    fake_db.append(new_task)
    save_db(fake_db)
    return new_task


@app.put("/tasks/{item_id}")
async def update_tasks(item_id: int , update:TaskUpdate):
    for i in fake_db:
        if i["id"] == item_id:
            i["title"] = update.title
            i["status"] = update.status
            i["due_date"] = update.due_date
            save_db(fake_db)
            return i
    raise HTTPException(status_code=404, detail="item id not found ")    

@app.patch("/tasks/{item_id}")
async def patch_task(item_id: int, updates: TaskPatch):
    for i in fake_db:
        if i["id"] == item_id:
            if updates.title is not None:
                i["title"] = updates.title
            if updates.status is not None:
                i["status"] = updates.status
            if updates.due_date is not None:
                i["due_date"] = updates.due_date
            save_db(fake_db)
            return i
    raise HTTPException(status_code=404, detail="item id not found")


@app.delete("/tasks/{item_id}")
async def delete_task(item_id: int):
    for i in fake_db:
        if i["id"] == item_id:
            fake_db.remove(i)
            save_db(fake_db)
            return {"message": "task deleted"}
    raise HTTPException(status_code=404, detail="item id not found")

@app.get("/tasks")
async def readitems(
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    title: Optional[str] = None,
):
    results = fake_db
    if created_after is not None:
        results = [t for t in results if t["created_at"] >= created_after]
    if created_before is not None:
        results = [t for t in results if t["created_at"] <= created_before]
    if title is not None:
        results = [t for t in results if title.lower() in t["title"].lower()]
    return results