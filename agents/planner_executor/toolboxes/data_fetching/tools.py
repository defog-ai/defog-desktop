async def data_fetcher_and_aggregator(
    question: str,
    global_dict: dict = {},
    **kwargs,
):
    """
    This function generates a SQL query and runs it to get the answer.
    """
    from pathlib import Path
    home_path = Path.home()
    log_path = home_path / "defog_logs.txt"
    with open(log_path, "a") as f:
        f.write(f"Question: {question}\n")

    import os
    import asyncio
    import pandas as pd
    from tool_code_utilities import safe_sql, fetch_query_into_df
    from defog import Defog
    from utils import SqlExecutionError

    if question == "" or question is None:
        raise ValueError("Question cannot be empty")

    dev = global_dict.get("dev", False)
    print(f"Dev: {dev}")
    print(f"Global dict currently has keys: {list(global_dict.keys())}")

    # send the data to the Defog, and get a response from it
    defog = Defog()
    defog.base_url = os.environ.get("DEFOG_BASE_URL", "https://api.defog.ai")
    defog.generate_query_url = os.environ.get(
        "DEFOG_GENERATE_URL", defog.base_url + "/generate_query_chat"
    )
    # make async request to the url, using the appropriate library
    try:
        res = await asyncio.to_thread(defog.get_query, question, dev=dev)
        query = res["query_generated"]
        print(query)
    except:
        return {
            "error": "There was an error in generating the query. Please try again."
        }
    
    with open(log_path, "a") as f:
        f.write(f"Query: {query}\n")

    if not safe_sql(query):
        success = False
        print("Unsafe SQL Query")
        return {
            "outputs": [
                {
                    "data": pd.DataFrame(),
                    "analysis": "This was an unsafe query, and hence was not executed",
                }
            ],
            "sql": query.strip(),
        }

    print(f"Running query: {query}")

    with open(log_path, "a") as f:
        f.write(f"Attempting to run query\n")

    try:
        df = await fetch_query_into_df(query)
    except Exception as e:
        print("Raising execution error", flush=True)
        with open(log_path, "a") as f:
            f.write(f"ERROR: {str(e)}\n")
        raise SqlExecutionError(query, str(e))
    
    with open(log_path, "a") as f:
        f.write(f"Answer: {df.to_csv(index=False)}\n")

    analysis = ""
    return {
        "outputs": [{"data": df, "analysis": analysis}],
        "sql": query.strip(),
    }


async def global_dict_data_fetcher_and_aggregator(
    question: str,
    input_dfs: list,  # list of dfs from global dict
    global_dict: dict = {},
    **kwargs,
):
    """
    This function generates a SQL query and runs it on a list of dfs to get the answer.
    """
    import requests
    import asyncio
    import pandas as pd
    from pandasql import sqldf
    from tool_code_utilities import safe_sql

    if question == "" or question is None:
        raise ValueError("Question cannot be empty")

    glossary = global_dict.get("glossary", "")

    # create metadata using input_df's columns as a csv string with the format:
    # table_name,column_name,column_data_type
    metadata = "table_name,column_name,column_data_type\n"
    for input_df in input_dfs:
        df_name = input_df.df_name
        metadata += "\n".join(
            [f"{df_name},{col},{input_df[col].dtype}" for col in input_df.columns]
        )
        # set in globals
        globals()[df_name] = input_df

    # replace "object\n" with "string\n" because there is no object data type in SQL
    metadata = metadata.replace("object\n", "string\n")
    print(
        "Running global_dict_data_fetcher_and_aggregator with this custom metadata: \n"
    )
    print(metadata)
    print("\n")

    question += ". Give me SQLite SQL, not Postgres. Remember that SQLite does not support all the features of Postgres like stddev, variance, etc. You will have to calculate them yourself."

    # send the data to an API, and get a response from it
    url = global_dict["llm_calls_url"]
    payload = {
        "request_type": "generate_sql",
        "question": question,
        "glossary": glossary,
        "metadata": metadata,
    }

    # make async request to the url, using the appropriate library
    r = await asyncio.to_thread(requests.post, url, json=payload)
    res = r.json()
    query = res["query"]

    if not safe_sql(query):
        success = False
        print("Unsafe SQL Query")
        return {
            "outputs": [
                {
                    "data": pd.DataFrame(),
                    "analysis": "This was an unsafe query, and hence was not executed",
                }
            ],
            "sql": query.strip(),
        }

    print(f"Running query: {query}")

    pysqldf = lambda q: sqldf(q, globals())

    df = pysqldf(query)

    analysis = ""
    return {
        "outputs": [{"data": df, "analysis": analysis}],
        "sql": query.strip(),
    }
