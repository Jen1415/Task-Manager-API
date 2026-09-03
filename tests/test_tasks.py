from datetime import datetime, timezone

# get tasks and create tasks
async def test_get_tasks_no_token(async_client):
    response = await async_client.get("/tasks/")
    assert response.status_code == 401


async def test_get_tasks_invalid_token(async_client):
    response = await async_client.get(
        "/tasks/", headers={"Authorization": "Bearer not.a.valid.token"}
    )
    assert response.status_code == 401


async def test_get_tasks_valid_token_empty(async_client, auth_headers):
    response = await async_client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_and_get_task(async_client, auth_headers):
    create_response = await async_client.post(
        "/tasks/",
        json={
            "title": "Write tests",
            "description": "Milestone 3",
            "due_date": datetime.now(timezone.utc).isoformat(),
            "status": "todo",
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["title"] == "Write tests"

    get_response = await async_client.get(f"/tasks/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


async def test_get_task_not_found(async_client, auth_headers):
    response = await async_client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

# update and delete tasks
async def test_update_task(async_client, auth_headers):
    create_response = await async_client.post(
        "/tasks/",
        json={
            "title": "Original title",
            "due_date": datetime.now(timezone.utc).isoformat(),
        },
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    update_response = await async_client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated title"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated title"


async def test_update_task_not_found(async_client, auth_headers):
    response = await async_client.patch(
        "/tasks/9999",
        json={"title": "Doesn't matter"},
        headers=auth_headers,
    )
    assert response.status_code == 404


async def test_delete_task(async_client, auth_headers):
    create_response = await async_client.post(
        "/tasks/",
        json={
            "title": "To be deleted",
            "due_date": datetime.now(timezone.utc).isoformat(),
        },
        headers=auth_headers,
    )
    task_id = create_response.json()["id"]

    delete_response = await async_client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = await async_client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


async def test_delete_task_not_found(async_client, auth_headers):
    response = await async_client.delete("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404