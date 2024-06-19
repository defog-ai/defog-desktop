from db_utils import engine, Users
from sqlalchemy import (
    select,
    update,
    insert
)
import asyncio
from generic_utils import make_request

async def login_user(username, password):
    # sent a request to the server to check if the user exists
    # if the user exists, then add their username, api_key, hashed_password to the database
    # that's it!
    r = await make_request("https://api.defog.ai/login", json={"username": username, "password": password})
    if r["status"] == "success":
        hashed_password = r["hashed_password"]
        with engine.begin() as conn:
            # check if user exists
            user = conn.execute(select(Users).where(Users.username == username)).fetchone()
            if not user:
                conn.execute(
                    insert(Users).values(username=username, hashed_password=hashed_password, user_type="admin")
                )
            else:
                conn.execute(
                    update(Users)
                    .where(Users.username == username)
                    .values(hashed_password=hashed_password, user_type="admin")
                )
    else:
        return {"status": "error", "error": "Invalid username or password"}
    
    # now make a request to the server to get the api key
    r = await make_request("https://api.defog.ai/get_token", json={"username": username}, headers={"x-hashed-password": hashed_password})
    api_key = r["token"]
    with engine.begin() as conn:
        conn.execute(
            update(Users)
            .where(Users.username == username)
            .values(token=api_key)
        )
    return {"status": "success", "token": hashed_password, "user_type": "admin"}


def validate_user_email(email):
    with engine.begin() as conn:
        user = conn.execute(select(Users).where(Users.username == email)).fetchone()
    if user:
        return True
    else:
        return False
