import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)





def test_client_auth():
    response = client.get("/auth/test")
    assert response.status_code == 200
    assert response.json() == {}