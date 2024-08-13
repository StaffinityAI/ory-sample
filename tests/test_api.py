import pytest
import requests
from xprocess import ProcessStarter

# @pytest.fixture(autouse=True, scope="session")
# def fastapi_server(xprocess):
#     class APIStarter(ProcessStarter):
#         # startup pattern
#         pattern = "Uvicorn running on http://127.0.0.1:8000"
#         max_read_lines = 200
#         # command to start process
#         # args = ["uvicorn", "ory_test.main:app"]
#         args = ["docker", "compose", "up"]

#     # ensure process is running and return its logfile
#     logfile = xprocess.ensure("docker_compose", APIStarter)

#     # conn = # create a connection or url/port info to the server
#     # yield conn
#     yield

#     # clean up whole process tree afterwards
#     xprocess.getinfo("docker_compose").terminate()


# def test_test_endpoint():
#     response = requests.get("http://localhost:8000/api/v1/test")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello, world!"}


# -- need to chnage for ouathkeeper


def test_test_endpoint_secured_unauthenticated():
    response = requests.get("http://localhost:4465/api/v1/test")
    assert response.status_code == 401
    assert response.json() == {
        "error": {
            "code": 401,
            "status": "Unauthorized",
            "message": "Access credentials are invalid",
        }
    }


def get_token(secret: str):
    url = "http://localhost:4444/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": "user123",
        "client_secret": secret,
        "scope": "read",
    }
    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200
    return response.json()["access_token"]


def test_test_endpoint():
    # TODO: This unit test should generate a new user as in tasks.py
    access_token = get_token("test123")
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("http://localhost:4465/api/v1/test", headers=header)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}
