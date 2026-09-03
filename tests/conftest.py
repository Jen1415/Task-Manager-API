import os
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from taskmanagerapi.database import Base, get_db
from taskmanagerapi.main import app

from taskmanagerapi.models import user, task

engine = create_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest_asyncio.fixture
async def async_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest_asyncio.fixture()
async def auth_headers(async_client):
    await async_client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "strongpassword123"},
    )
    response = await async_client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "strongpassword123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}   