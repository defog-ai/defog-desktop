import inspect
import json
import logging
import traceback
import datetime
import uuid
import pandas as pd
from sqlalchemy import (
    create_engine,
    select,
    update,
    insert,
    delete,
)
from sqlalchemy.ext.automap import automap_base

import asyncio
from utils import warn_str, YieldList, make_request
import os

from pathlib import Path

home_dir = Path.home()
# see if we have a custom report assets directory
if not os.path.exists(home_dir / "defog_report_assets"):
    # create one
    os.mkdir(home_dir / "defog_report_assets")

analysis_assets_dir = home_dir / "defog_report_assets"
analysis_assets_dir = os.environ.get(
    "REPORT_ASSETS_DIR", analysis_assets_dir.as_posix()
)


print("using sqlite as our internal db")
# if using sqlite
connection_uri = "sqlite:///defog_local.db"
engine = create_engine(connection_uri, connect_args={"timeout": 3})

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

Analyses = Base.classes.defog_analyses
TableCharts = Base.classes.defog_table_charts
ToolRuns = Base.classes.defog_tool_runs
Toolboxes = Base.classes.defog_toolboxes
Tools = Base.classes.defog_tools
Users = Base.classes.defog_users
Feedback = Base.classes.defog_plans_feedback
DbCreds = Base.classes.defog_db_creds


def save_csv_to_db(table_name, data):
    df = pd.DataFrame(data[1:], columns=data[0])
    if "" in df.columns:
        del df[""]
    print(df)
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        return True
    except Exception as e:
        print(e)
        return False


def get_db_type_creds(api_key):
    with engine.begin() as conn:
        row = conn.execute(
            select(DbCreds.db_type, DbCreds.db_creds).where(DbCreds.api_key == api_key)
        ).fetchone()

    print(row)

    return row


def update_db_type_creds(api_key, db_type, db_creds):
    with engine.begin() as conn:
        # first, check if the record exists
        record = conn.execute(
            select(DbCreds).where(DbCreds.api_key == api_key)
        ).fetchone()

        if record:
            conn.execute(
                update(DbCreds)
                .where(DbCreds.api_key == api_key)
                .values(db_type=db_type, db_creds=db_creds)
            )
        else:
            conn.execute(
                insert(DbCreds).values(
                    api_key=api_key, db_type=db_type, db_creds=db_creds
                )
            )

    return True


def validate_user(token, user_type=None, get_username=False):
    with engine.begin() as conn:
        user = conn.execute(
            select(Users).where(Users.hashed_password == token)
        ).fetchone()

    if user:
        if user_type == "admin":
            if user[0] == "admin":
                if get_username:
                    return user[1]
                else:
                    return True
            else:
                return False
        else:
            if get_username:
                return user[1]
            else:
                return True
    else:
        return False


async def execute_code(
    code_snippets: list,  # list of code strings to execute
    fn_name=None,  # function name to call
    use_globals=False,  # whether to use globals as the sandbox
):
    """
    Runs code string and returns output.
    """
    err = None
    out = None
    try:
        sandbox = {}
        if use_globals:
            sandbox = globals()

        for code in code_snippets:
            exec(code, sandbox)

        if fn_name:
            # check if test_tool is an async function
            if inspect.iscoroutinefunction(sandbox[fn_name]):
                out = await sandbox[fn_name]()
            else:
                out = sandbox[fn_name]()
    except Exception as e:
        out = None
        err = str(e)
        sandbox = None
        traceback.print_exc()
    finally:
        return err, out, sandbox


