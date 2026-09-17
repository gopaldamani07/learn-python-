from fastapi import FastAPI, Response, Cookie
from typing import Annotated


app = FastAPI()


@app.post("/login")
async def login(response: Response):

    username = "gopal"

    response.set_cookie(
        key="username",
        value=username
    )

    return {
        "message": "Login successful",
        "username": username
    }


@app.get("/profile")
async def get_profile(
    username: Annotated[str | None, Cookie()] = None
):

    if username is None:
        return {
            "message": "You are not logged in"
        }

    return {
        "message": "Welcome",
        "username": username
    }
# from typing import Annotated

# from fastapi import Cookie, FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Cookies(BaseModel):
#     session_id: str
#     fatebook_tracker: str | None = None
#     googall_tracker: str | None = None


# @app.get("/items/")
# async def read_items(cookies: Annotated[Cookies, Cookie()]):
#     return cookies

# from typing import Annotated

# from fastapi import Cookie, FastAPI

# app = FastAPI()


# @app.get("/items/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads_id}


# from typing import Annotated

# from fastapi import Cookie, FastAPI

# app = FastAPI()


# @app.get("/items/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads_id}
