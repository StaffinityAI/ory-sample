from invoke import task
import requests


@task
def dk_attach_hydra(c):
    """This method is for open shell inside docker"""
    c.run("docker exec -it ory-test-hydra-1 /bin/sh", pty=True)


@task
def generate_user(c):
    """This method is for registering user inside hydra db"""
    c.run(
        """curl --request POST --url http://localhost:4445/clients --header 'Content-Type: application/json' --data '{
    "client_id": "user123",
    "client_secret": "test123",
    "grant_types": ["client_credentials"],
    "response_types": ["token"],
    "scope": "read",
    "redirect_uris": ["http://localhost:8000/callback"]
  }'"""
    )


@task
def client_secret_post(c):
    """This method is for giving permission to user for gerenarting acces token"""
    c.run(
        """curl --request PUT --url http://localhost:4445/clients/user123 --header 'Content-Type: application/json' --data '{
    "client_secret": "test123",
    "grant_types": ["client_credentials"],
    "response_types": ["token"],
    "scope": "read write",
    "redirect_uris": ["http://localhost:8000/callback"],
    "token_endpoint_auth_method": "client_secret_post"
  }' """
    )


@task
def gen_access_token(c, secret="test123"):
    """this is the funtion for generation access token"""
    c.run(
        f"curl --request POST  --url http://localhost:4444/oauth2/token --header 'Content-Type: application/x-www-form-urlencoded' --data 'grant_type=client_credentials&client_id=user123&client_secret={secret}&scope=read'",
        pty=True,
    )


@task
def hydra_psql(c):
    c.run("docker compose exec hydra-database psql -U postgres -d hydra", pty=True)


@task
def check_secure_endpoint(c):
    c.run(
        """ curl --request GET --url http://localhost:4465/api/v1/test --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImY0NGM4OGI2LTU2ZjgtNGExOS1hNGE5LTIzNDRhMTI1ZTllNyIsInR5cCI6IkpXVCJ9.eyJhbXIiOlsicGFzc3dvcmQiXSwiYXRfaGFzaCI6ImdVWXI4WUtCWjVObEJsWGppV3o0QkEiLCJhdWQiOlsiZWQ5ZGFjNTUtZmQyMi00YzA2LTkzNzAtZDg0MWNkNzUxM2JmIl0sImF1dGhfdGltZSI6MTcyMjkzNTE4NCwiZXhwIjoxNzIyOTQxNTQxLCJpYXQiOjE3MjI5Mzc5NDEsImlzcyI6Imh0dHA6Ly8xMjcuMC4wLjE6NDQ0NCIsImp0aSI6IjhmMGE5NGMxLWVmNTEtNDNmZS1hNDhkLTNmYWUzZThjZWQzZCIsInJhdCI6MTcyMjkzNzg3Mywic2lkIjoiZTVhMTZlZTgtMzgyNy00MTI2LTkxMzQtZjA5NzlhMGMzOTIwIiwic3ViIjoiZGY1MWJmMmItY2M0MC00Y2VmLWE3OGYtMDNhMDMxOTdjMjAzIn0.Liu1G_S-G__uoqicre03mMYRzLviOUkWDKli852SSIzg0dO1orbEU8XFBaLZaRj-p7k8FBCEPhY4SYZEHYDQfMdypJ9CuxVQBXiLSFo9VLiIJx-nyXiLAT0l2wA0GCEcF7VLNc12MzAXrJoWiU0zfp4BnQYsakHkpAFpGOFhBqhQFSlY0KwavrTwv3ikRYVAl7BhJ_wl1BajWhVbJ5Bj7fDfkci4JcWNXWINevEWFFD_kYp7TTRxTLPeeeThXSAljic2SLvyE25l19yXIFtUN5JInHT7M2XTH_8KUdB1IH3lFGn-GGNlndNnKw7bA4PQLUej_MoOjT6matRnaMLRREvPQWDo2BF0wxwO5V8iE2aRa6B4DVsbLFnGaxwbWCpq0GOmrQBFow0k_5wcPv6fdCBiWzDwjGSN2F2LhOkIaidFqLVMa95MRSgv0JzdYZc_hJjVGnpGwXNdpBc9WOfTAgEgB3eqZke6NXpuH9gsxVS3lj3H-JnRj99wump7oc0eSOipwbzAduVwjdOnOxdZ8eRRyekEeCHcqtTj2AUIlQxxKHZfrgkE9Am4KIV2A4Zh_PMMvrJDUykL7cAXHQ6AkvfMSNG2qqFg6D5BegtQBbSR0ACxELQlnR-K5MJBqJYdiCW45VIZa6OU3hbaTqDZZCELbBKwMeeDY9dJiCVwiAk'""",
        pty=True,
    )