async def initialise_analysis(
    user_question, token, api_key, custom_id=None, other_data={}
):
    username = validate_user(token, get_username=True)
    if not username:
        return "Invalid token.", None

    err = None
    timestamp = str(datetime.datetime.now())
    new_analysis_data = None

    try:
        """Create a new analyis in the defog_analyses table"""
        with engine.begin() as conn:
            if not custom_id or custom_id == "":
                analysis_id = str(uuid.uuid4())
            else:
                analysis_id = custom_id
            print("Creating new analyis with uuid: ", analysis_id)
            new_analysis_data = {
                "user_question": user_question,
                "timestamp": timestamp,
                "analysis_id": analysis_id,
                "api_key": api_key,
                "username": username,
            }
            if other_data is not None and type(other_data) is dict:
                new_analysis_data.update(other_data)

            conn.execute(insert(Analyses).values(new_analysis_data))
            # if other data has parent_analyses, insert analysis_id into the follow_up_analyses column, which is an array, of all the parent analyses
            if (
                other_data is not None
                and type(other_data) is dict
                and other_data.get("parent_analyses") is not None
            ):
                for parent_analysis_id in other_data.get("parent_analyses"):
                    # get the parent analysis
                    parent_analysis = conn.execute(
                        select(Analyses).where(
                            Analyses.analysis_id == parent_analysis_id
                        )
                    ).fetchone()
                    if parent_analysis is not None:
                        parent_analysis = parent_analysis._mapping
                        # get the follow_up_analyses array
                        follow_up_analyses = (
                            parent_analysis.get("follow_up_analyses") or []
                        )
                        # add the analysis_id to the array
                        follow_up_analyses.append(analysis_id)
                        # update the row
                        conn.execute(
                            update(Analyses)
                            .where(Analyses.analysis_id == parent_analysis_id)
                            .values(follow_up_analyses=follow_up_analyses)
                        )
                    else:
                        print(
                            "Could not find parent analysis with id: ",
                            parent_analysis_id,
                        )

    except Exception as e:
        traceback.print_exc()
        print(e)
        err = "Could not create a new analysis."
        new_analysis_data = None
    finally:
        return err, new_analysis_data


def get_analysis_data(analysis_id):
    try:
        err = None
        analysis_data = {}

        if analysis_id == "" or not analysis_id:
            print(analysis_id == "")
            print(analysis_id is None)
            print(not analysis_id)
            err = "Could not find analyis. Are you sure you have the correct link?"

        elif analysis_id != "" and analysis_id is not None and analysis_id != "new":
            print("Looking for uuid: ", analysis_id)
            # try to fetch analysis_data data
            with engine.begin() as conn:
                row = conn.execute(
                    select(Analyses).where(Analyses.analysis_id == analysis_id)
                ).fetchone()

                if row:
                    print("Found uuid: ", analysis_id)
                    analysis_data = analysis_data_from_row(row)
                else:
                    err = "Could not find analyis. Are you sure you have the correct link?"

    except Exception as e:
        err = "Server error. Please contact us."
        analysis_data = None
        print(e)
        traceback.print_exc()

    finally:
        return err, analysis_data


def get_assignment_understanding(analysis_id):
    """
    Returns the assignment_understanding column from the analysis with the given analysis_id
    """

    try:
        err = None
        understanding = None

        if analysis_id == "" or not analysis_id:
            err = "Could not find analyis. Are you sure you have the correct link?"

        elif analysis_id != "" and analysis_id is not None and analysis_id != "new":
            # try to fetch analysis_data data
            with engine.begin() as conn:
                row = conn.execute(
                    select(
                        Analyses.__table__.columns["assignment_understanding"]
                    ).where(Analyses.analysis_id == analysis_id)
                ).fetchone()

                if row:
                    understanding = row.assignment_understanding
                else:
                    err = "Could not find analyis. Are you sure you have the correct link?"

    except Exception as e:
        err = "Server error."
        understanding = None
        print(e)
        traceback.print_exc()
    finally:
        return err, understanding


def update_assignment_understanding(analysis_id, understanding):
    """
    Updates the assignment_understanding column in the analysis with the given analysis_id
    """

    try:
        err = None

        if analysis_id == "" or not analysis_id:
            err = "Could not find analyis. Are you sure you have the correct link?"

        elif analysis_id != "" and analysis_id is not None and analysis_id != "new":
            # try to fetch analysis_data data
            with engine.begin() as conn:
                conn.execute(
                    update(Analyses)
                    .where(Analyses.analysis_id == analysis_id)
                    .values(assignment_understanding=understanding)
                )

    except Exception as e:
        err = "Server error."
        print(e)
        traceback.print_exc()
    finally:
        return err


