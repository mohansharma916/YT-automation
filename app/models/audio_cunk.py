from pathlib import Path

from pydantic import BaseModel


class AudioChunk(BaseModel):

    index: int

    start: float

    end: float

    path: Path