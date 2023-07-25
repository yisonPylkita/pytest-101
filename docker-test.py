import docker
import pytest
import requests
from retry import retry


@pytest.fixture
def env_fixture():
    client = docker.from_env()
    container = client.containers.run(
        "ealen/echo-server", detach=True, ports={"80/tcp": "8080"}
    )
    address = "localhost:8080"
    ensure_server_up(address)
    yield address
    container.kill()


@retry(Exception, tries=100, delay=0.1)
def ensure_server_up(address: str):
    assert requests.get(f"http://{address}").status_code == 200


def test_fruit_salad(env_fixture):
    address = env_fixture

    response = requests.get(f"http://{address}/param", params={"query": "demo"}).json()

    assert len(response) > 0
