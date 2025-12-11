#imports
import uuid
from fastapi import FastAPI, BackgroundTasks

from app.storage import GRAPHS, RUNS
from app.models import CreateGraphRequest, RunGraphRequest
from app.engine import run_engine


app = FastAPI()
#create graph from user data
@app.post("/graph/create")
def create_graph(req: CreateGraphRequest):
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = req.dict()
    return {"graph_id": graph_id, "msg": "Graph saved"}
#running the created graph
@app.post("/graph/run")
def run_graph(req: RunGraphRequest, background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())
    initial_state = {"input": req.input}
# Run in background 
    background_tasks.add_task(run_engine, req.graph_id, run_id, initial_state)

    return {"run_id": run_id, "status": "STARTED"}
#get current state
@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    return RUNS.get(run_id, {"error": "Run not found"})