async def update_analysis_data(
    analysis_id, request_type=None, new_data=None, replace=False, overwrite_key=None
):
    err = None
    request_types = [
        "clarify",
        "understand",
        "gen_approaches",
        "gen_steps",
        "gen_analysis",
        "user_question",
    ]
    try:
        # if new data is a list, filter out null elements
        # this can sometimes happen when the LLM server takes too long to respond etc.
        if type(new_data) == list:
            new_data = list(filter(None, new_data))

        if request_type is None or request_type not in request_types:
            err = "Incorrect request_type: " + request_type

        else:
            with engine.begin() as conn:
                # first get the data
                row = conn.execute(
                    select(Analyses.__table__.columns[request_type]).where(
                        Analyses.analysis_id == analysis_id
                    )
                ).fetchone()

                if row:
                    curr_data = getattr(row, request_type) or []
                    print("current data length ", len(curr_data))

                    # if new data is a list and we're not asked to replace, concat
                    # if new data is anything else, replace
                    if (
                        type(new_data) == list or type(new_data) == YieldList
                    ) and not replace:
                        if not overwrite_key or type(overwrite_key) != str:
                            curr_data = curr_data + new_data
                        # if there's an overwrite_key provided,
                        # then go through old data, and the new_data
                        # if the overwrite_key is found in the old data, replace it with the elements that exist new_data with the same overwrite_key
                        # if it's not found, just append the item to the end
                        else:
                            print(
                                "Overwriting data with overwrite_key: ", overwrite_key
                            )
                            replaced = 0
                            for i, item in enumerate(new_data):
                                # try to find the item
                                found = False
                                for j, old_item in enumerate(curr_data):
                                    if old_item.get(overwrite_key) == item.get(
                                        overwrite_key
                                    ):
                                        curr_data[j] = item
                                        found = True
                                        replaced += 1
                                        break
                                if not found:
                                    # just append
                                    logging.info("Item not found. Appending.")
                                    curr_data.append(item)

                            print(
                                f"Replaced {replaced} items in {request_type} with overwrite_key: {overwrite_key}"
                            )
                            print(
                                "New length of ", request_type, " is ", len(curr_data)
                            )
                    else:
                        curr_data = new_data
                    print("writing to ", request_type, "in analyis id: ", analysis_id)
                    print("writing array of length: ", len(curr_data))
                    # insert back into analyses table
                    # if the request type is user_question, we will also update the embedding
                    if request_type == "user_question":
                        conn.execute(
                            update(Analyses)
                            .where(Analyses.analysis_id == analysis_id)
                            .values({request_type: new_data})
                        )
                    else:
                        conn.execute(
                            update(Analyses)
                            .where(Analyses.analysis_id == analysis_id)
                            .values({request_type: curr_data})
                        )
                else:
                    err = "Analysis not found."
                    raise ValueError(err)

    except Exception as e:
        err = str(e)
        print(e)
        traceback.print_exc()
    finally:
        return err


def analysis_data_from_row(row):
    rpt = None
    try:
        clarify = None if row.clarify is None else row.clarify
        gen_steps = None if row.gen_steps is None else row.gen_steps
        parent_analyses = row.parent_analyses or []
        follow_up_analyses = row.follow_up_analyses or []
        direct_parent_id = row.direct_parent_id or None

        # send only the ones that are not none.
        # we should have a better solution to this.
        rpt = {
            "user_question": row.user_question,
            "analysis_id": row.analysis_id,
            "timestamp": row.timestamp,
            "parent_analyses": parent_analyses,
            "follow_up_analyses": follow_up_analyses,
            "direct_parent_id": direct_parent_id,
        }

        if clarify is not None:
            rpt["clarify"] = {
                "success": True,
                "clarification_questions": clarify,
            }

        if gen_steps is not None:
            rpt["gen_steps"] = {
                "success": True,
                "steps": gen_steps,
            }

    except Exception as e:
        print(e)
        traceback.print_exc()
        rpt = None
    finally:
        return rpt


def get_all_analyses(api_key: str):
    # get analyses from the analyses table
    err = None
    analyses = []
    try:
        with engine.begin() as conn:
            # first get the data
            rows = conn.execute(
                select(Analyses).where(Analyses.api_key == api_key)
            ).fetchall()
            if len(rows) > 0:
                # reshape with "success = true"
                for row in rows:
                    rpt = analysis_data_from_row(row)
                    if rpt is not None:
                        analyses.append(rpt)
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = "Something went wrong while fetching your analyses. Please contact us."
        analyses = None
    finally:
        return err, analyses


def create_table_chart(table_data):
    err = None
    if table_data is None or table_data.get("table_id") is None:
        return "Invalid table data"

    try:
        with engine.begin() as conn:
            print("Creating new table chart with id: ", table_data.get("table_id"))
            conn.execute(insert(TableCharts).values(table_data))

    except Exception as e:
        err = str(e)
        print(e)
        traceback.print_exc()
    finally:
        return err


