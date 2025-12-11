# imports
import asyncio
from app.storage import GRAPHS, RUNS
from app.tools import TOOL_MAP


# THE GRAPH ENGINE(asyncfunction)
async def run_engine(graph_id: str, run_id: str, initial_state: dict):
    graph = GRAPHS[graph_id]

    state = initial_state
    state["logs"] = []
    state["status"] = "RUNNING"
    RUNS[run_id] = state

    current_node = graph["start_node"]
# run the loop
    while current_node:
        print(f"Executing {current_node}...")
        # Get the tool name for this node
        tool_name = graph["nodes"].get(current_node)
        func = TOOL_MAP.get(tool_name)
        # Run the tool
        if func:
            func(state)

        # if we are at 'refine' check length
        if current_node == "refine":
            if len(state["final"]) > 20:
                next_node = "refine"
            else:
                next_node = None
        else:
            next_node = graph["edges"].get(current_node)
        #implementing sleep for better debugging(optional)
        await asyncio.sleep(0.5)

        if not next_node:
            break

        current_node = next_node

    state["status"] = "COMPLETED"
    RUNS[run_id] = state
