from enum import Enum
from fastapi import FastAPI


app = FastAPI()


class Car(str, Enum):
    coolcar = "ferrari"
    supercar = "Bugatti"
    xcar = "bmw"


@app.get("/models/{model_name}")
async def get_model(model_name: Car):

    if model_name is Car.coolcar:
        return {
            "model_name": model_name,
            "message": "the red color is ..."
        }

    if model_name is Car.supercar:
        return {
            "model_name": model_name,
            "message": "This is a supercar!"
        }

    if model_name is Car.xcar:
        return {
            "model_name": model_name,
            "message": "BMW car!"
        }

# from enum import Enum
# from fastapi import FastAPI

# app = FastAPI()


# class UserRole(str, Enum):
#     admin = "admin"
#     editor = "editor"
#     viewer = "viewer"


# @app.get("/users/{role}")
# async def get_users(role: UserRole):

#     if role is UserRole.admin:
#         return {"message": "Admin has full access"}

#     elif role is UserRole.editor:
#         return {"message": "Editor can modify content"}

#     else:
#         return {"message": "Viewer can only read"}
        # from enum import Enum

# from fastapi import FastAPI


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# app = FastAPI()


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}



# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}


# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}





# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/items/{items_id}")
# async def read_inside_items(items_id):
#     return {"items_id":items_id}