async def update_table_chart_data(table_id, edited_table_data):
    err = None
    analysis = None
    updated_data = None

    if table_id is None:
        return "Invalid table data"

    try:
        with engine.begin() as conn:
            # check if exists.
            # if not, create
            row = conn.execute(
                select(TableCharts).where(TableCharts.table_id == table_id)
            ).fetchone()

            if not row:
                err = "Invalid table id"
            else:
                # print(edited_table_data)
                print("Running table again...")

                # execute the new code
                err, analysis, updated_data = await execute_code(
                    edited_table_data["code"]
                )

                if err is None:
                    chart_images = []
                    if hasattr(updated_data, "kmc_plot_paths"):
                        chart_images = [
                            {"path": kmc_path, "type": "kmc"}
                            for kmc_path in updated_data.kmc_plot_paths
                        ]

                    updated_data = {
                        "data_csv": updated_data.to_csv(
                            float_format="%.3f", index=False
                        ),
                        "sql": edited_table_data.get("sql"),
                        "code": edited_table_data.get("code"),
                        "tool": edited_table_data.get("tool"),
                        "reactive_vars": (
                            updated_data.reactive_vars
                            if hasattr(updated_data, "reactive_vars")
                            else None
                        ),
                        "table_id": table_id,
                        "chart_images": chart_images,
                        "error": None,
                    }

                    # insert the data back into TableCharts table
                    print("writing to table chart, table id: ", table_id)
                    updated_data["edited"] = True

                    conn.execute(
                        update(TableCharts)
                        .where(TableCharts.table_id == table_id)
                        .values(updated_data)
                    )
                else:
                    print("Error: ", err)
    except Exception as e:
        err = str(e)
        analysis = None
        updated_data = None
        print(e)
        traceback.print_exc()
    finally:
        return err, analysis, updated_data


async def get_table_data(table_id):
    err = None
    table_data = None
    if table_id == "" or table_id is None or not table_id:
        return "Invalid table data", None

    try:
        with engine.begin() as conn:
            # check if document exists
            row = conn.execute(
                select(TableCharts).where(TableCharts.table_id == table_id)
            ).fetchone()

            if row:
                # document exists
                print("Found table with id: ", table_id)
                table_data = row._mapping

            else:
                err = "Table not found."

    except Exception as e:
        traceback.print_exc()
        print(e)
        err = "Could not find table."
        table_data = None
    finally:
        return err, table_data


async def get_all_analyses(api_key: str):
    # get analyses from the analyses table
    err = None
    analyses = []
    try:
        """Create a new analyis in the defog_analyses table"""
        with engine.begin() as conn:
            # first get the data
            rows = conn.execute(
                select(
                    *[
                        Analyses.__table__.columns["analysis_id"],
                        Analyses.__table__.columns["user_question"],
                    ]
                )
                .where(Analyses.api_key == api_key)
                .where(Analyses.analysis_id.contains("analysis"))
            ).fetchall()

            if len(rows) > 0:
                for row in rows:
                    analyses.append(row._mapping)
    except Exception as e:
        traceback.print_exc()
        print(e)
        err = "Could not find analyses for the user."
        analyses = []
    finally:
        return err, analyses


async def get_toolboxes(token):
    username = validate_user(token, get_username=True)
    if not username:
        return "Invalid token.", None
    # table is defog_agent_toolboxes
    # get all toolboxes available to a user using the username
    err = None
    toolboxes = []
    try:
        with engine.begin() as conn:
            rows = conn.execute(
                select(Toolboxes).where(Toolboxes.username == username)
            ).fetchall()

            for row in rows:
                row_dict = row._mapping

                if len(row_dict["toolboxes"]) == 0:
                    continue

                if row_dict["toolboxes"][0] == "*":
                    toolboxes = ["data-fetching", "stats", "plots", "cancer-survival"]
                    break

                else:
                    toolboxes += row_dict["toolboxes"]
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = "Could not fetch toolboxes for the user."
        toolboxes = []
    finally:
        return err, toolboxes


