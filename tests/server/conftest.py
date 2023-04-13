import pytest
from fastapi.testclient import TestClient
from frictionless.server import Server, Config


@pytest.fixture(scope="session")
def api_client(tmpdir_factory):
    config = Config(folder=tmpdir_factory.mktemp("server"))
    server = Server.create(config)
    client = TestClient(server)
    return client


@pytest.fixture(scope="session")
def api_client_root():
    config = Config()
    server = Server.create(config)
    client = TestClient(server)
    return client
