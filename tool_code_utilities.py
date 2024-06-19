# includes utilties that a user can import when writing their tool code
# top level for a cleaner import statement
# from tool_code_utilities import xx

import asyncio
from defog import Defog
from defog.query import execute_query
import re
import pandas as pd
import os
from db_utils import get_api_key

from pathlib import Path
home_dir = Path.home()

# see if we have a custom report assets directory
if not os.path.exists(home_dir / "defog_report_assets"):
    # create one
    os.mkdir(home_dir / "defog_report_assets")

report_assets_dir = home_dir / "defog_report_assets"

report_assets_dir = os.environ.get("REPORT_ASSETS_DIR", report_assets_dir.as_posix())

# make sure the query does not contain any malicious commands like drop, delete, etc.
def safe_sql(query):
    if query is None:
        return False

    query = query.lower()
    if (
        "drop" in query
        or "delete" in query
        or "truncate" in query
        or "append" in query
        or "insert" in query
        or "update" in query
    ):
        return False

    return True


async def fetch_query_into_df(sql_query: str) -> pd.DataFrame:
    """
    Runs a sql query and stores the results in a pandas dataframe.
    """

    # important note: this is currently a blocking call
    # TODO: add an option to the defog library to make this async
    defog = Defog()
    db_type = defog.db_type
    db_creds = defog.db_creds

    colnames, data, new_sql_query = await asyncio.to_thread(
        execute_query, sql_query, get_api_key(), db_type, db_creds, retries=0
    )
    df = pd.DataFrame(data, columns=colnames)

    # if this df has any columns that have lists, remove those columns
    for col in df.columns:
        if df[col].apply(type).eq(list).any():
            df = df.drop(col, axis=1)

    df.sql_query = sql_query
    return df


def natural_sort_function(l, ascending=True):
    """
    Sorts a list or a pandas series in a natural way.
    If it's a list of numbers or datetimes, just sort them normally.
    If it's a string, check if there are numbers in the string, and sort them as a heirarchy of numbers.
    Example 1: ['a', 'b', 'c'] would be sorted as ['a', 'b', 'c']
    Example 2: ['1', '10', '2'] would be sorted as ['1', '2', '10']
    Example 3: ['a1', 'a10', 'a2'] would be sorted as ['a1', 'a2', 'a10']
    Example 4: ['C1D1', 'C10D10', 'C2D2', 'C1D11'] would be sorted as ['C1D1', 'C1D11', 'C2D2', 'C10D10']
    """

    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    if type(l) == pd.Series:
        # TODO do this in a more efficient way
        l = l.tolist()

    l.sort(key=alphanum_key, reverse=not ascending)
    return l


def natural_sort(df, time_column, units=None, ascending=True):
    """
    Sorts a dataframe in a natural way, using the natural_sort_function.
    """
    if df[time_column].dtype == "object":
        order = natural_sort_function(df[time_column].unique().tolist())
        df[time_column] = pd.Categorical(
            df[time_column], categories=order, ordered=True
        )
        if units:
            df = df.sort_values(by=[units, time_column], ascending=ascending)
        else:
            df = df.sort_values(by=time_column, ascending=ascending)
    else:
        df = df.sort_values(by=time_column, ascending=ascending)
    return df


default_top_level_imports = "\n\n".join(
    [
        "from agents.planner_executor.tool_helpers.tool_param_types import (",
        "  DBColumn,",
        "  DropdownSingleSelect,",
        "  ListWithDefault,",
        "  db_column_list_type_creator,",
        ")",
        "import pandas",
        "import pandas as pd",
    ]
)


def add_default_imports(code):
    """
    Adds the default imports to the code.
    """
    return default_top_level_imports + "\n\n" + code


def fix_savefig_calls(code):
    """
    Fixes the savefig calls in the code by changing the path and always appending report_assets_dir variable to the path.
    """
    # check both for double and single quote
    code = code.replace('savefig("', f'savefig({report_assets_dir} + "')
    code = code.replace("savefig('", f"savefig({report_assets_dir} + '")
    # remove jic we got two slashes
    code = code.replace("//", "/")
    return code
