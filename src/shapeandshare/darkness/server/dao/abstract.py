import logging
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from src.shapeandshare.darkness import WrappedData

logger = logging.getLogger()

T = TypeVar("T")


class DocumentType(str, Enum):
    WORLD = "worlds"
    ISLAND = "islands"
    TILE = "tiles"
    ENTITY = "entities"


# class DocumentPath(BaseModel):
# tables = ["worlds", "islands", "tiles", "entities"]


class AbstractDao[T](BaseModel):
    storage_base_path: Path

    @staticmethod
    def recursive_dict_merge(dict1: dict, dict2: dict) -> dict:
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                dict1[key] = AbstractDao.recursive_dict_merge(dict1[key], value)
            else:
                # Merge non-dictionary values
                dict1[key] = value
        return dict1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_base_path.mkdir(parents=True, exist_ok=True)

    def _document_path(self, tokens: dict) -> Path:
        path: Path = self.storage_base_path
        if "world_id" in tokens:
            path = path / "worlds" / tokens["world_id"]

        if "island_id" in tokens:
            path = path / "islands" / tokens["island_id"]

        if "tile_id" in tokens:
            path = path / "tiles" / tokens["tile_id"]

        if "entity_id" in tokens:
            path = path / "entities" / tokens["entity_id"]

        return path / "metadata.json"

    # @abstractmethod
    # def _document_path(self, *args, **kwargs) -> Path:
    #     """ """

    @abstractmethod
    async def get(self, *args, **kwargs) -> WrappedData[T]:
        """ """

    @abstractmethod
    async def post(self, *args, **kwargs) -> WrappedData[T]:
        """ """

    @abstractmethod
    async def put(self, *args, **kwargs) -> WrappedData[T]:
        """ """

    @abstractmethod
    async def patch(self, *args, **kwargs) -> WrappedData[T]:
        """ """

    @abstractmethod
    async def delete(self, *args, **kwargs) -> bool:
        """ """
