from agents.planner_executor.tool_helpers.all_tools import tools
from db_utils import add_tool
import os
import asyncio


async def main():
    # initialise basic tools in db
    for key in tools:
        tool = tools[key]
        function_name = tool["function_name"]
        description = tool["description"]
        code = tool["code"]
        tool_name = tool["tool_name"]
        toolbox = tool["toolbox"]
        input_metadata = tool["input_metadata"]
        output_metadata = tool["output_metadata"]
        api_keys = os.environ["DEFOG_API_KEY"].split(",")
        # create embedding for the tool name + description

        for api_key in api_keys:
            err = await add_tool(
                api_key=api_key,
                tool_name=tool_name,
                function_name=function_name,
                description=description,
                code=code,
                input_metadata=input_metadata,
                output_metadata=output_metadata,
                toolbox=toolbox,
                cannot_delete=True,
                cannot_disable=True,
            )

            if err:
                if "already exists" in err:
                    print(f"Tool {function_name} already exists in the database.")
                else:
                    print(f"Error adding tool {tool_name}: {err}")
            else:
                print(f"Tool {function_name} added to the database.")


# Run the main function
asyncio.run(main())
