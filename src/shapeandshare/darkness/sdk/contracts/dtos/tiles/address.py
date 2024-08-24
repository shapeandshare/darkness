from pathlib import Path

from pydantic import BaseModel


class Address(BaseModel):
    world_id: str | None = None
    chunk_id: str | None = None
    tile_id: str | None = None
    entity_id: str | None = None

    def resolve(self) -> Path:
        path: Path = Path()
        if self.world_id is not None:
            path = path / "worlds" / self.world_id
        if self.chunk_id is not None:
            path = path / "chunks" / self.chunk_id
        if self.tile_id is not None:
            path = path / "tiles" / self.tile_id
        if self.entity_id is not None:
            path = path / "entities" / self.entity_id
        path = path / "metadata.json"
        return path
