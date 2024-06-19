from fastapi import APIRouter, Request, HTTPException
from auth_utils import login_user


router = APIRouter()


@router.post("/login")
async def login(request: Request):
    params = await request.json()
    username = params.get("username", None)
    password = params.get("password", None)
    if not username:
        return {"error": "no user id provided"}
    if not password:
        return {"error": "no password provided"}

    dets = await login_user(username, password)
    return dets
