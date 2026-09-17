from fastapi import FastAPI
from pydantic import BaseModel
import json
import os


app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    course: str
    data :str 
    somthingmore: str
    



@app.post("/students")
async def create_student(student: Student):

    file_name = "students.json"

   
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            students = json.load(file)
    else:
        students = []

    
    student_data = student.model_dump()

    students.append(student_data)

   # save the data in student.json file 
    with open(file_name, "w") as file:
        json.dump(students, file, indent=4)

    return {
        "message": "Student created successfully",
        "student": student_data
    }