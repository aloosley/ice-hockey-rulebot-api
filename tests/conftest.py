import pytest
from starlette.testclient import TestClient

from app import app


@pytest.fixture(scope="function")
def app_test_client() -> TestClient:
    return TestClient(app=app, headers={})
