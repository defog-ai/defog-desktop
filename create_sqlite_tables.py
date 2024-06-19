# read a sql file, and create tables in sqlite database

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, Boolean
from sqlalchemy.dialects.sqlite import JSON
import os
from pathlib import Path

def create_sqlite_tables():
    home_dir = Path.home()
    path_to_sql_file = home_dir / "defog_local.db"

    if not os.path.exists(path_to_sql_file):
        print(f"Creating SQLite database at {path_to_sql_file}")
        open(path_to_sql_file, "w").close()
    else:
        print(f"SQLite database already exists at {path_to_sql_file}")
        return

    # Create an engine (SQLite in this example)
    engine = create_engine(f"sqlite:///{path_to_sql_file}", echo=True)

    # Initialize MetaData object
    metadata = MetaData()

    # Define tables
    defog_docs = Table(
        "defog_docs",
        metadata,
        Column("doc_id", Text, primary_key=True),
        Column("doc_md", Text),
        Column("doc_blocks", JSON),
        Column("editor_defog_blocks", JSON),
        Column("api_key", Text, nullable=False),
        Column("timestamp", Text),
        Column("username", Text),
        Column("doc_xml", Text),
        Column("doc_uint8", JSON),
        Column("doc_title", Text),
        Column("archived", Boolean, default=False),
    )

    defog_recently_viewed_docs = Table(
        "defog_recently_viewed_docs",
        metadata,
        Column("username", Text, primary_key=True),
        Column("api_key", Text, nullable=False),
        Column("recent_docs", JSON),
    )

    defog_reports = Table(
        "defog_reports",
        metadata,
        Column("report_id", Text, primary_key=True),
        Column("api_key", Text, nullable=False),
        Column("email", Text),
        Column("timestamp", Text),
        Column("report_uuid", Text),
        Column("approaches", JSON),
        Column("report_markdown", Text),
        Column("clarify", JSON),
        Column("understand", JSON),
        Column("gen_approaches", JSON),
        Column("user_question", Text),
        Column("gen_report", JSON),
        Column("gen_steps", JSON),
        Column("follow_up_analyses", JSON),
        Column("parent_analyses", JSON),
        Column("is_root_analysis", Boolean, default=True),
        Column("root_analysis_id", Text),
        Column("direct_parent_id", Text),
        Column("username", Text),
    )

    defog_table_charts = Table(
        "defog_table_charts",
        metadata,
        Column("table_id", Text, primary_key=True),
        Column("data_csv", JSON),
        Column("query", Text),
        Column("chart_images", JSON),
        Column("sql", Text),
        Column("code", Text),
        Column("tool", JSON),
        Column("edited", Integer),
        Column("error", Text),
        Column("reactive_vars", JSON),
    )

    defog_tool_runs = Table(
        "defog_tool_runs",
        metadata,
        Column("tool_run_id", Text, primary_key=True),
        Column("step", JSON),
        Column("outputs", JSON),
        Column("tool_name", Text),
        Column("tool_run_details", JSON),
        Column("error_message", Text),
        Column("edited", Integer),
        Column("analysis_id", Text),
    )

    defog_toolboxes = Table(
        "defog_toolboxes",
        metadata,
        Column("api_key", Text, primary_key=True),
        Column("username", Text, nullable=False),
        Column("toolboxes", JSON),
    )

    defog_tools = Table(
        "defog_tools",
        metadata,
        Column("tool_name", Text, primary_key=True),
        Column("function_name", Text, nullable=False),
        Column("description", Text, nullable=False),
        Column("code", Text, nullable=False),
        Column("input_metadata", JSON),
        Column("output_metadata", JSON),
        Column("toolbox", Text),
        Column("disabled", Boolean, default=False),
        Column("cannot_delete", Boolean, default=False),
        Column("cannot_disable", Boolean, default=False),
    )

    defog_users = Table(
        "defog_users",
        metadata,
        Column("username", Text, primary_key=True),
        Column("hashed_password", Text),
        Column("token", Text),
        Column("user_type", Text),
        Column("csv_tables", Text),
        Column("is_premium", Integer),
        Column("created_at", Text),
        Column("is_verified", Integer),
    )

    defog_plans_feedback = Table(
        "defog_plans_feedback",
        metadata,
        Column("analysis_id", Text, primary_key=True),
        Column("api_key", Text, nullable=False),
        Column("user_question", Text, nullable=False),
        Column("username", Text, nullable=False),
        Column("comments", JSON),
        Column("is_correct", Boolean, nullable=False),
        Column("metadata", Text, nullable=False),
        Column("client_description", Text),
        Column("glossary", Text),
        Column("db_type", Text, nullable=False),
    )

    # Create tables in the database
    metadata.create_all(engine)
    return

if __name__ == "__main__":
    create_sqlite_tables()