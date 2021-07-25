# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from {{cookiecutter.project_slug}}.config import GCONFIG

router = APIRouter(prefix="/api/v1", tags=["{{cookiecutter.project_slug}}"])

logger = logging.getLogger(__name__)


class Item(BaseModel):
   info: str = Field(...)

@router.post("/info", response_model=Item)
async def check_validity():
    return {"info": "implementMe"}
