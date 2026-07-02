from pydantic import BaseModel


class SubtitleSegment(BaseModel):
    start: float
    end: float
    text: str


class Subtitle(BaseModel):
    segments: list[SubtitleSegment]