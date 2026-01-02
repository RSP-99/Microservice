# Simple FastAPI Todo Microservice

This repository contains a minimal FastAPI microservice that provides CRUD operations for `Todo` items using an in-memory store (for demo/testing only).

Run locally

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the server (development):

```powershell
uvicorn app.main:app --reload
```

API endpoints

- `GET /` : health check
- `POST /todos` : create a todo (JSON body: `title`, optional `description`, optional `completed`)
- `GET /todos` : list all todos
- `GET /todos/{id}` : get one
- `PUT /todos/{id}` : update
- `DELETE /todos/{id}` : delete

Run tests

```powershell
pytest -q
```

Docker

Build and run:

```powershell
docker build -t fastapi-todo:local .
docker run -p 8000:80 fastapi-todo:local
```

Notes

- This uses an in-memory store; restart clears data. Replace with a DB for production.
- CORS is wide open for convenience in this example; tighten it in production.
