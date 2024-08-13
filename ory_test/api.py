import logging
logger = logging.getLogger("ory_test")

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    async with AsyncClient() as client:
        response = await client.get(
            "http://kratos:4433/sessions/whoami",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        user_info = response.json()
        return user_info

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict

logger = logging.getLogger("ory_test")

router = APIRouter()

class SampleResponseSchema(BaseModel):
    message: str

async def check_team(user_info: dict, required_team: str):
    if user_info["identity"]["traits"]["team"] != required_team:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Team mismatch")

@router.get("/api/v1/frontend", response_model=SampleResponseSchema)  # type: ignore
async def read_frontend_data(user_info: dict = Depends(get_current_user)) -> SampleResponseSchema:
    await check_team(user_info, "frontend")
    return SampleResponseSchema(message="Hello, frontend world!")

@router.get("/api/v1/backend", response_model=SampleResponseSchema)  # type: ignore
async def read_backend_data(user_info: dict = Depends(get_current_user)) -> SampleResponseSchema:
    await check_team(user_info, "backend")
    return SampleResponseSchema(message="Hello, backend world!")

