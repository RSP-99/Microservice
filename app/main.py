from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import db

app = FastAPI(title="Simple Todo microservice")


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Todo(TodoBase):
    id: int


@app.on_event("startup")
def startup_event():
    db.init_db()


@app.get("/", summary="Health check")
def root():
    return {"message": "Todo microservice is running"}


def _payload_to_dict(payload: TodoBase) -> dict:
    # support pydantic v1 and v2
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoBase):
    data = _payload_to_dict(payload)
    row = db.create_todo(data["title"], data.get("description"), data.get("completed", False))
    return Todo(**row)


@app.get("/todos", response_model=List[Todo])
def list_todos():
    rows = db.list_todos()
    return [Todo(**r) for r in rows]


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    row = db.get_todo(todo_id)
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**row)


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoBase):
    data = _payload_to_dict(payload)
    row = db.update_todo(todo_id, data["title"], data.get("description"), data.get("completed", False))
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**row)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    ok = db.delete_todo(todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return


# Allow all origins for easy local testing (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
