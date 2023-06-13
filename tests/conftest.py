import pytest
from fastapi.testclient import TestClient

from my_cookbook import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)
