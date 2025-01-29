from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create FastAPI app
app = FastAPI()

# Simulated database
task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

# Security
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Pydantic Model
class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: str
    is_finished: bool

# ----------------------
# API Version 1 (apiv1)
# ----------------------
@app.get("/apiv1/tasks/{task_id}")
def get_task_v1(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}

@app.post("/apiv1/tasks", status_code=201)
def add_task_v1(task: Task):
    if task.task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    if any(t["task_id"] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists")
    task_db.append(task.dict())
    return {"status": "ok", "task": task}

@app.patch("/apiv1/tasks/{task_id}", status_code=204)
def update_task_v1(task_id: int, task: Task):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    for t in task_db:
        if t["task_id"] == task_id:
            t.update(task.dict())
            return
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/apiv1/tasks/{task_id}", status_code=204)
def delete_task_v1(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db[:] = [t for t in task_db if t["task_id"] != task_id]
    return

# ----------------------
# API Version 2 (apiv2)
# ----------------------
@app.get("/apiv2/tasks/{task_id}")
def get_task_v2(task_id: int, key: str = Depends(verify_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}

@app.post("/apiv2/tasks", status_code=201)
def add_task_v2(task: Task, key: str = Depends(verify_api_key)):
    if task.task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    if any(t["task_id"] == task.task_id for t in task_db):
        raise HTTPException(status_code=400, detail="Task ID already exists")
    task_db.append(task.dict())
    return {"status": "ok", "task": task}

@app.patch("/apiv2/tasks/{task_id}", status_code=204)
def update_task_v2(task_id: int, task: Task, key: str = Depends(verify_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    for t in task_db:
        if t["task_id"] == task_id:
            t.update(task.dict())
            return
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/apiv2/tasks/{task_id}", status_code=204)
def delete_task_v2(task_id: int, key: str = Depends(verify_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db[:] = [t for t in task_db if t["task_id"] != task_id]
    return
