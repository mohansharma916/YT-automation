from pathlib import Path

from pydantic import BaseModel
from app.models.short import Shorts
from app.models.subtitle import Subtitle


class Timeline(BaseModel):

    audio: Path

    subtitle: Subtitle

    duration: float

    shorts: Shorts | None = None