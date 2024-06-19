from fastapi import APIRouter, Request
import json
import os
from defog import Defog

from db_utils import validate_user, get_api_key
import asyncio
from generic_utils import make_request, convert_nested_dict_to_list

DEFOG_BASE_URL = os.environ.get("DEFOG_BASE_URL", "https://api.defog.ai")

home_dir = os.path.expanduser("~")
defog_path = os.path.join(home_dir, ".defog")

router = APIRouter()


@router.post("/integration/get_tables_db_creds")
async def get_tables_db_creds(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    try:
        defog = Defog()
        defog.base_url = DEFOG_BASE_URL
    except:
        return {"error": "no defog instance found"}

    try:
        table_names = await asyncio.to_thread(
            defog.generate_db_schema,
            tables=[],
            upload=False,
            scan=False,
            return_tables_only=True,
        )
        print(table_names, flush=True)
    except Exception as e:
        print(e, flush=True)
        table_names = []

    try:
        with open(os.path.join(defog_path, "selected_tables.json"), "r") as f:
            selected_table_names = json.load(f)
    except:
        selected_table_names = table_names

    # only keep selected table names that are in table_names
    selected_table_names = [t for t in selected_table_names if t in table_names]

    db_type = defog.db_type
    db_creds = defog.db_creds

    return {
        "tables": table_names,
        "db_creds": db_creds,
        "db_type": db_type,
        "selected_tables": selected_table_names,
    }


@router.post("/integration/get_metadata")
async def get_metadata(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}
    try:
        md = await make_request(
            f"{DEFOG_BASE_URL}/get_metadata", {"api_key": get_api_key()}
        )
        table_metadata = md["table_metadata"]

        metadata = convert_nested_dict_to_list(table_metadata)
        return {"metadata": metadata}
    except:
        return {"error": "no metadata found"}


@router.post("/integration/update_db_creds")
async def update_db_creds(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}
    db_type = params.get("db_type")
    db_creds = params.get("db_creds")
    for k in ["api_key", "db_type"]:
        if k in db_creds:
            del db_creds[k]

    if db_type == "bigquery":
        db_creds["json_key_path"] = "/backend/bq.json"

    defog = Defog(get_api_key(), db_type, db_creds)

    return {"success": True}


@router.post("/integration/generate_metadata")
async def generate_metadata(request: Request):
    params = await request.json()

    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    tables = params.get("tables")
    dev = params.get("dev", False)

    with open(os.path.join(defog_path, "selected_tables.json"), "w") as f:
        json.dump(tables, f)

    defog = Defog()
    defog.base_url = DEFOG_BASE_URL
    table_metadata = await asyncio.to_thread(
        defog.generate_db_schema, tables=tables, upload=False, scan=False
    )

    md = await make_request(
        f"{DEFOG_BASE_URL}/get_metadata", {"api_key": get_api_key(), "dev": dev}
    )
    try:
        existing_metadata = md["table_metadata"]
    except:
        print("No existing metadata found", flush=True)
        existing_metadata = {}

    for table_name in table_metadata:
        for idx, item in enumerate(table_metadata[table_name]):
            if table_name in existing_metadata:
                print(f"Found table {table_name} in existing metadata", flush=True)
                for existing_item in existing_metadata[table_name]:
                    if existing_item["column_name"] == item["column_name"]:
                        print(
                            f"Found column {item['column_name']} in existing metadata",
                            flush=True,
                        )
                        table_metadata[table_name][idx]["column_description"] = (
                            existing_item["column_description"]
                        )

    metadata = convert_nested_dict_to_list(table_metadata)
    return {"metadata": metadata}


@router.post("/integration/update_metadata")
async def update_metadata(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    metadata = params.get("metadata")
    dev = params.get("dev", False)

    # convert metadata to nested dictionary
    table_metadata = {}
    for item in metadata:
        table_name = item["table_name"]
        if table_name not in table_metadata:
            table_metadata[table_name] = []
        table_metadata[table_name].append(
            {
                "column_name": item["column_name"],
                "data_type": item["data_type"],
                "column_description": item["column_description"],
            }
        )

    defog = Defog()
    defog.base_url = DEFOG_BASE_URL

    # update on API server
    r = await make_request(
        defog.base_url + "/update_metadata",
        json={
            "api_key": defog.api_key,
            "table_metadata": table_metadata,
            "db_type": defog.db_type,
            "dev": dev,
        },
    )

    return r


@router.post("/integration/copy_prod_to_dev")
async def copy_prod_to_dev(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    r = await make_request(
        DEFOG_BASE_URL + "/copy_prod_to_dev", json={"api_key": get_api_key()}
    )

    return r


@router.post("/integration/copy_dev_to_prod")
async def copy_prod_to_dev(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    r = await make_request(
        DEFOG_BASE_URL + "/copy_dev_to_prod", json={"api_key": get_api_key()}
    )

    return r


@router.post("/integration/get_glossary_golden_queries")
async def get_glossary_golden_queries(request: Request):
    params = await request.json()
    token = params.get("token")
    dev = params.get("dev", False)
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    defog = Defog()
    defog.base_url = DEFOG_BASE_URL

    # get glossary
    glossary = await asyncio.to_thread(defog.get_glossary, dev=dev)

    # get golden queries
    golden_queries = await asyncio.to_thread(defog.get_golden_queries, dev=dev)
    return {"glossary": glossary, "golden_queries": golden_queries}


@router.post("/integration/update_glossary")
async def update_glossary(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    glossary = params.get("glossary")
    dev = params.get("dev", False)

    defog = Defog()
    defog.base_url = DEFOG_BASE_URL

    # update glossary
    r = await asyncio.to_thread(defog.update_glossary, glossary, dev=dev)
    return r


@router.post("/integration/update_golden_queries")
async def update_golden_queries(request: Request):
    params = await request.json()
    token = params.get("token")
    if not validate_user(token, user_type="admin"):
        return {"error": "unauthorized"}

    golden_queries = params.get("golden_queries")
    dev = params.get("dev", False)

    defog = Defog()
    defog.base_url = DEFOG_BASE_URL

    # first, delete the existing golden queries
    r = await asyncio.to_thread(
        defog.delete_golden_queries,
        all=True,
        dev=dev,
    )

    # update golden queries
    r = await asyncio.to_thread(
        defog.update_golden_queries, golden_queries, dev=dev, scrub=False
    )
    return r
