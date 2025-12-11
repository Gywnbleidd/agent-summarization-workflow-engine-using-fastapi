# README
# How to Run

1.  **Install dependencies**

    ```bash
    pip install fastapi uvicorn pydantic

    ```

2.  **Start the FastAPI server**

    Run this from the project root (NOT inside `/app`):

    ```bash
    python -m uvicorn app.main:app --reload
    ```

3.  **Open API documentation**

    Visit the interactive Swagger UI:
    `http://127.0.0.1:8000/docs`
    you will see:

    POST /graph/create

    POST /graph/run

    GET /graph/state/{run_id}

    All automatically documented by FastAPI.

---

#  Create & Run a Workflow

4.  **Create a workflow graph**

    * **Endpoint:** `POST /graph/create`
    * **Example body:**

        ```json
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
         Click Execute → You’ll get:

         {
          "graph_id": "xxxxx",
          "msg": "Graph saved"
         }
        
         Save that graph_id.
        ```

5.  **Run the workflow**

    * **Endpoint:** `POST /graph/run`
    * **Example request:**

        ```json
        {
          "graph_id": "<your-graph-id>",
          "input": "This is a long text that will be processed by the workflow..."
        }
        Click Execute.

        You will get:

       {
        "run_id": "xxxxx",
        "status": "STARTED"
       }
        ```
6.  **Check Engine State**

    Now use:
    `GET /graph/state/{run_id}`

    You will see:
    * `status`: `RUNNING` or `COMPLETED`
    * Workflow logs (`chunks`, `summaries`, `final text`)

    * **Example response:**

        ```json
        {
          "status": "COMPLETED",
          "logs": [
            "Split into 3 chunks.",
            "Summarized chunks.",
            "Merged summaries.",
            "Refining... length is now 42",
            "Refining... length is now 37",
            "Refinement complete."
          ],
          "final": "shorter summary..."
        }
        ```
#  What the Workflow Engine Supports

### **Graph-based Workflow Execution**
Your engine allows you to define:
* **nodes** (steps in the workflow)
* **edges** (connections between steps)
* a **start node**

It executes nodes in the correct order based on the graph structure. 

### **Shared State Between Nodes**
A global state dictionary is passed through the workflow.

Each node:
* reads data from the state
* writes its own output back into the state

This is how information flows between steps.

### **Built-in Agent-Style Tools**
The engine includes four example tools:
* `split` → splits text into chunks
* `summarize` → generates mock summaries
* `merge` → merges summaries into one output
* `refine` → iteratively shortens the result

These demonstrate how you can build an agent workflow.

### **Looping / Branching Support**
The `refine` node loops until a condition is met.

This shows the engine supports:
* conditional transitions
* self-loops
* dynamic routing based on state values

### **Asynchronous Background Execution**
Workflows run using FastAPI’s `BackgroundTasks`, which means:
* the API returns immediately
* the workflow continues running in the background
* users can check progress via `/graph/state/{run_id}`

### **Execution Logging**
Every node appends human-readable logs to `state["logs"]`, allowing:
* step-by-step debugging
* transparency into the workflow process

### **Multiple Simultaneous Runs**
Each workflow invocation receives a unique `run_id`, enabling many workflows to run at the same time without interfering with each other.

---

#  What I Would Improve With More Time

### **1. Persistent Storage**
Right now graphs and runs are stored in Python dictionaries (in-memory).

With more time, I would replace them with:
* Redis
* PostgreSQL
* SQLite

This would allow:
* runs to survive server restarts
* better scalability
* multi-user support

### **2️. Visual Graph Editor + Viewer**
I would add:
* a UI to draw nodes and edges
* a visualization endpoint
* a flow diagram showing which node executed when 

This makes the workflow engine easier to understand and debug.

### **3️. Advanced Conditional Logic**
Right now conditions are simple (e.g., length check).

I would support:
* multiple possible next nodes
* decision trees
* complex routing rules
* parallel execution paths

### **4️. Real Summarization Using an LLM**
Replace mock tools with actual models like:
* OpenAI GPT
* Cohere
* HuggingFace transformers

This would convert the engine into a real AI agent system.

### **5️. Retry, Error Handling, and Fail States**
Improve workflow robustness by adding:
* auto-retry on failure
* error logs
* fail state tracking
* partial rollback

### **6 Live Log Streaming via WebSockets**
Instead of polling with `/graph/state/{run_id}`, I would implement:
* real-time log streaming
* live workflow updates
* better user experience