@task
def attach_fastapi(c):
    c.run("docker compose exec fastapi /bin/sh", pty=True)


@task
def validate_token(c, token):
    # token = request.headers["Authorization"].split(" ")[1]
    url = "http://localhost:4445/oauth2/introspect"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"token": token}
    response = requests.post(url=url, data=data, headers=header)
    print(response.json())


@task
def get_health_status(c):
    url = "http://127.0.0.1:4433/health/alive"
    response = requests.get(url=url)
    print(response.json())


@task
def get_client_details(c):
    url = "http://127.0.0.1:4445/admin/clients"
    response = requests.get(url=url)
    print(response.json())


@task
def create_clients(c):
    url = "http://127.0.0.1:4445/admin/clients"
    data = {
        "grant_types": ["authorization_code", "refresh_token"],
        "redirect_uris": ["http://127.0.0.1:5555/callback"],
        "response_types": ["code", "id_token"],
        "scope": "openid offline",
        "token_endpoint_auth_method": "none",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, json=data, headers=headers)
    print(response.json())


@task
def query_endpoint(c, auth_code, team):
    url = f"http://0.0.0.0:8000/api/v1/{team}"
    payload = {}
    headers = {"Authorization": f"Bearer {auth_code}"}
    response = requests.get(url, headers=headers, data=payload)
    print(response.json())


# ------------------------------------------------------------------


@task
def get_registration_flow_id(c):
    url = "http://127.0.0.1:4433/self-service/registration/api"
    response = requests.get(url=url)
    print(response.json()["id"])
    return response.json()["id"]


@task
def register(c, id, name, email, team, password):
    url = "http://127.0.0.1:4433/self-service/registration"
    data = {
        "method": "password",
        "password": password,
        "traits": {
            "name": name,
            "email": email,
            "team": team,
            "company_name": "staffinity",
        },
    }
    params = {"flow": id}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, json=data, headers=headers, params=params)
    print(response.json())
    # return response.json()["id"]


@task
def get_login_flow_id(c):
    url = "http://127.0.0.1:4433/self-service/login/api"
    response = requests.get(url=url)
    print(response.json()["id"])
    return response.json()["id"]


@task
def login(c, id, email, password):
    url = "http://127.0.0.1:4433/self-service/login"
    data = {
        "method": "password",
        "password": password,
        "identifier": email,
    }

    params = {"flow": id}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, json=data, headers=headers, params=params)
    print(response.json())
    return response.json()["session_token"]


@task
def query_frontend(c):
    name = "frontend_user"
    email = "frontend_user@gmail.com"
    team = "frontend"
    password = "test1234"
    registration_flow_id = get_registration_flow_id(c)
    login_flow_id = get_login_flow_id(c)
    register(c, registration_flow_id, name, email, team, password)
    auth_code = login(c, login_flow_id, email, password)
    query_endpoint(c, auth_code, team)


@task
def query_backend(c):
    name = "backend_user"
    email = "backend_user@gmail.com"
    team = "backend"
    password = "test1234"
    registration_flow_id = get_registration_flow_id(c)
    login_flow_id = get_login_flow_id(c)
    register(c, registration_flow_id, name, email, team, password)
    auth_code = login(c, login_flow_id, email, password)
    query_endpoint(c, auth_code, team)
