from dotenv import load_dotenv

load_dotenv()
import requests
import logging

# from jose import JWTError, jwt
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import ory_test.api as ory_test_api


# from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger("ory_sample")

app = FastAPI()

logger.info(f"Starting Ory Sample API...")
app = FastAPI(
    title="Ory Sample API",
    version="0.1",
)


app.include_router(ory_test_api.router)


import uvicorn


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("ory_test.main:app", host="0.0.0.0", port=8000),


def start_debug() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("ory_test.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
