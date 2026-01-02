import os
os.environ["DATABASE_URL"] = ":memory:"

from app import db
db.init_db()

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_crud_flow():
    # create
    r = client.post("/todos", json={"title": "Test item"})
    assert r.status_code == 201
    todo = r.json()
    todo_id = todo["id"]

    # read
    r = client.get(f"/todos/{todo_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test item"

    # update
    r = client.put(f"/todos/{todo_id}", json={"title": "Updated", "completed": True})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"
    assert r.json()["completed"] is True

    # delete
    r = client.delete(f"/todos/{todo_id}")
    assert r.status_code == 204

    # not found afterwards
    r = client.get(f"/todos/{todo_id}")
    assert r.status_code == 404
