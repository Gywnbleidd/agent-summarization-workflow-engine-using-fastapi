# imports
from pydantic import BaseModel
from typing import Dict
#pydantic models
class CreateGraphRequest(BaseModel):
    nodes: Dict[str, str]
    edges: Dict[str, str]
    start_node: str

class RunGraphRequest(BaseModel):
    graph_id: str
    input: str
