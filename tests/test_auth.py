async def test_register_user(async_client):
    response = await async_client.post(
        "/users/",
        json={"email": "alice@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "hashed_password" not in data
    assert "password" not in data

async def test_register_duplicate_email(async_client):
    payload = {"email": "bob@example.com", "password": "strongpassword123"}

    first = await async_client.post("/users/", json=payload)
    assert first.status_code == 200

    second = await async_client.post("/users/", json=payload)
    assert second.status_code == 409
    assert second.json()["detail"] == "Email already registered"

async def test_login_success(async_client):
    await async_client.post(
        "/users/", 
        json={"email": "carol@example.com", "password": "strongpassword123"}
    )

    response = await async_client.post(
        "auth/login",
        data={"username": "carol@example.com", "password": "strongpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(async_client):
    response = await async_client.post(
        "/auth/login",
        data={"username": "ghost@example.com", "password": "whatever123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"