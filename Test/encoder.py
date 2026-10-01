from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
import json
import os


app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    course: str
    created_at: datetime


@app.post("/students")
async def create_student(student: Student):

    file_name = "students.json"

  
    student_data = jsonable_encoder(student)

   
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            students = json.load(file)
    else:
        students = []

  
    students.append(student_data)

    
    with open(file_name, "w") as file:
        json.dump(students, file, indent=4)

    return {
        "message": "Student saved successfully",
        "student": student_data
    }


# from datetime import datetime

# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel


# app = FastAPI()

# # Fake database
# fake_db = {}


# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None


# @app.put("/items/{id}")
# def update_item(id: str, item: Item):


#     json_compatible_item_data = jsonable_encoder(item)


#     fake_db[id] = json_compatible_item_data

#     return {
#         "message": "Item saved successfully",
#         "id": id,
#         "data": fake_db[id]
#     }


# @app.get("/items/{id}")
# def get_item(id: str):

#     return fake_db.get(id, {"message": "Item not found"})

    
#     from datetime import datetime

# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel

# fake_db = {}


# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None


# app = FastAPI()


# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data