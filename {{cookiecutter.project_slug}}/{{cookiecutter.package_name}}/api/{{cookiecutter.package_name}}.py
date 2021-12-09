# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/v1", tags=["{{cookiecutter.package_name}}"])

logger = logging.getLogger(__name__)

# CHANGE BELOW
class Item(BaseModel):
    item1: str = Field(...)

class ResponseExample(BaseModel):
    synced: bool = Field(...)
    path: str = Field(...)
    fstat: str = Field(...)


@router.post("/example_route", response_model=ResponseExample)
async def example_route(item: Item) -> ResponseExample:

    # ... your logic goes here
    
    return ResponseExample(
        synced=True,
        fstat="example",
        path="/bla",
    )
