from fastapi import APIRouter, Request
from sqlalchemy import (
    select,
    update,
    insert,
    delete,
)
from db_utils import engine, Users, validate_user
import hashlib
import pandas as pd
from io import StringIO
import requests
import asyncio
from fastapi.responses import JSONResponse

router = APIRouter()

SALT = "WITHPEPPER"
INTERNAL_API_KEY = "DUMMY_KEY"


@router.post("/admin/add_users")
async def add_user(request: Request):
    params = await request.json()
    token = params.get("token")
    gsheets_url = params.get("gsheets_url")
    if not validate_user(token, user_type="admin"):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"},
        )

    if not gsheets_url:
        return {"error": "no google sheets url provided"}

    # get the users from the google sheet
    user_dets_csv = None
    try:
        url_to_query = gsheets_url.split("/edit")[0] + "/gviz/tq?tqx=out:csv&sheet=v4"
        user_dets_csv = await asyncio.to_thread(requests.get, url_to_query)
        user_dets_csv = user_dets_csv.text
    except:
        return {"error": "could not get the google sheet"}

    # get the users from the csv
    try:
        users = pd.read_csv(StringIO(user_dets_csv)).to_dict(orient="records")
        print(users, flush=True)
    except:
        return {"error": "could not parse the google sheets csv"}

    # create a password for each user
    userdets = []
    for user in users:
        dets = {
            "username": user.get("username", user.get("user_email")).lower(),
            "user_type": user.get("user_type", user.get("user_role")).lower(),
        }
        userdets.append(dets)

    # save the users to postgres
    with engine.begin() as conn:
        for dets in userdets:
            hashed_password = hashlib.sha256(
                (dets["username"] + SALT + "defog_" + dets["username"]).encode()
            ).hexdigest()

            # check if user already exists
            user_exists = conn.execute(
                select(Users).where(Users.username == dets["username"])
            ).fetchone()

            if user_exists:
                conn.execute(
                    update(Users)
                    .where(Users.username == dets["username"])
                    .values(
                        hashed_password=hashed_password, user_type=dets["user_type"]
                    )
                )
            else:
                conn.execute(
                    insert(Users).values(
                        username=dets["username"],
                        hashed_password=hashed_password,
                        token=INTERNAL_API_KEY,
                        user_type=dets["user_type"],
                        is_premium=True,
                    )
                )

    return {"status": "success"}


@router.post("/admin/add_users_csv")
async def add_users_csv(request: Request):
    params = await request.json()
    token = params.get("token")
    users_csv = params.get("users_csv")
    if not validate_user(token, user_type="admin"):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"},
        )

    if not users_csv:
        return {"error": "no users provided"}

    users = pd.read_csv(StringIO(users_csv)).to_dict(orient="records")

    # create a password for each user
    userdets = []
    for user in users:
        dets = {
            "username": user.get("username", user.get("user_email")).lower(),
            "password": user.get("password", user.get("user_password")),
            "user_type": user.get("user_type", user.get("user_role")).lower(),
        }
        userdets.append(dets)

    # save the users to postgres
    # save the users to postgres
    with engine.begin() as conn:
        cur = conn.connection.cursor()
        for dets in userdets:
            hashed_password = hashlib.sha256(
                (dets["username"] + SALT + dets["password"]).encode()
            ).hexdigest()

            # check if user already exists
            user_exists = conn.execute(
                select(Users).where(Users.username == dets["username"])
            ).fetchone()

            if user_exists:
                conn.execute(
                    update(Users)
                    .where(Users.username == dets["username"])
                    .values(
                        hashed_password=hashed_password, user_type=dets["user_type"]
                    )
                )
            else:
                conn.execute(
                    insert(Users).values(
                        username=dets["username"],
                        hashed_password=hashed_password,
                        token=INTERNAL_API_KEY,
                        user_type=dets["user_type"],
                        is_premium=True,
                    )
                )

        return {"status": "success"}


@router.post("/admin/get_users")
async def get_users(request: Request):
    params = await request.json()
    token = params.get("token", None)
    if not validate_user(token, user_type="admin"):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"},
        )

    with engine.begin() as conn:
        users = conn.execute(select(Users)).fetchall()

    users = pd.DataFrame(users)[["username", "user_type"]].to_dict(orient="records")
    return {"users": users}


@router.post("/admin/delete_user")
async def delete_user(request: Request):
    params = await request.json()
    token = params.get("token", None)
    if not validate_user(token, user_type="admin"):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"},
        )

    username = params.get("username", None)
    with engine.begin() as conn:
        conn.execute(delete(Users).where(Users.username == username))
    return {"status": "success"}
