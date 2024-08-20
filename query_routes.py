from fastapi import APIRouter, Request
from defog import Defog
from db_utils import validate_user, get_db_type_creds
import pandas as pd
import asyncio
import os
from generic_utils import make_request, get_api_key_from_key_name
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/query")
async def query(request: Request):
    body = await request.json()
    question = body.get("question")
    previous_context = body.get("previous_context")
    dev = body.get("dev", False)
    key_name = body.get("key_name")
    glossary = body.get("glossary", "")
    api_key = get_api_key_from_key_name(key_name)
    res = get_db_type_creds(api_key)

    if res:
        db_type, db_creds = res
    else:
        return {"error": "no db creds found"}
    ignore_cache = body.get("ignore_cache", False)
    token = body.get("token")
    if not validate_user(token):
        return JSONResponse(
            status_code=401,
            content={
                "error": "unauthorized",
                "message": "Invalid username or password",
            },
        )

    print(
        "Base Url: ",
        os.environ.get("DEFOG_BASE_URL", "https://api.defog.ai"),
        flush=True,
    )

    defog = Defog(api_key=api_key, db_type=db_type, db_creds=db_creds)
    defog.base_url = os.environ.get("DEFOG_BASE_URL", "https://api.defog.ai")
    defog.generate_query_url = os.environ.get(
        "DEFOG_GENERATE_URL", f"{defog.base_url}/generate_query_chat"
    )
    print("Generate Query URL: ", defog.generate_query_url, flush=True)
    res = await asyncio.to_thread(
        defog.run_query,
        question,
        previous_context=previous_context,
        dev=dev,
        profile=True,
        ignore_cache=ignore_cache,
        glossary=glossary,
    )

    if "generation_time_taken" in res:
        res["debug_info"] = (
            f"Query Generation Time: {res.get('generation_time_taken', '')}\nQuery Execution Time: {res.get('execution_time_taken', '-')}"
        )
    else:
        res["debug_info"] = (
            f"Query Execution Time: {res.get('execution_time_taken', '-')}"
        )
    # do this to prevent frontend from breaking if a columns is all empty
    if "data" in res and res["data"] is not None:
        res["data"] = pd.DataFrame(res["data"])
        res["data"] = res["data"].fillna("").values.tolist()
    else:
        res["data"] = []
        res["columns"] = []
    return res


@router.post("/get_chart_types")
async def get_chart_types(request: Request):
    print("CALLED GET CHART TYPES", flush=True)
    body = await request.json()
    columns = body.get("columns")
    question = body.get("question")
    key_name = body.get("key_name")
    api_key = get_api_key_from_key_name(key_name)

    res = await make_request(
        "https://api.defog.ai/get_chart_type",
        json={"api_key": api_key, "columns": columns, "question": question},
    )
    return res