async def update_particular_step(analysis_id, tool_run_id, prop, new_val):
    if tool_run_id is None or prop is None or analysis_id is None:
        return "Invalid tool run data"

    # get the analyis data
    with engine.begin() as conn:
        analysis_data = conn.execute(
            select(Analyses).where(Analyses.analysis_id == analysis_id)
        ).fetchone()

        if analysis_data is not None:
            # copy row mapping
            analyis = analysis_data._mapping
            # update the property
            new_steps = analyis.gen_steps
            for step in new_steps:
                if step["tool_run_id"] == tool_run_id:
                    step[prop] = new_val
                    break

            # update the row
            conn.execute(
                update(Analyses)
                .where(Analyses.analysis_id == analysis_id)
                .values(gen_steps=new_steps)
            )


# skip_step_update helps us skip a step update when createing a new step
# we first run the tool, and only if it runs fully, we create a new step in the analysis.
async def store_tool_run(analysis_id, step, run_result, skip_step_update=False):
    try:
        insert_data = {
            "analysis_id": analysis_id,
            "tool_run_id": step["tool_run_id"],
            "tool_name": step["tool_name"],
            "step": step,
            "tool_run_details": {},
            "outputs": {},
            "error_message": run_result.get("error_message"),
            "edited": False,
        }
        # store everything but the "outputs" key in tool_run_details
        for k, v in run_result.items():
            if k != "outputs":
                insert_data["tool_run_details"][k] = v

        # we will store chart images right now
        files_to_store_in_gcs = []
        # feather files later
        files_for_rabbitmq_queue = []

        # could have been an error, if so, no outputs
        if "outputs" in run_result:
            for i, k in enumerate(step["outputs_storage_keys"]):
                # if output is a pandas df, convert to csv
                out = run_result["outputs"][i]
                data = out.get("data")
                chart_images = out.get("chart_images")
                reactive_vars = out.get("reactive_vars")
                analysis = out.get("analysis")

                insert_data["outputs"][k] = {}

                if data is not None and type(data) == type(pd.DataFrame()):
                    # save this dataset on local disk in feather format in analysis_dataset_dir/datasets
                    db_path = step["tool_run_id"] + "_output-" + k + ".feather"

                    # for sending to client, store max 1000 rows
                    if len(data) > 1000:
                        print(
                            warn_str(
                                "More than 1000 rows in output. Storing full db as feather, but sending only 1000 rows to client."
                            )
                        )

                    insert_data["outputs"][k]["data"] = data.head(1000).to_csv(
                        float_format="%.3f", index=False
                    )

                    # de-duplicate column names
                    # if the same column name exists more than once, add a suffix
                    columns = data.columns.tolist()
                    seen = {}
                    for i, item in enumerate(columns):
                        if item in seen:
                            columns[i] = f"{item}_{seen[item]}"
                            seen[item] += 1
                        else:
                            seen[item] = 1

                    data.columns = columns

                    # have to reset index for feather to work
                    data.reset_index(drop=True).to_feather(
                        analysis_assets_dir + "/datasets/" + db_path
                    )

                    # also store this in gcs
                    files_for_rabbitmq_queue.append(
                        analysis_assets_dir + "/datasets/" + db_path
                    )

                # check if it has reactive_vars
                if reactive_vars is not None:
                    insert_data["outputs"][k]["reactive_vars"] = reactive_vars

                # check if it has chart images
                if chart_images is not None:
                    insert_data["outputs"][k]["chart_images"] = chart_images
                    try:
                        # i fear some error here someday
                        files_to_store_in_gcs += [
                            analysis_assets_dir + "/" + img["path"]
                            for img in chart_images
                        ]
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        print("Could not store chart images to gcs")

                # check if it has analysis
                if analysis is not None and analysis != "":
                    insert_data["outputs"][k]["analysis"] = analysis

            # add files to rabbitmq queue
            # if len(files_for_rabbitmq_queue) > 0:
            #     err = await add_files_to_rabbitmq_queue(files_for_rabbitmq_queue)
            #     if err is not None:
            #         print(error_str(err))

            # # store images to gcs now
            # if len(files_to_store_in_gcs) > 0:
            #     await store_files_to_gcs(files_to_store_in_gcs)

        with engine.begin() as conn:
            # first check if this tool run already exists
            rows = conn.execute(
                select(ToolRuns).where(ToolRuns.tool_run_id == step["tool_run_id"])
            ).fetchone()
            if rows is not None:
                # update the row
                conn.execute(
                    update(ToolRuns)
                    .where(ToolRuns.tool_run_id == step["tool_run_id"])
                    .values(insert_data)
                )
            else:
                conn.execute(insert(ToolRuns).values(insert_data))

        if not skip_step_update:
            # also update the error message in gen_steps in the analyses table
            await update_particular_step(
                analysis_id,
                step["tool_run_id"],
                "error_message",
                run_result.get("error_message"),
            )

        return {"success": True, "tool_run_data": insert_data}
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Could not store tool run")
        return {"success": False, "error_message": str(e)}


