import logging
from dotenv import load_dotenv
import os

load_dotenv("config.env")

DEFOG_API_KEY = os.environ.get("DEFOG_API_KEY")
if DEFOG_API_KEY is None or DEFOG_API_KEY == "" or DEFOG_API_KEY == "YOUR_API_KEY":
    raise Exception(
        f"Your DEFOG_API_KEY is currently invalid. Please set DEFOG_API_KEY to your valid API key in your config.env file."
    )

import traceback
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import FileResponse
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from connection_manager import ConnectionManager
from agents.planner_executor.execute_tool import execute_tool
from uuid import uuid4
from utils import make_request

from db_utils import (
    get_all_analyses,
    get_analysis_data,
    initialise_analysis,
)
from generic_utils import get_api_key_from_key_name
import integration_routes, query_routes, admin_routes, auth_routes, readiness_routes, csv_routes, feedback_routes, slack_routes, agent_routes, imgo_routes

logging.basicConfig(level=logging.INFO)

manager = ConnectionManager()

app = FastAPI()
app.include_router(integration_routes.router)
app.include_router(query_routes.router)
app.include_router(admin_routes.router)
app.include_router(auth_routes.router)
app.include_router(readiness_routes.router)
app.include_router(csv_routes.router)
app.include_router(feedback_routes.router)
app.include_router(imgo_routes.router)
app.include_router(slack_routes.router)
app.include_router(agent_routes.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

request_types = ["clarify", "understand", "gen_approaches", "gen_steps", "gen_analysis"]
from pathlib import Path

home_dir = Path.home()
analysis_assets_dir = home_dir / "defog_report_assets"
analysis_assets_dir = os.environ.get(
    "REPORT_ASSETS_DIR", analysis_assets_dir.as_posix()
)


llm_calls_url = os.environ.get("LLM_CALLS_URL", "https://api.defog.ai/agent_endpoint")


@app.get("/ping")
async def root():
    return {"message": "Hello World"}


edit_request_types_and_prop_names = {
    "edit_analysis_md": {
        "table_column": "gen_analysis",
        "prop_name": "analysis_sections",
    },
    "edit_approaches": {"table_column": "gen_approaches", "prop_name": "approaches"},
}


async def get_classification(question, api_key, debug=False):
    r = await make_request(
        f"{os.environ.get('DEFOG_BASE_URL', 'https://api.defog.ai')}/update_agent_feedback",
        payload={"question": question, "api_key": api_key},
    )
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error getting question classification: {r.status_code}")
        print(r.text)


@app.post("/get_analyses")
async def all_analyses(request: Request):
    params = await request.json()
    key_name = params.get("key_name")
    api_key = get_api_key_from_key_name(key_name)
    try:
        err, analyses = get_all_analyses(api_key=api_key)
        if err is not None:
            return {"success": False, "error_message": err}

        return {"success": True, "analyses": analyses}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"success": False, "error_message": "Incorrect request"}


@app.post("/get_analysis")
async def one_analysis(request: Request):
    try:
        params = await request.json()
        analysis_id = params.get("analysis_id")

        print("get_one_analysis", params)

        err, analysis_data = get_analysis_data(analysis_id)

        if err is not None:
            return {"success": False, "error_message": err}

        return {"success": True, "analysis_data": analysis_data}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"success": False, "error_message": "Incorrect request"}


@app.post("/create_analysis")
async def create_analysis(request: Request):
    try:
        params = await request.json()
        token = params.get("token")

        key_name = params.get("key_name")
        api_key = get_api_key_from_key_name(key_name)

        print("create_analysis", params)

        err, analysis_data = await initialise_analysis(
            user_question="",
            token=token,
            api_key=api_key,
            custom_id=params.get("custom_id"),
            other_data=params.get("other_data"),
        )

        if err is not None:
            return {"success": False, "error_message": err}

        return {"success": True, "analysis_data": analysis_data}
    except Exception as e:
        print(e)
        return {"success": False, "error_message": "Incorrect request"}


@app.get("/get_assets")
async def get_assets(path: str):
    try:
        return FileResponse(os.path.join(analysis_assets_dir, path))
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"success": False, "error_message": "Error getting assets"}


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
