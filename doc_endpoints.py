import datetime
import os
from uuid import uuid4
import traceback

from fastapi.responses import JSONResponse
import requests
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from agents.planner_executor.tool_helpers.rerun_step import rerun_step_and_dependents
from agents.planner_executor.tool_helpers.core_functions import analyse_data
from agents.planner_executor.tool_helpers.all_tools import tool_name_dict
import pandas as pd
from io import StringIO
from utils import execute_code, get_clean_plan, get_db_type, log_msg, snake_case
import logging
from db_utils import get_api_key
logging.basicConfig(level=logging.INFO)

from connection_manager import ConnectionManager
from db_utils import (
    add_to_recently_viewed_docs,
    add_tool,
    delete_tool,
    get_all_docs,
    get_analysis_versions,
    get_doc_data,
    get_report_data,
    get_tool_run,
    get_toolboxes,
    initialise_report,
    store_feedback,
    store_tool_run,
    toggle_disable_tool,
    update_doc_data,
    update_report_data,
    update_table_chart_data,
    get_table_data,
    get_all_analyses,
    update_tool_run_data,
    delete_doc,
    get_all_tools,
)

router = APIRouter()

manager = ConnectionManager()

llm_calls_url = os.environ.get("LLM_CALLS_URL", "https://api.defog.ai/agent_endpoint")

from pathlib import Path
home_dir = Path.home()
# see if we have a custom report assets directory
if not os.path.exists(home_dir / "defog_report_assets"):
    # create one
    os.mkdir(home_dir / "defog_report_assets")

report_assets_dir = home_dir / "defog_report_assets"
report_assets_dir = os.environ.get("REPORT_ASSETS_DIR", report_assets_dir.as_posix())


@router.websocket("/docs")
async def doc_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "ping" in data:
                # don't do anything
                continue
            if data.get("doc_uint8") is None:
                logging.info("No document data provided.")
                logging.info(data)
                # send error back
                await manager.send_personal_message(
                    {"success": False, "error_message": "No document data provided."},
                    websocket,
                )
                continue

            if data.get("doc_id") is None:
                await manager.send_personal_message(
                    {"success": False, "error_message": "No document id provided."},
                    websocket,
                )
                logging.info("Doc id is none ")
                logging.info(data)

                continue

            col_name = "doc_blocks" if data.get("doc_blocks") else "doc_uint8"
            err = await update_doc_data(
                data.get("doc_id"),
                [col_name, "doc_title"],
                {col_name: data.get(col_name), "doc_title": data.get("doc_title")},
            )

            logging.info(data.get("api_key"))
            logging.info(data.get("token"))
            logging.info(data.get("doc_id"))

            await manager.send_personal_message(data, websocket)
    except WebSocketDisconnect as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        manager.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        # other reasons for disconnect, like websocket being closed or a timeout
        manager.disconnect(websocket)
        await websocket.close()


@router.post("/add_to_recently_viewed_docs")
async def add_to_recently_viewed_docs_endpoint(request: Request):
    """
    Add a document to the recently viewed docs of a user.
    """
    try:
        data = await request.json()
        token = data.get("token")
        doc_id = data.get("doc_id")

        if token is None or type(token) != str:
            return {"success": False, "error_message": "Invalid token."}

        if doc_id is None or type(doc_id) != str:
            return {"success": False, "error_message": "Invalid document id."}

        await add_to_recently_viewed_docs(
            token=token,
            doc_id=doc_id,
            timestamp=str(datetime.datetime.now()),
        )

        return {"success": True}
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.post("/toggle_archive_status")
async def toggle_archive_status(request: Request):
    """
    Toggle the archive status of a document.
    """
    data = await request.json()
    doc_id = data.get("doc_id")
    archive_status = data.get("archive_status")

    err = await update_doc_data(doc_id, ["archived"], {"archived": archive_status})

    if err:
        return {"success": False, "error_message": err}

    return {"success": True}