async def get_tool_run(tool_run_id):
    error = None
    tool_run_data = None
    try:
        with engine.begin() as conn:
            rows = conn.execute(
                select(ToolRuns).where(ToolRuns.tool_run_id == tool_run_id)
            ).fetchall()

            if len(rows) == 0:
                return "Tool run not found", None

            row = rows[0]
            tool_run_data = row._mapping
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Could not fetch tool run")
        tool_run_data = None
        error = str(e)
    finally:
        return error, tool_run_data


async def update_tool_run_data(analysis_id, tool_run_id, prop, new_val):
    """
    Update a single property of a tool run.
    """

    error = None
    new_data = None

    # if new_val is a pandas df, only print the shape and columns
    if type(new_val) == type(pd.DataFrame()):
        print(
            "Updating property: ", prop, " with value: ", new_val.shape, new_val.columns
        )
    else:
        print("Updating property: ", prop, " with value: ", new_val)

    try:
        if tool_run_id is None or prop is None or analysis_id is None:
            raise Exception("Invalid tool run data")

        with engine.begin() as conn:
            # get tool run data
            row = conn.execute(
                select(ToolRuns).where(ToolRuns.tool_run_id == tool_run_id)
            ).fetchone()
            if row is None:
                error = "Tool run not found"
                raise Exception(error)

        step = row._mapping.step

        if prop == "sql" or prop == "code_str" or prop == "analysis":
            # these exist in tool_run_details
            # copy row mapping
            tool_run_details = row._mapping.tool_run_details
            # update the property
            tool_run_details[prop] = new_val
            # also set edited to True
            # update the row
            with engine.begin() as conn:
                conn.execute(
                    update(ToolRuns)
                    .where(ToolRuns.tool_run_id == tool_run_id)
                    .values(tool_run_details=tool_run_details, edited=True)
                )
        elif prop == "error_message":
            # update the row
            # probably after a re run, so set edited to false
            # tool_run_data also unfortunately has error message in it's "step"
            new_step = row._mapping.step
            new_step["error_message"] = new_val
            with engine.begin() as conn:
                conn.execute(
                    update(ToolRuns)
                    .where(ToolRuns.tool_run_id == tool_run_id)
                    .values(error_message=new_val, edited=False, step=new_step)
                )
            # also remove errors from the steps in the analysis_data
            await update_particular_step(
                analysis_id, tool_run_id, "error_message", new_val
            )

        elif prop == "inputs":
            # these exist in step
            # copy row mapping
            # update the property
            step[prop] = new_val
            # also set edited to True
            # update the row
            with engine.begin() as conn:
                conn.execute(
                    update(ToolRuns)
                    .where(ToolRuns.tool_run_id == tool_run_id)
                    .values(step=step, analysis_id=analysis_id, edited=True)
                )
            # we should also update this in the defog_analyses table in the gen_steps column
            await update_particular_step(analysis_id, tool_run_id, "inputs", new_val)

        elif prop == "outputs":
            files_for_rabbitmq_queue = []
            # set edited to false because this is most probably after a re run
            # this will only be called if data_Fetcher was re run with a new sql.
            # all other tools re runs will use the store_tool_run function.
            # don't need to check for chart_images or reactive_vars
            for k in new_val:
                # update the row
                # save this dataset on local disk in feather format in analysis_dataset_dir/datasets
                db_path = step["tool_run_id"] + "_output-" + k + ".feather"
                data = new_val[k]["data"]

                if data is not None and type(data) == type(pd.DataFrame()):
                    if len(data) > 1000:
                        print(
                            warn_str(
                                "More than 1000 rows in output. Storing full db as feather, but sending only 1000 rows to client."
                            )
                        )

                    # for sending to client, store max 1000 rows
                    new_val[k]["data"] = data.head(1000).to_csv(
                        float_format="%.3f", index=False
                    )

                    # have to reset index for feather to work
                    data.reset_index(drop=True).to_feather(
                        analysis_assets_dir + "/datasets/" + db_path
                    )

                    # also store this in gcs

                    files_for_rabbitmq_queue.append(
                        analysis_assets_dir + "/datasets/" + db_path
                    )

            # add files to rabbitmq queue
            # if len(files_for_rabbitmq_queue) > 0:
            #     err = await add_files_to_rabbitmq_queue(files_for_rabbitmq_queue)
            #     if err is not None:
            #         print(error_str(err))

            with engine.begin() as conn:
                conn.execute(
                    update(ToolRuns)
                    .where(ToolRuns.tool_run_id == tool_run_id)
                    .values(outputs=new_val, edited=False)
                )

        with engine.begin() as conn:
            row = conn.execute(
                select(ToolRuns).where(ToolRuns.tool_run_id == tool_run_id)
            ).fetchone()

        if row is not None:
            new_data = dict(row._mapping)

        return {"success": True, "tool_run_data": new_data}
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Could not fetch tool run")
        error = str(e)
        return {"success": False, "error_message": str(e)}


