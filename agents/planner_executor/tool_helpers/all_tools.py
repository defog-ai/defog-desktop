# this is where you can import your custom tools
# create a folder insider toolboxes and add your tools (aka python functions) there inside a tools.py file
# and finally add all your tools in the tools array below in the given format
from ..toolboxes.data_fetching.tools import *
from ..toolboxes.stats.tools import *

import inspect

tool_name_dict = tools = {
    "data_fetcher_and_aggregator": {
        "function_name": "data_fetcher_and_aggregator",
        "tool_name": "Fetch data from database",
        "description": "Converting a natural language question into a SQL query, that then runs on an external database. Fetches, joins, filters, aggregates, and performs arithmetic computations on data. Remember that this tool does not have access to the data returned by the previous steps. It only has access to the data in the database. We should attempt to give this tool very specific questions that pertain to the user question, instead of overly broad or generic ones. However, do not make any mention of which table to query when you give it your question. You can use this exactly once among all steps.",
        "fn": data_fetcher_and_aggregator,
        "code": inspect.getsource(data_fetcher_and_aggregator),
        "input_metadata": {
            "question": {
                "name": "question",
                "default": None,
                "description": "natural language description of the data required to answer this question (or get the required information for subsequent steps) as a string",
                "type": "str",
            },
        },
        "toolbox": "data_fetching",
        "output_metadata": [
            {
                "name": "output_df",
                "description": "pandas dataframe",
                "type": "pandas.core.frame.DataFrame",
            }
        ],
    },
    "global_dict_data_fetcher_and_aggregator": {
        "function_name": "global_dict_data_fetcher_and_aggregator",
        "tool_name": "Query data from a pandas dataframe",
        "fn": global_dict_data_fetcher_and_aggregator,
        "code": inspect.getsource(global_dict_data_fetcher_and_aggregator),
        "description": "Converting a natural language question into a SQL query, that then runs on a database that is stored in global_dict. Fetches, filters, aggregates, and performs arithmetic computations on data. This tool has access to all of global_dict. This will only run on the data that is stored in global_dict. For external databases, use the data_fetcher_and_aggregator tool.",
        "input_metadata": {
            "question": {
                "name": "question",
                "default": None,
                "description": "Natural language description of the data required as a string",
                "type": "str",
            },
            "input_dfs": {
                "name": "input_dfs",
                "default": None,
                "meta_": "global_dict.<input_df_name>",
                "description": "A list of dataframes stored in global_dict. [global_dict.<input_df_name>, global_dict.<input_df_name> ...]",
                "type": "list",
            },
        },
        "toolbox": "data_fetching",
        "output_metadata": [
            {
                "name": "output_df",
                "description": "pandas dataframe",
                "type": "pandas.core.frame.DataFrame",
            }
        ],
    },
    "t_test": {
        "function_name": "t_test",
        "fn": t_test,
        "code": inspect.getsource(t_test),
        "tool_name": "T Test",
        "description": "This function gets two groups and runs a t-test to check if there is a significant difference between their means. There are two ways to run the test: paired and unpaired. Paired test has one group column, unpaired has one group column.",
        "input_metadata": {
            "full_data": {
                "name": "full_data",
                "default": None,
                "description": '"global_dict.<input_df_name>"',
                "type": "pandas.core.frame.DataFrame",
            },
            "group_column": {
                "name": "group_column",
                "default": None,
                "description": "group column",
                "type": "DBColumn",
            },
            "score_column": {
                "name": "score_column",
                "default": None,
                "description": "score column",
                "type": "DBColumn",
            },
            "name_column": {
                "name": "name_column",
                "default": None,
                "description": "name column or None",
                "type": "DBColumn",
            },
            "t_test_type": {
                "name": "t_test_type",
                "default": ["unpaired", "paired"],
                "description": "type of t test as a string (paired or unpaired)",
                "type": "DropdownSingleSelect",
            },
        },
        "toolbox": "stats",
        "output_metadata": [
            {
                "name": "output_df",
                "description": "pandas dataframe",
                "type": "pandas.core.frame.DataFrame",
            }
        ],
    },
    "wilcoxon_test": {
        "function_name": "wilcoxon_test",
        "fn": wilcoxon_test,
        "code": inspect.getsource(wilcoxon_test),
        "tool_name": "Wilcoxon Test",
        "description": "This function gets two groups and runs a wilcoxon test to check if there is a significant difference between their means.",
        "input_metadata": {
            "full_data": {
                "name": "full_data",
                "default": None,
                "description": '"global_dict.<input_df_name>"',
                "type": "pandas.core.frame.DataFrame",
            },
            "group_column": {
                "name": "group_column",
                "default": None,
                "description": "group column",
                "type": "DBColumn",
            },
            "score_column": {
                "name": "score_column",
                "default": None,
                "description": "score column",
                "type": "DBColumn",
            },
            "name_column": {
                "name": "name_column",
                "default": None,
                "description": " name column",
                "type": "DBColumn",
            },
        },
        "toolbox": "stats",
        "output_metadata": [
            {
                "name": "output_df",
                "description": "pandas dataframe",
                "type": "pandas.core.frame.DataFrame",
            }
        ],
    },
}
