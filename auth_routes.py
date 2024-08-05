from fastapi import APIRouter, Request
from auth_utils import login_user, reset_password
from db_utils import validate_user
from fastapi.responses import JSONResponse

INTERNAL_API_KEY = "DUMMY_KEY"

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

    dets = login_user(username, password)
    return dets


@router.post("/reset_password")
async def reset_password(request: Request):
    params = await request.json()
    username = params.get("username", None)
    new_password = params.get("password", None)
    token = params.get("token", None)
    if not validate_user(token, user_type="admin"):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"},
        )
    if not username:
        return {"error": "no user id provided"}
    if not new_password:
        return {"error": "no password provided"}
    dets = reset_password(username, new_password)
    return dets
