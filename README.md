README
How to Run
1. Install dependencies
pip install -r requirements.txt

2. Start the FastAPI server

From the project root (not inside /app):

python -m uvicorn app.main:app --reload

3. Open API documentation

Visit:

http://127.0.0.1:8000/docs

4. Create a workflow graph

Use:

POST /graph/create


Example body:

{
  "nodes": {
    "split": "split",
    "summarize": "summarize",
    "merge": "merge",
    "refine": "refine"
  },
  "edges": {
    "split": "summarize",
    "summarize": "merge",
    "merge": "refine"
  },
  "start_node": "split"
}

5. Run the workflow
POST /graph/run

6. Check execution state
GET /graph/state/{run_id}
