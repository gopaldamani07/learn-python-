import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import duckdb
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, model_validator



SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

con = duckdb.connect(":memory:")

con.execute("CREATE SEQUENCE IF NOT EXISTS users_id_seq START 1")
con.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR UNIQUE NOT NULL,
        hashed_password VARCHAR NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

con.execute("CREATE SEQUENCE IF NOT EXISTS teams_id_seq START 1")
con.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        description VARCHAR,
        owner VARCHAR NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_scheme = HTTPBearer()

app = FastAPI(title="Auth + Teams API")


class SignupRequest(BaseModel):
    username: str

    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class LoginRequest(BaseModel):
    username: str
    password: str


class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None


TEAM_COLUMNS = "id, name, description, owner, created_at"


def user_to_dict(r):
    return {"id": r[0], "username": r[1], "created_at": r[2]}


def team_to_dict(r):
    return {"id": r[0], "name": r[1], "description": r[2], "owner": r[3], "created_at": r[4]}


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """Reads the bearer token and returns the logged-in username."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_error
    username = payload.get("sub")
    if username is None:
        raise credentials_error

    row = con.cursor().execute(
        "SELECT 1 FROM users WHERE username = ?", [username]
    ).fetchone()
    if row is None:
        raise credentials_error
    return username


def get_own_team(cur, team_id: int, username: str):
    """404 if the team doesn't exist, 403 if it belongs to someone else."""
    row = cur.execute(
        f"SELECT {TEAM_COLUMNS} FROM teams WHERE id = ?", [team_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if row[3] != username:
        raise HTTPException(status_code=403, detail="You can only change your own teams")
    return row


@app.post("/signup", status_code=201)
def signup(user: SignupRequest):
    # one cursor per request: a DuckDB connection isn't safe to share across threads
    cur = con.cursor()
    try:
        row = cur.execute(
            """INSERT INTO users (id, username, hashed_password)
               VALUES (nextval('users_id_seq'), ?, ?)
               RETURNING id, username, created_at""",
            [user.username, pwd_context.hash(user.password)]
        ).fetchone()
    except duckdb.ConstraintException:
        raise HTTPException(status_code=409, detail="Username already taken")
    return user_to_dict(row)


@app.post("/login")
def login(user: LoginRequest):
    row = con.cursor().execute(
        "SELECT hashed_password FROM users WHERE username = ?", [user.username]
    ).fetchone()
    if row is None or not pwd_context.verify(user.password, row[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"bearer_token": create_access_token(user.username)}


@app.post("/teams", status_code=201)
def create_team(team: TeamCreate, username: str = Depends(get_current_user)):
    row = con.cursor().execute(
        f"""INSERT INTO teams (id, name, description, owner)
            VALUES (nextval('teams_id_seq'), ?, ?, ?)
            RETURNING {TEAM_COLUMNS}""",
        [team.name, team.description, username]
    ).fetchone()
    return team_to_dict(row)



@app.get("/teams", dependencies=[Depends(get_current_user)])
def list_teams():
    rows = con.cursor().execute(
        f"SELECT {TEAM_COLUMNS} FROM teams ORDER BY id"
    ).fetchall()
    return [team_to_dict(r) for r in rows]



@app.get("/teams/search", dependencies=[Depends(get_current_user)])
def search_teams(name: str):
    rows = con.cursor().execute(
        f"SELECT {TEAM_COLUMNS} FROM teams WHERE name ILIKE '%' || ? || '%' ORDER BY id",
        [name]
    ).fetchall()
    return [team_to_dict(r) for r in rows]


@app.get("/teams/{team_id}", dependencies=[Depends(get_current_user)])
def get_team(team_id: int):
    row = con.cursor().execute(
        f"SELECT {TEAM_COLUMNS} FROM teams WHERE id = ?", [team_id]
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_to_dict(row)


@app.put("/teams/{team_id}")
def update_team(team_id: int, team: TeamCreate, username: str = Depends(get_current_user)):
    cur = con.cursor()
    get_own_team(cur, team_id, username)
    row = cur.execute(
        f"""UPDATE teams SET name = ?, description = ? WHERE id = ?
            RETURNING {TEAM_COLUMNS}""",
        [team.name, team.description, team_id]
    ).fetchone()
    return team_to_dict(row)


@app.delete("/teams/{team_id}", status_code=204)
def delete_team(team_id: int, username: str = Depends(get_current_user)):
    cur = con.cursor()
    get_own_team(cur, team_id, username)
    cur.execute("DELETE FROM teams WHERE id = ?", [team_id])