@router.post("/get_doc")
async def get_document(request: Request):
    """
    Get the document using the id passed.
    If it doesn't exist, create one and return empty data.
    """
    data = await request.json()
    doc_id = data.get("doc_id")
    token = data.get("token")
    col_name = data.get("col_name") or "doc_blocks"

    if doc_id is None or type(doc_id) != str:
        return {"success": False, "error_message": "Invalid document id."}

    err, doc_data = await get_doc_data(doc_id, token, col_name)

    if err:
        return {"success": False, "error_message": err}

    return {"success": True, "doc_data": doc_data}


@router.post("/get_toolboxes")
async def get_toolboxes_endpoint(request: Request):
    """
    Get all toolboxes using the username.
    """
    try:
        data = await request.json()
        token = data.get("token")

        if token is None or type(token) != str:
            return {"success": False, "error_message": "Invalid token."}

        err, toolboxes = await get_toolboxes(token)
        if err:
            return {"success": False, "error_message": err}

        return {"success": True, "toolboxes": toolboxes}
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.post("/get_docs")
async def get_docs(request: Request):
    """
    Get all documents of a user using the api key.
    """
    try:
        data = await request.json()
        token = data.get("token")

        if token is None or type(token) != str:
            return {"success": False, "error_message": "Invalid token."}

        err, own_docs, recently_viewed_docs = await get_all_docs(token)
        if err:
            return {"success": False, "error_message": err}

        return {
            "success": True,
            "docs": own_docs,
            "recently_viewed_docs": recently_viewed_docs,
        }
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.post("/get_analyses")
async def get_analyses(request: Request):
    """
    Get all analysis of a user using the api key.
    """
    try:
        err, analyses = await get_all_analyses()
        if err:
            return {"success": False, "error_message": err}

        return {"success": True, "analyses": analyses}
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.websocket("/table_chart")
async def update_table_chart(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "ping" in data:
                # don't do anything
                continue

            if data.get("table_id") is None:
                logging.info("No table id ")
                continue

            if data.get("data") is None:
                logging.info("No data given for table update")
                continue

            err, analysis, updated_data = await update_table_chart_data(
                data.get("table_id"), data.get("data")
            )

            if err is None:
                # run this table again
                logging.info("Ran fine.")
                await manager.send_personal_message(
                    {"success": True, "run_again": True, "table_data": updated_data},
                    websocket,
                )
            elif err is not None:
                logging.info("Error re running:" + str(err))
                await manager.send_personal_message(
                    {"success": False, "run_again": True, "error_message": str(err)},
                    websocket,
                )

    except WebSocketDisconnect as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        manager.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # traceback.print_exc()
        # other reasons for disconnect, like websocket being closed or a timeout
        manager.disconnect(websocket)
        await websocket.close()


@router.post("/get_table_chart")
async def get_table_chart(request: Request):
    """
    Get the table_chart using the id passed.
    """
    try:
        data = await request.json()
        table_id = data.get("table_id")

        if table_id is None or type(table_id) != str:
            return {"success": False, "error_message": "Invalid document id."}

        err, table_data = await get_table_data(table_id)

        if err:
            return {"success": False, "error_message": err}

        return {"success": True, "table_data": table_data}
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.post("/get_tool_run")
async def get_tool_run_endpoint(request: Request):
    """
    Get the tool run using the id passed.
    """
    try:
        data = await request.json()
        tool_run_id = data.get("tool_run_id")
        logging.info("getting tool run: " + tool_run_id)

        if tool_run_id is None or type(tool_run_id) != str:
            return {"success": False, "error_message": "Invalid tool run id."}

        err, tool_run = await get_tool_run(tool_run_id)

        if err:
            return {"success": False, "error_message": err}

        return {"success": True, "tool_run_data": tool_run}
    except Exception as e:
        logging.info("Error getting analyses: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": "Unable to parse your request."}


@router.websocket("/edit_tool_run")
async def edit_tool_run(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

            if "ping" in data:
                # don't do anything
                continue

            if data.get("tool_run_id") is None:
                logging.info("No tool run id ")
                continue

            if data.get("analysis_id") is None:
                logging.info("No analysis id ")
                continue

            update_res = await update_tool_run_data(
                data.get("analysis_id"),
                data.get("tool_run_id"),
                data.get("update_prop"),
                data.get("new_val"),
            )
            if not update_res["success"]:
                logging.info(
                    f"Error updating tool run: {update_res['error_message']}"
                )

    except WebSocketDisconnect as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        manager.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        # other reasons for disconnect, like websocket being closed or a timeout
        manager.disconnect(websocket)
        try:
            await websocket.close()
        except:
            pass


@router.websocket("/step_rerun")
async def rerun_step(websocket: WebSocket):
    """
    Re run a step (and associated steps) in the analysis.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "ping" in data:
                # don't do anything
                continue

            tool_run_id = data.get("tool_run_id")
            analysis_id = data.get("analysis_id")
            dev = data.get("dev", False)

            if tool_run_id is None or type(tool_run_id) != str:
                return {"success": False, "error_message": "Invalid tool run id."}

            if analysis_id is None or type(analysis_id) != str:
                return {"success": False, "error_message": "Invalid analysis id."}

            # get steps from db
            err, analysis_data = get_report_data(analysis_id)
            if err:
                return {
                    "success": False,
                    "error_message": err,
                    "tool_run_id": tool_run_id,
                    "analysis_id": analysis_id,
                }

            global_dict = {
                "user_question": analysis_data["user_question"],
                "llm_calls_url": llm_calls_url,
                "report_assets_dir": report_assets_dir,
                "dev": dev,
            }

            if err:
                return {
                    "success": False,
                    "error_message": err,
                    "tool_run_id": tool_run_id,
                    "analysis_id": analysis_id,
                }

            steps = analysis_data["gen_steps"]
            if steps["success"]:
                steps = steps["steps"]
            else:
                return {
                    "success": False,
                    "error_message": steps["error_message"],
                    "tool_run_id": tool_run_id,
                    "analysis_id": analysis_id,
                }

            logging.info([s["inputs"] for s in steps])
            async for err, reran_id, new_data in rerun_step_and_dependents(
                analysis_id, tool_run_id, steps, global_dict=global_dict
            ):
                if new_data and type(new_data) == dict:
                    if reran_id:
                        logging.info("Reran step: " + reran_id)
                        await manager.send_personal_message(
                            {
                                "success": True,
                                "tool_run_id": reran_id,
                                "analysis_id": analysis_id,
                                "tool_run_data": new_data,
                            },
                            websocket,
                        )
                    elif new_data.get("pre_tool_run_message"):
                        logging.info(
                            f"Starting rerunning of step: {new_data.get('pre_tool_run_message')} with websocket: {websocket} in application_state: {websocket.application_state} and client_state: {websocket.client_state}"
                        )
                        await manager.send_personal_message(
                            {
                                "pre_tool_run_message": new_data.get(
                                    "pre_tool_run_message"
                                ),
                                "analysis_id": analysis_id,
                            },
                            websocket,
                        )
                else:
                    logging.info("Error: " + str(err))
                    await manager.send_personal_message(
                        {
                            "success": False,
                            "error_message": err,
                            "tool_run_id": reran_id,
                            "analysis_id": analysis_id,
                        },
                        websocket,
                    )

    except WebSocketDisconnect as e:
        logging.info("Disconnected. Error: " + str(e))
        # # traceback.print_exc()
        manager.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        # other reasons for disconnect, like websocket being closed or a timeout
        manager.disconnect(websocket)
        try:
            await websocket.close()
        except Exception as e:
            pass


# setup an analyse_data websocket endpoint
@router.websocket("/analyse_data")
async def analyse_data_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "ping" in data:
                # don't do anything
                continue
            if data.get("question") is None:
                await manager.send_personal_message(
                    {"success": False, "error_message": "No question"}, websocket
                )
                continue

            if data.get("data") is None:
                await manager.send_personal_message(
                    {"success": False, "error_message": "No data"}, websocket
                )
                continue

            # read data from the csv
            df = pd.read_csv(StringIO(data.get("data")))
            image_path = data.get("image")

            async for chunk in analyse_data(
                data.get("question"), df, image_path=image_path
            ):
                await manager.send_personal_message(chunk, websocket)

    except WebSocketDisconnect as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # # traceback.print_exc()
        manager.disconnect(websocket)
        await websocket.close()
    except Exception as e:
        # logging.info("Disconnected. Error: " +  str(e))
        # traceback.print_exc()
        await manager.send_personal_message(
            {"success": False, "error_message": str(e)[:300]}, websocket
        )
        # other reasons for disconnect, like websocket being closed or a timeout
        manager.disconnect(websocket)
        await websocket.close()


@router.post("/create_new_step")
async def create_new_step(request: Request):
    """
    This is called when a user adds a step on the front end.
    This will receive a tool name, and tool inputs.
    This will create a new step in the analysis.
    No tool run will occur. Though a tool run id will be created for this step in case rerun is called in the future.
    """
    try:
        data = await request.json()
        # check if this has analysis_id, tool_name and parent_step, and inputs
        analysis_id = data.get("analysis_id")
        tool_name = data.get("tool_name")
        parent_step = data.get("parent_step")
        inputs = data.get("inputs")
        outputs_storage_keys = data.get("outputs_storage_keys")

        if analysis_id is None or type(analysis_id) != str:
            return {"success": False, "error_message": "Invalid analysis id."}

        if (
            tool_name is None
            or type(tool_name) != str
            or tool_name not in tool_name_dict
        ):
            return {"success": False, "error_message": "Invalid tool name."}

        if parent_step is None or type(parent_step) != dict:
            return {"success": False, "error_message": "Invalid parent step."}

        if inputs is None or type(inputs) != dict:
            return {"success": False, "error_message": "Invalid inputs."}

        if outputs_storage_keys is None or type(outputs_storage_keys) != list:
            return {"success": False, "error_message": "Invalid outputs provided."}

        if len(outputs_storage_keys) == 0:
            return {"success": False, "error_message": "Please type in output names."}

        # if any of the outputs are empty or aren't strings
        if any([not o or type(o) != str for o in outputs_storage_keys]):
            return {
                "success": False,
                "error_message": "Outputs provided are either blank or incorrect.",
            }

        # try to get this analysis' data
        err, analysis_data = get_report_data(analysis_id)
        if err:
            return {"success": False, "error_message": err}

        # get the steps
        steps = analysis_data.get("gen_steps")
        if steps and steps["success"]:
            steps = steps["steps"]
        else:
            return {
                "success": False,
                "error_message": (
                    steps.get("error_message")
                    if steps is not None
                    else "No steps found for analysis"
                ),
            }

        err, tools = get_all_tools()
        if err:
            return {"success": False, "error_message": err}

        tool = tools[tool_name]

        new_tool_run_id = str(uuid4())

        # a new empty step
        new_step = {
            "tool_name": tool_name,
            "model_generated_inputs": inputs,
            "inputs": inputs,
            "input_metadata": tool["input_metadata"],
            "tool_run_id": new_tool_run_id,
            "outputs_storage_keys": outputs_storage_keys,
        }

        # add a step with the given inputs and tool_name
        steps.append(new_step)

        # store a empty tool run
        store_result = await store_tool_run(
            analysis_id,
            new_step,
            {
                "success": True,
                "code_str": tool["code"],
            },
            skip_step_update=True,
        )

        if not store_result["success"]:
            return store_result

        # update report data
        update_err = await update_report_data(analysis_id, "gen_steps", [new_step])

        if update_err:
            return {"success": False, "error_message": update_err}

        return {
            "success": True,
            "new_step": new_step,
            "tool_run_id": new_tool_run_id,
        }

    except Exception as e:
        logging.info("Error creating new step: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}
    return


@router.post("/delete_doc")
async def delete_doc_endpoint(request: Request):
    """
    Delete a document using the id passed.
    """
    try:
        data = await request.json()
        doc_id = data.get("doc_id")

        if doc_id is None or type(doc_id) != str:
            return {"success": False, "error_message": "Invalid document id."}

        err = await delete_doc(doc_id)

        if err:
            return {"success": False, "error_message": err}

        return {"success": True}
    except Exception as e:
        logging.info("Error deleting doc: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


# download csv using tool_run_id and output_storage_key
@router.post("/download_csv")
async def download_csv(request: Request):
    """
    Download a csv using the tool run id and output storage key.
    """
    try:
        data = await request.json()
        tool_run_id = data.get("tool_run_id")
        output_storage_key = data.get("output_storage_key")
        analysis_id = data.get("analysis_id")

        if tool_run_id is None or type(tool_run_id) != str:
            return {"success": False, "error_message": "Invalid tool run id."}

        if output_storage_key is None or type(output_storage_key) != str:
            return {"success": False, "error_message": "Invalid output storage key."}

        if analysis_id is None or type(analysis_id) != str:
            return {"success": False, "error_message": "Invalid analysis id."}

        # first try to find this file in the file system
        f_name = tool_run_id + "_output-" + output_storage_key + ".feather"
        f_path = os.path.join(report_assets_dir, "datasets", f_name)

        if not os.path.isfile(f_path):
            log_msg(
                f"Input {output_storage_key} not found in the file system. Rerunning step: {tool_run_id}"
            )
            # re run this step
            # get steps from db
            err, analysis_data = get_report_data(analysis_id)
            if err:
                return {"success": False, "error_message": err}

            global_dict = {
                "user_question": analysis_data["user_question"],
                "llm_calls_url": llm_calls_url,
                "report_assets_dir": report_assets_dir,
            }

            if err:
                return {"success": False, "error_message": err}

            steps = analysis_data.get("gen_steps")
            if steps and steps.get("success") and steps.get("steps"):
                steps = steps["steps"]
            else:
                return {"success": False, "error_message": steps["error_message"]}

            async for err, reran_id, new_data in rerun_step_and_dependents(
                analysis_id, tool_run_id, steps, global_dict=global_dict
            ):
                # don't need to yield unless there's an error
                # if error, then bail
                if err:
                    return {"success": False, "error_message": err}
        else:
            log_msg(
                f"Input {output_storage_key} found in the file system. No need to rerun step."
            )

        # now the file *should* be available
        df = pd.read_feather(f_path)

        return {
            "success": True,
            "tool_run_id": tool_run_id,
            "output_storage_key": output_storage_key,
            # get it as a csv string
            "csv": df.to_csv(index=False),
        }

    except Exception as e:
        logging.info("Error downloading csv: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


# an endpoint to delete steps.
# we will get a list of tool run ids
# we will remove these from the analysis


@router.post("/delete_steps")
async def delete_steps(request: Request):
    """
    Delete steps using the tool run ids passed.
    """
    try:
        data = await request.json()
        tool_run_ids = data.get("tool_run_ids")
        analysis_id = data.get("analysis_id")

        if tool_run_ids is None or type(tool_run_ids) != list:
            return {"success": False, "error_message": "Invalid tool run ids."}

        if analysis_id is None or type(analysis_id) != str:
            return {"success": False, "error_message": "Invalid analysis id."}

        # try to get this analysis' data
        err, analysis_data = get_report_data(analysis_id)
        if err:
            return {"success": False, "error_message": err}

        # get the steps
        steps = analysis_data.get("gen_steps")
        if steps and steps["success"]:
            steps = steps["steps"]
        else:
            return {
                "success": False,
                "error_message": (
                    steps.get("error_message")
                    if steps is not None
                    else "No steps found for analysis"
                ),
            }

        # remove the steps with these tool run ids
        new_steps = [s for s in steps if s["tool_run_id"] not in tool_run_ids]

        # # # update report data
        update_err = await update_report_data(
            analysis_id, "gen_steps", new_steps, replace=True
        )

        if update_err:
            return {"success": False, "error_message": update_err}

        return {"success": True, "new_steps": new_steps}

    except Exception as e:
        logging.info("Error deleting steps: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


@router.post("/get_user_tools")
async def get_user_tools(request: Request):
    """
    Get all tools available to the user.
    """
    err, tools = get_all_tools()
    if err:
        return {"success": False, "error_message": err}
    return {"success": True, "tools": tools}


@router.post("/delete_tool")
async def delete_tool_endpoint(request: Request):
    """
    Delete a tool using the tool name.
    """
    try:
        data = await request.json()
        function_name = data.get("function_name")

        if function_name is None or type(function_name) != str:
            return {"success": False, "error_message": "Invalid tool name."}

        err = await delete_tool(function_name)

        if err:
            return {"success": False, "error_message": err}

        logging.info("Deleted tool: " + function_name)

        return {"success": True}
    except Exception as e:
        logging.info("Error disabling tool: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


@router.post("/toggle_disable_tool")
async def toggle_disable_tool_endpoint(request: Request):
    """
    Toggle the disabled property of a tool using the tool name.
    """
    try:
        data = await request.json()
        function_name = data.get("function_name")

        if function_name is None or type(function_name) != str:
            return {"success": False, "error_message": "Invalid tool name."}

        err = await toggle_disable_tool(function_name)

        if err:
            raise Exception(err)

        return {"success": True}
    except Exception as e:
        logging.info("Error disabling tool: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


@router.post("/add_tool")
async def add_tool_endpoint(request: Request):
    """
    Add a tool to the defog_tools table.
    """
    try:
        data = await request.json()
        tool_name = data.get("tool_name")
        function_name = data.get("function_name")
        description = data.get("description")
        code = data.get("code")
        input_metadata = data.get("input_metadata")
        output_metadata = data.get("output_metadata")
        toolbox = data.get("toolbox")
        no_code = data.get("no_code", False)

        if (
            function_name is None
            or type(function_name) != str
            or len(function_name) == 0
        ):
            return {"success": False, "error_message": "Invalid tool name."}

        if description is None or type(description) != str or len(description) == 0:
            return {"success": False, "error_message": "Invalid description."}

        if code is None or type(code) != str or len(code) == 0:
            return {"success": False, "error_message": "Invalid code."}

        if input_metadata is None or type(input_metadata) != dict:
            return {"success": False, "error_message": "Invalid input_metadata."}

        if (
            output_metadata is None
            or type(output_metadata) != list
            or len(output_metadata) == 0
        ):
            return {
                "success": False,
                "error_message": "Invalid or empty output_metadata.",
            }

        if tool_name is None or type(tool_name) != str or len(tool_name) == 0:
            return {"success": False, "error_message": "Invalid display name."}

        if toolbox is None or type(toolbox) != str or len(toolbox) == 0:
            return {"success": False, "error_message": "Invalid toolbox."}

        if no_code is None or type(no_code) != bool:
            return {"success": False, "error_message": "Invalid no code."}

        err = await add_tool(
            tool_name,
            function_name,
            description,
            code,
            input_metadata,
            output_metadata,
            toolbox,
            no_code,
        )

        if err:
            raise Exception(err)

        logging.info("Added tool: " + function_name)

        return {"success": True}
    except Exception as e:
        logging.info("Error adding tool: " + str(e))
        # traceback.print_exc()
        return {"success": False, "error_message": str(e)[:300]}


@router.post("/submit_feedback")
async def submit_feedback(request: Request):
    """
    Submit feedback to the backend.
    """
    error = None
    try:
        data = await request.json()
        analysis_id = data.get("analysis_id")
        comments = data.get("comments", {})
        is_correct = data.get("is_correct", False)
        user_question = data.get("user_question")
        analysis_id = data.get("analysis_id")
        token = data.get("token")
        db_type = get_db_type()

        if analysis_id is None or type(analysis_id) != str:
            raise Exception("Invalid analysis id.")

        if user_question is None or type(user_question) != str:
            raise Exception("Invalid user question.")

        err, analysis_data = get_report_data(analysis_id)

        # store in the defog_plans_feedback table
        err, did_overwrite = await store_feedback(
            user_question,
            analysis_id,
            is_correct,
            comments,
            db_type,
        )

        if err:
            raise Exception(err)

        return {"success": True, "did_overwrite": did_overwrite}

        # cleaned_plan = get_clean_plan(analysis_data)
        # generated_plan_yaml = yaml.dump(cleaned_plan)
        # send the following to the defog server, and get feedback on how to improve it
        # - user_question
        # - comments
        # - metadata
        # - glossary
        # - plan generated
        # if not is_correct:
        #     err, tools = get_all_tools()
        #     tools = [
        #         {
        #             "function_name": tools[tool]["function_name"],
        #             "description": tools[tool]["description"],
        #             "input_metadata": tools[tool]["input_metadata"],
        #             "output_metadata": tools[tool]["output_metadata"],
        #         }
        #         for tool in tools
        #     ]

        # tool_description_yaml = yaml.dump(tools)

        # TODO: implement this on the defog server
        # r = requests.post(
        #     "https://api.defog.ai/reflect_on_agent_feedback",
        #     json={
        #         "question": user_question,
        #         "comments": comments,
        #         "plan_generated": generated_plan_yaml,
        #         "api_key": DEFOG_API_KEY,
        #         "tool_description": tool_description_yaml,
        #     },
        # )

        # we will get back:
        # - updated metadata
        # - updated glossary
        # - updated golden plan
        # raw_response = r.json()["diagnosis"]

        # # extract yaml from metadata
        # initial_recommended_plan = (
        #     raw_response.split("```yaml")[-1].split("```")[0].strip()
        # )
        # logging.info(initial_recommended_plan)
        # new_analysis_id = str(uuid4())
        # new_analysis_data = None
        # try:
        #     initial_recommended_plan = yaml.safe_load(initial_recommended_plan)
        #     # give each tool a tool_run_id
        #     # duplicate model_generated_inputs to inputs
        #     for i, item in enumerate(initial_recommended_plan):
        #         item["tool_run_id"] = str(uuid4())
        #         item["inputs"] = item["model_generated_inputs"].copy()

        #     # create a new analysis with these as steps
        #     err, new_analysis_data = await initialise_report(
        #         user_question,
        #         token,
        #         new_analysis_id,
        #         {"gen_steps": [], "clarify": []},
        #     )
        #     if err:
        #         raise Exception(err)

        #     setup, post_process = await execute(
        #         report_id=new_analysis_id,
        #         user_question=user_question,
        #         client_description=client_description,
        #         toolboxes=[],
        #         parent_analyses=[],
        #         similar_plans=[],
        #         predefined_steps=initial_recommended_plan,
        #     )

        #     if not setup.get("success"):
        #         raise Exception(setup.get("error_message", ""))

        #     final_executed_plan = []
        #     # run the generator
        #     if "generator" in setup:
        #         g = setup["generator"]
        #         async for step in g():
        #             # step comes in as a list of 1 step
        #             final_executed_plan += step
        #             err = await update_report_data(
        #                 new_analysis_id, "gen_steps", step
        #             )
        #             if err:
        #                 raise Exception(err)

        #     recommended_plan = final_executed_plan
        # except Exception as e:
        #     logging.info(e)
        #     # traceback.print_exc()
        #     recommended_plan = None
        #     new_analysis_data = None

        # if err is not None:
        #     raise Exception(err)

        # return {
        #     "success": True,
        #     "did_overwrite": did_overwrite,
        #     "suggested_improvements": raw_response,
        #     "recommended_plan": recommended_plan,
        #     "new_analysis_id": new_analysis_id,
        #     "new_analysis_data": new_analysis_data,
        # }
        # else:
        #     return {"success": True, "did_overwrite": did_overwrite}

    except Exception as e:
        logging.info(str(e))
        error = str(e)[:300]
        logging.info(error)
        # traceback.print_exc()
        return {"success": False, "error_message": error}


@router.post("/get_analysis_versions")
async def get_analysis_versions_endpoint(request: Request):
    # get all analysis ids that have teh suffix -v1, -v2, -v3 etc
    try:
        params = await request.json()
        root_analysis_id = params.get("root_analysis_id", None)

        if not root_analysis_id:
            raise Exception("No root analysis provided.")

        await get_analysis_versions(root_analysis_id)
        pass
    except Exception as e:
        logging.info("Error getting analysis versions: " + str(e))
        # traceback.print_exc()
        return {
            "success": False,
            "error_message": "Unable to get versions: " + str(e[:300]),
        }


@router.post("/update_dashboard_data")
async def update_dashboard_data_endpoint(request: Request):
    try:
        data = await request.json()
        if data.get("doc_uint8") is None:
            return {"success": False, "error_message": "No document data provided."}

        if data.get("doc_id") is None:
            return {"success": False, "error_message": "No document id provided."}

        col_name = "doc_blocks" if data.get("doc_blocks") else "doc_uint8"
        err = await update_doc_data(
            data.get("doc_id"),
            [col_name, "doc_title"],
            {col_name: data.get(col_name), "doc_title": data.get("doc_title")},
        )
        if err:
            return {"success": False, "error_message": err}

        return {"success": True}
    except Exception as e:
        logging.info("Error adding analysis to dashboard: " + str(e))
        # traceback.print_exc()
        return {
            "success": False,
            "error_message": "Unable to add analysis to dashboard: " + str(e)[:300],
        }


@router.post("/generate_tool_code")
async def generate_tool_code_endpoint(request: Request):
    try:
        data = await request.json()
        tool_name = data.get("tool_name")
        tool_description = data.get("tool_description")
        user_question = data.get("user_question")
        current_code = data.get("current_code")

        if not tool_name:
            raise Exception("Invalid parameters.")

        if not user_question or user_question == "":
            user_question = "Please write the tool code."

        payload = {
            "request_type": "generate_tool_code",
            "tool_name": tool_name,
            "tool_description": tool_description,
            "user_question": user_question,
            "current_code": current_code,
            "api_key": get_api_key(),
        }

        retries = 0
        error = None
        while retries < 3:
            try:
                logging.info(payload)
                resp = requests.post(
                    llm_calls_url,
                    json=payload,
                ).json()

                # testing code has two functions: generate_sample_inputs and test_tool
                if resp.get("error_message"):
                    raise Exception(resp.get("error_message"))

                tool_code = resp["tool_code"]
                testing_code = resp["testing_code"]

                # find the function name in tool_code
                try:
                    function_name = tool_code.split("def ")[1].split("(")[0]
                except Exception as e:
                    logging.error("Error finding function name: " + str(e))
                    # default to snake case tool name
                    function_name = snake_case(tool_name)
                    logging.error(
                        "Defaulting to snake case tool name: " + function_name
                    )

                # try running this code
                err, testing_details = await execute_code(
                    [tool_code, testing_code], "test_tool"
                )

                if err:
                    raise Exception(err)

                # unfortunately testing_details has outputs, and inside of it is another outputs which is returned by the tool :tear:
                testing_details["outputs"] = testing_details["outputs"]["outputs"]

                # convert inputs to a format we can send back to the user
                # convert pandas dfs to csvs in both inoputs and outputs
                for i, input in enumerate(testing_details["inputs"]):
                    value = input["value"]
                    if type(value) == pd.DataFrame:
                        testing_details["inputs"][i]["value"] = value.to_csv(
                            index=False
                        )

                for output in testing_details["outputs"]:
                    output["data"] = output["data"].to_csv(index=False)

                return JSONResponse(
                    {
                        "success": True,
                        "tool_name": tool_name,
                        "tool_description": tool_description,
                        "generated_code": tool_code,
                        "testing_code": testing_code,
                        "function_name": function_name,
                        "testing_results": {
                            "inputs": testing_details["inputs"],
                            "outputs": testing_details["outputs"],
                        },
                    }
                )
            except Exception as e:
                error = str(e)[:300]
                logging.info("Error generating tool code: " + str(e))
                # traceback.print_exc()
            finally:
                if error:
                    payload = {
                        "request_type": "fix_tool_code",
                        "error": error,
                        "messages": resp["messages"],
                        "api_key": get_api_key(),
                    }
                retries += 1

        logging.info("Max retries reached but couldn't generate code.")
        raise Exception("Max retries exceeded but couldn't generate code.")

    except Exception as e:
        logging.info("Error generating tool code: " + str(e))
        # traceback.print_exc()
        return {
            "success": False,
            "error_message": "Unable to generate tool code: " + str(e)[:300],
        }
