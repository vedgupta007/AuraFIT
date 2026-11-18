import pytest
import os
os.environ["TESTING"] = "1"
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    # Because 'localhost' is in URI, mongomock_motor will be used in memory automatically
    # Context manager triggers lifespan to create mock client and indexes
    with TestClient(app) as c:
        yield c

