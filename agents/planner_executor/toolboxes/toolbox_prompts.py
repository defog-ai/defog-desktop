# - tool_name: simple_stats
#   description: Gets simple statistics from a pandas df using numpy and pandas.
#   inputs: [snippets of python code for each calculation]
#   outputs: [pandas dfs in the same order as the above snippets]


toolbox_prompts = {
    "data-fetching": """
- tool_name: data_fetcher_and_aggregator
  description: Converting a natural language question into a SQL query, that then runs on an external database. Fetches, filters, aggregates, and performs arithmetic computations on data. Remember that this tool does not have access to the data returned by the previous steps. It only has access to the data in the database.
  inputs: [natural language description of the data required to answer this question (or get the required information for subsequent steps) as a string]
  outputs: pandas df
  
- tool_name: global_dict_data_fetcher_and_aggregator
  description: Converting a natural language question into a SQL query, that then runs on a database that is stored in global_dict. Fetches, filters, aggregates, and performs arithmetic computations on data. This tool has access to all of global_dict. This will only run on the data that is stored in global_dict. For external databases, use the data_fetcher_and_aggregator tool.
  inputs: [natural language description of the data required as a string, "global_dict.<input_df_name>"]
  outputs: pandas df""",
    "stats": """-tool_name: t_test
  description: This function gets two groups and runs a t-test to check if there is a significant difference between their means. There are two ways to run the test: paired and unpaired. Paired test has one group column, unpaired has one group column.
  inputs: ["global_dict.<input_df_name>", group column, score column, name column or None, type of t test as a string (paired or unpaired)]
  outputs: pandas df

-tool_name: wilcoxon_test
  description: This function gets two groups and runs a wilcoxon test to check if there is a significant difference between their means.
  inputs: ["global_dict.<input_df_name>", group column, score column, name column]
  outputs: pandas df""",
}