def get_multiple_analyses(analysis_ids=[], columns=["analysis_id", "user_question"]):
    err = None
    analyses = []
    try:
        with engine.begin() as conn:
            # first get the data
            rows = conn.execute(
                select(
                    *[
                        Analyses.__table__.columns[c]
                        for c in columns
                        if c in Analyses.__table__.columns
                    ]
                ).where(Analyses.analysis_id.in_(analysis_ids))
            ).fetchall()

            if len(rows) > 0:
                for row in rows:
                    analyses.append(row._mapping)
    except Exception as e:
        traceback.print_exc()
        print(e)
        err = "Could not find analyses for the user."
        analyses = []
    finally:
        return err, analyses


async def store_feedback(
    api_key,
    user_question,
    analysis_id,
    is_correct,
    comments,
    db_type,
):
    error = None
    did_overwrite = False

    asyncio.create_task(
        make_request(
            f"{os.environ.get('DEFOG_BASE_URL', 'https://api.defog.ai')}/update_agent_feedback",
            {
                "api_key": api_key,
                "user_question": user_question,
                "analysis_id": analysis_id,
                "is_correct": is_correct,
                "comments": comments,
                "db_type": db_type,
            },
        )
    )

    return error, did_overwrite


def get_all_tools():
    err = None
    tools = {}
    try:
        with engine.begin() as conn:
            all_tools = conn.execute(select(Tools)).fetchall()
            # convert this to a dictionary without embedding
            all_tools = {
                tool.function_name: {
                    "tool_name": tool.tool_name,
                    "function_name": tool.function_name,
                    "description": tool.description,
                    "code": tool.code,
                    "toolbox": tool.toolbox,
                    "input_metadata": tool.input_metadata,
                    "output_metadata": tool.output_metadata,
                    "cannot_delete": tool.cannot_delete,
                    "cannot_disable": tool.cannot_disable,
                    "disabled": tool.disabled,
                }
                for tool in all_tools
            }

            # if user_question_embedding is None, return all tools
            tools = all_tools

    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
        tools = []
    finally:
        return err, tools


async def add_tool(
    api_key,
    tool_name,
    function_name,
    description,
    code,
    input_metadata,
    output_metadata,
    toolbox,
    cannot_delete=False,
    cannot_disable=False,
):
    err = None
    try:
        embedding = None
        # insert into the tools table
        with engine.begin() as conn:
            # first check if it exists
            row = conn.execute(
                select(Tools).where(Tools.tool_name == tool_name)
            ).fetchone()

        # check if latest tool code is same as the code we are trying to insert
        no_changes = False
        if row:
            no_changes = row.code == code

        if no_changes:
            print(f"Tool {tool_name} already exists and no code changes detected.")
        else:
            with engine.begin() as conn:
                # delete if exists
                if row:
                    conn.execute(delete(Tools).where(Tools.tool_name == tool_name))

                # update with latest
                conn.execute(
                    insert(Tools).values(
                        {
                            "tool_name": tool_name,
                            "function_name": function_name,
                            "description": description,
                            "code": code,
                            "toolbox": toolbox,
                            "input_metadata": input_metadata,
                            "output_metadata": output_metadata,
                            "cannot_delete": cannot_delete,
                            "cannot_disable": cannot_disable,
                            "disabled": False,
                        }
                    )
                )

        print("Adding tool to the defog API server", tool_name)
        asyncio.create_task(
            make_request(
                url=f"{os.environ.get('DEFOG_BASE_URL', 'https://api.defog.ai')}/update_tool",
                payload={
                    "api_key": api_key,
                    "tool_name": tool_name,
                    "function_name": function_name,
                    "description": description,
                    "code": code,
                    "embedding": embedding,
                    "input_metadata": input_metadata,
                    "output_metadata": output_metadata,
                    "toolbox": toolbox,
                    "disabled": False,
                    "cannot_delete": cannot_delete,
                    "cannot_disable": cannot_disable,
                },
                verbose=True,
            )
        )
    except ValueError as e:
        err = str(e)
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
    finally:
        return err


