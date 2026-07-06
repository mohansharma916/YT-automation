from pydantic import BaseModel

from app.models.video_part import VideoPart


class VideoParts(BaseModel):

    parts: list[VideoPart]