import pytest
from starlette.testclient import TestClient

from icehockey_rules.app import app


@pytest.fixture(scope="function")
def app_test_client() -> TestClient:
    return TestClient(app=app, headers={})