async def update_tool(function_name, update_dict):
    err = None
    try:
        with engine.begin() as conn:
            # check if tool exists
            row = conn.execute(
                select(Tools).where(Tools.function_name == function_name)
            ).fetchone()

            if row is None:
                raise ValueError(f"Tool {function_name} does not exist.")
            else:
                # update with latest
                conn.execute(
                    update(Tools)
                    .where(Tools.function_name == function_name)
                    .values(update_dict)
                )
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
    finally:
        return err


async def toggle_disable_tool(function_name):
    err = None
    try:
        with engine.begin() as conn:
            # check cannot_disable
            rows = conn.execute(
                select(Tools).where(Tools.function_name == function_name)
            ).fetchone()
            if rows is None:
                raise ValueError(f"Tool {function_name} does not exist.")
            elif rows.cannot_disable:
                raise ValueError(
                    f"Tool {function_name} cannot be disabled. Please contact admin."
                )
            else:
                conn.execute(
                    update(Tools)
                    .where(Tools.function_name == function_name)
                    .values(disabled=not rows.disabled)
                )
                print(
                    "Toggled tool: ", function_name, "to disabled: ", not rows.disabled
                )
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
    finally:
        return err


async def delete_tool(function_name):
    err = None
    try:
        with engine.begin() as conn:
            # also cannot_delete check
            rows = conn.execute(
                select(Tools).where(Tools.function_name == function_name)
            ).fetchone()
            if rows is None:
                raise ValueError(f"Tool {function_name} does not exist.")
            elif rows.cannot_delete:
                raise ValueError(
                    f"Tool {function_name} cannot be deleted. Please contact admin."
                )
            else:
                conn.execute(delete(Tools).where(Tools.function_name == function_name))
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
    finally:
        return err


async def get_analysis_versions(root_analysis_id):
    # get all versions of an analysis
    # get ids that end with -v1, -v2, -v3..
    err = None
    versions = []
    try:
        with engine.begin() as conn:
            cursor = conn.connection.cursor()
            cursor.execute(
                """
                SELECT analysis_id, user_question, gen_steps
                FROM defog_analyses
                WHERE root_analysis_id = ?
                ORDER BY timestamp ASC
                """,
                (root_analysis_id,),
            )
            rows = cursor.fetchall()
            versions = [{"analysis_id": x[0], "user_question": x[1]} for x in rows]
    except Exception as e:
        print(e)
        traceback.print_exc()
        err = str(e)
    finally:
        return err, versions


# returns all combined user_questions of root_analysis + max_n direct parents
# helps embed tools better
async def get_analysis_question_context(analysis_id, max_n=5):
    # get this analysis
    # check direct_parent_id of this analysis
    # and keep going up the analysis chain till we get an is_root_analysis or we reach max_n
    # and finally also get the root_analysis_id from this analysis
    # and merge all the question: root analysis's plus all parents we found
    err = None
    question_context = ""
    try:
        curr_analysis_id = analysis_id

        count = 0
        while True:
            # get this analysis
            err, analysis_data = get_analysis_data(curr_analysis_id)
            if err:
                raise Exception(err)

            if analysis_data["direct_parent_id"] and count <= max_n:
                curr_analysis_id = analysis_data["direct_parent_id"]
                count += 1

                # skip if analysis was not fully completed
                # aka has no steps
                if (
                    not analysis_data["gen_steps"]
                    or len(analysis_data["gen_steps"]) == 0
                ):
                    continue

                # else add this q to context
                question_context = (
                    analysis_data["user_question"] + " " + question_context
                )
            else:
                break

    except Exception as e:
        err = str(e)[:300]
        question_context = ""
    finally:
        return err, question_context
